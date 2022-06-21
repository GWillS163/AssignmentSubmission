import os
import time
from datetime import datetime
# from venv import logger
from zipfile import ZipFile

from django.contrib import admin

# Register your models here.
from django.contrib.admin import register, display
from django.http import HttpResponse, StreamingHttpResponse

from infoManage.models import Curriculum
from userManage.models import userInfo
from .models import Assignment, FilesModel
from django.forms import TextInput, Textarea
from django.db import models
from threading import Thread


def read_file(file_name, chunk_size=512):
    with open(file_name, "rb") as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break


class AssignmentAdmin(admin.ModelAdmin):
    # exclude = ('relateCurriculum',)
    list_display = (
    'title', 'deadLine', 'status', 'fileNameRule', 'assignmentDescribe', 'relateCurriculum', 'fileDescribe',)
    fieldsets = (
        (
            '基本', {'fields': (('title', 'fileNameRule'),
                              ('relateCurriculum'), ('deadLine', 'status'),
                              ('assignmentDescribe', 'fileDescribe',))}
        ),
    )
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '40'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }
    list_editable = ('fileNameRule', 'relateCurriculum', 'deadLine', 'status')


    def get_list_display_links(self, request, list_display):
        if request.user.is_superuser:
            return ('title')
        else:
            return


class FilesModelAdmin(admin.ModelAdmin):
    list_per_page = 20
    # TODO: 自动填写上传用户
    actions_on_bottom = True
    actions = ['download']
    fieldsets = (
        (
            '基本内容', {'fields': (('relateAssignment', 'fileName'), ('file'),)}
        ),
        (
            '高级', {'fields': (('fileSize', 'relateCurriculum', 'relateUser',),)}
        ),
    )
    # list_filter = ['fileName']
    # preserve_filters =
    # list_display_links = None
    def get_list_display(self, request):
        if request.user.is_superuser:
            return ('fileName', 'fileSize', 'uploadDateTime', 'relateCurriculum', 'relateAssignment', 'get_relateUser')

        else:
            return ('fileName', 'fileSize', 'uploadDateTime', 'relateCurriculum', 'relateAssignment', 'get_relateUser')

    def _get_list_editable_queryset(self, request, prefix):
        return ('relateCurriculum', 'relateAssignment',)

    search_fields = ['fileName', 'relateCurriculum', 'relateAssignment', 'relateUser']
    ordering = ('-uploadDateTime',)

    @display(ordering="relateUser_id", description="用户")
    def get_relateUser(self, obj):
        # return userInfo.objects.get(user=obj.relateUserInfo).name
        return obj.relateUserInfo.name

    def get_list_display_links(self, request, list_display):
        if request.user.is_superuser:
            return ('fileName')
        else:
            return None

    def get_readonly_fields(self, request, obj=None):
        """不同权限的只读不同"""
        # return ()
        if request.user.is_superuser:
            return ()
        else:
            return ('relateUser',)


    def get_queryset(self, request):  # show data only owned by the user
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        """不同身份返回不同集合"""
        # qs = super(FilesModelAdmin, self).get_queryset(request)

        if request.user.is_superuser:  # admin所有权限
            return FilesModel.objects.all()
        return FilesModel.objects.filter(relateUser=request.user)  # 返回一般用户所有的文件
        # group_names = self.get_group_names(request.user)
        # if request.user.is_superuser or 'hr' in group_names:
        #     return qs
        # return Candidate.objects.filter(
        #     Q(first_interviewer_user=request.user) | Q(second_interviewer_user=request.user))


    def has_change_permission(self, request, obj=None):
        """检查是否有权限查看"""

        has_class_permission = super(FilesModelAdmin, self).has_change_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser and request.user.id != obj.relateUser.id:
            return False
        return True

        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        # if self.value() == '80s':
        #     return queryset.filter(birthday__gte=date(1980, 1, 1),
        #                             birthday__lte=date(1989, 12, 31))
        # if self.value() == '90s':
        #     return queryset.filter(birthday__gte=date(1990, 1, 1),
        #                             birthday__lte=date(1999, 12, 31))


    def download(self, filesmodel, set):
        print(filesmodel, set)
        # TODO: 设置权限区别
        # print(os.path)
        if len(set) > 1:
            filename = "作业批量下载" + datetime.now().strftime('%Y-%m-%d %M%S') + '.zip'
            filePath = 'uploads/' + 'temp.zip'
            with ZipFile(filePath, 'w') as myzip:  # 下载多个文件
                for i in set:
                    # print(i)
                    # os.rename('uploads/' + str(i.file), 'uploads/assignment/' + i.fileName)
                    myzip.write('uploads/assignment/' + i.fileName)
            # time.sleep(2)
        else:
            filePath = "uploads/"+str(set[0])
            filename = set[0].fileName
        response = StreamingHttpResponse(read_file(filePath),
                                         content_type="application/octet-stream",
                                         charset="utf-8")
        response['Content-Disposition'] = 'attachment; filename={}'.format(filename.encode('utf-8').decode('ISO-8859-1'))
        response["Access-Control-Expose-Headers"] = "Content-Disposition"  # 为了使前端获取到Content-Disposition属性

        return response


    # TODO: 构建自定义用户, 满足需求: 登录名19852331, 显示名为姓名
    download.short_description = u'下载选中文件'

    # def get_group_names(self, user):
    #     group_names = []  # 获得组， 以便验证权限
    #     for g in user.groups.all():
    #         group_names.append(g.name)
    #
    #     return group_names
    #
    # def get_readonly_fields(self, request, obj=None):  # 如果是面试官则 只读
    #     group_names = self.get_group_names(request.user)
    #     print(group_names)
    #     if '学生' in group_names:  # 如果是面试官则 只读
    #
    #         logger.info("学生 is in user's group for %s" % request.user.username)
    #         return self.default_list_editable
    #
    #     return ()

    def save_model(self, request, obj, form, change):
        """保存时执行"""
        # print('obj.relateAssignment:', obj.relateAssignment)
        # print('savemode 相关课程', Curriculum.objects.get(assignment__title=obj.relateAssignment))
        # if not change:
        # print(request.POST['file'])
        # print(request.POST)
        obj.relateUser = request.user
        try:
            obj.relateCurriculum = Curriculum.objects.get(assignment__title=obj.relateAssignment)
        except:
            obj.relateCurriculum = None
        obj.save()


# @register(FilesModel)
# class FilesModelAdmin(admin.ModelAdmin):
#     list_display = ('file', 'fileSize', 'uploadDateTime', 'relateUser')
#     list_per_page = 50
#
#     # readonly_fields = ('first_interviewr_user', 'second_interviewer_user',)
#     # def get_readonly_fields(self, request, obj):  # 设置只读
#     #     group_names = self.get_group_names(request.user)
#     #
#     #     if 'interviewer' in group_names:  # 如果是面试官
#     #         logger.info("interviewer is in user's group for %s" % request.user.username)
#     #         return self.default_list_editable
#     #     return ()
#
#     # 需要重写instance_forms方法，此方法作用是生成表单实例
#     def instance_forms(self):
#         super().instance_forms()
#         # 判断是否为新建操作，新建操作才会设置creator的默认值
#         if not self.org_obj:
#             self.form_obj.initial['relateUser'] = self.request.user.id

admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(FilesModel, FilesModelAdmin)
