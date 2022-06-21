import datetime

from django.contrib import admin
from django.contrib.admin import register
from django.db import models
from django.conf import settings

# Create your models here.
from django.contrib.auth.models import User
from infoManage.models import Curriculum
from userManage.models import userInfo

file_type_lst = [(0, '.pdf'),
                 (1, '.doc'),
                 (2, '.docx')]
assgin_status = [
    (0, "按DDL自动判断"),
    (1, "尚未募集"),
    (2, "即将截止"),
    (3, "正在募集"),
    (4, "已经截止"),
]


class Assignment(models.Model):
    # print()
    id = models.AutoField(primary_key=True, blank=True, null=False, auto_created=True)
    title = models.CharField(blank=False, max_length=20, verbose_name="作业简称")
    fileNameRule = models.CharField(blank=True, max_length=20, verbose_name="作业名规则", help_text='保留字(班级,学号,姓名)会被替换为学生信息')
    assignmentDescribe = models.TextField(blank=True, max_length=200, verbose_name="作业描述")
    fileDescribe = models.CharField(blank=True, max_length=20, null=True, help_text="一般为.pdf .doc .docx 这些文件", verbose_name="文件要求")
    deadLine = models.DateTimeField(blank=True, null=True, default="", max_length=200, help_text="默认空值为<即将收集>的作业", verbose_name="提出期限")
    status = models.IntegerField(blank=True, choices=assgin_status, default=0, help_text="建议为默认值，过期则不收集。", verbose_name="作业状态")

    despatchDate = models.DateTimeField(auto_now=True, verbose_name="发布时间")
    relateCurriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE, null=True, default=None, blank=True,
                                         verbose_name="所属课程")
    courseName = models.CharField(blank=True, max_length=20, verbose_name="课程")

    class Meta:
        verbose_name = u'作业规则'
        verbose_name_plural = u'作业收集提交'

    def __str__(self):
        return self.title


class FilesModel(models.Model):  # models.Model):
    """作业的文件模型"""

    id = models.AutoField(primary_key=True, verbose_name="id")
    file = models.FileField(upload_to='assignment/', verbose_name="文件下载", )
    fileName = models.CharField(max_length=40, blank=False, null=True, default=None, verbose_name="文件名")
    uploadDateTime = models.DateTimeField(auto_now=True, verbose_name="上传时间")
    fileSize = models.CharField(max_length=20, blank=True, verbose_name="文件大小")

    relateCurriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE, null=True, default=None, blank=True, verbose_name="所属课程")
    relateAssignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, null=True, default=None, blank=True, verbose_name="所属作业")
    # relateUser = models.ForeignKey(User, related_name='FilesModel', on_delete=models.CASCADE, null=True, blank=False, verbose_name="所属用户")
    relateUserInfo = models.ForeignKey(userInfo, related_name="relateUser", on_delete=models.PROTECT, null=True, default=None, blank=True, verbose_name="所属用户(旧)")
    # relateUserInfo = models.ForeignKey(userInfo, on_delete=models.CASCADE, null=True, default=None, blank=True, verbose_name="所属用户")
    # relateUser = models.ForeignKey(userInfo, on_delete=models.CASCADE, null=True, default=None, blank=True, verbose_name="所属用户")
    class Meta:
        verbose_name = u'提交文件'
        verbose_name_plural = u'提交文件管理'
        db_table = 'files_storage'
        # ordering = ['-id']

    def __str__(self):
        return self.file.name

    def instance_forms(self):
        pass

