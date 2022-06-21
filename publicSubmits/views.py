import os
from datetime import datetime

from django.db.models import Count, Aggregate, Avg
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from infoManage.models import Clazz
from userManage.models import userInfo
from .models import Assignment, assgin_status, FilesModel
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from rest_framework.viewsets import ModelViewSet
from publicSubmits import models  # , serializers


# Create your views here.


def publicSubmits(request):
    """首页 及作业规则"""
    def filterFrontData(assObj, status=None):  # 取出特定数据
        data = {}
        data.update({'title': assObj.title,
                     'relateCurriculum': assObj.relateCurriculum,
                     'fileDescribe': assObj.fileDescribe,
                     'fileNameRule': assObj.fileNameRule,
                     'assignmentDescribe': assObj.assignmentDescribe,
                     'deadLine': assObj.deadLine,
                     'status': assgin_status[assObj.status][1] if not status else status,
                     })
        return data

    data = Assignment.objects.order_by('despatchDate')

    # 分类作业， 先按强制指定的<作业状态>分类，最后自动判断<自动状态>
    assForthComing = []
    assComingUp = []
    assCollecting = []
    assStop = []
    for ass in data:
        if ass.status == 1:  # 即将发布
            assForthComing.append(filterFrontData(ass, status=f'已设为{assgin_status[1][1]}'))
        elif ass.status == 2:  # 即将截止
            assComingUp.append(filterFrontData(ass, status=f'已设为{assgin_status[2][1]}'))
        elif ass.status == 3:  # 正在收集
            assCollecting.append(filterFrontData(ass, status=f'已设为{assgin_status[3][1]}'))
        elif ass.status == 4:  # 已经截止
            assStop.append(filterFrontData(ass, status=f'已设为{assgin_status[4][1]}'))
        else:  # ass.status == 0:  # 自动判断作业状态， TODO:需要后端上传时处理是否接受过期的提交。
            # print(ass.deadLine.timestamp())
            # print(datetime.timestamp(datetime.now()))
            # print(f"是否可提交:{ass.deadLine.timestamp() > datetime.timestamp(datetime.now())}")

            # 根据时间分配作业归属
            nowTime = datetime.timestamp(datetime.now())
            deadLine = False if not ass.deadLine else ass.deadLine.timestamp()
            if not ass.deadLine:  # <即将收集>
                assForthComing.append(filterFrontData(ass, status=assgin_status[1][1]))
            elif deadLine > nowTime:
                if (deadLine - nowTime) < 86400:  # 小于一天， <即将截止>
                    assComingUp.append(filterFrontData(ass, status=assgin_status[2][1]))
                else:  # 大于一天， <正在收集>
                    assCollecting.append(filterFrontData(ass, status=assgin_status[3][1]))
            else:  # 大于DDL <停止提交>
                assStop.append(filterFrontData(ass, status=assgin_status[4][1]))
    assignments = []
    for assign in FilesModel.objects.order_by('-uploadDateTime').all():
        try:# TODO: 施工围挡， 之后可以拆掉 2022年4月4日
            assign.relateUser = assign.relateUserInfo.name
        except:
            pass
        assignments.append(assign)
    return render(request, 'Index.html', {
        "assForthComing": assForthComing,
        "assComingUp": assComingUp,
        "assCollecting": assCollecting,
        "assStop": assStop,
        "assignments": assignments,
    })

    # return render(request, 'index.html', {"AssignmentList": ""})


@csrf_exempt
def upload(request):
    """上传文件"""
    # 获取相对路径
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if request.method == 'POST':
        # print('request.POST:', request.POST)
        # print('request.POST[\'title\']:', request.POST['title'])
        # print('request.POST[\'relateCurriculum\']:', request.POST['relateCurriculum'])
        title = request.POST['title']
        relateCurriculum = request.POST['relateCurriculum']
        file = request.FILES.get('file')
        fileName, fileSuffix = file.name.split('.')
        print(fileName, fileSuffix)

        if FilesModel.objects.filter(fileName=file.name):  # 且企图覆盖文件
            print('匿名提交无法覆盖文件')
            message = {}
            message['code'] = 403
            return JsonResponse(message)

        # file_suffix = file.name.split(".")[1]  # 获取文件后缀
        # print('还未验证文件名后缀！：', file_suffix)

        # 更正文件名
        # TODO: 调用登录者的信息
        # login_user = userInfo.objects.get(user__username="19852331")
        login_user = None
        response = HttpResponse()
        response.status_code = 401

        # TODO: 实现前端对于两种上传失败状态的功能
        # 未登录尝试调用本人信息
        if not login_user:  # 未登录
            # 尝试找到
            if len(fileName) > 4:
                # 不知道文件所属，未登录，文件名不对， 返回警告
                response.content = '文件名过长，看起来不像只是你的姓名'
                return response
            else:
                try:
                    login_user = userInfo.objects.get(name=fileName)
                except:
                    response.content = '文件名不是被许可的姓名，因此无法调用你的信息更名'
                    return response

        name = login_user.name  # 匹配数据库的用户 提取关键字
        clazz = login_user.clazz.clazz_brief
        stuNum = login_user.user.username

        # TODO: 暂时没做：保存前检查是否有同名文件，否则（未登录）返回失败
        # 关联作业条目
        relateAssignment = models.Assignment.objects.filter(title=title)[0]
        if relateAssignment.fileNameRule:
            fileName = relateAssignment.fileNameRule \
                           .replace("班级", clazz) \
                           .replace("姓名", name) \
                           .replace("学号", stuNum) \
                       + "." + fileSuffix
            file.name = fileName
        # 保存文件条目
        FilesModel.objects.create(file=file,
                                  fileName=file.name,
                                  relateUserInfo=login_user,
                                  relateCurriculum=models.Curriculum.objects.filter(brief_name=relateCurriculum)[0],
                                  relateAssignment=relateAssignment,
                                  uploadDateTime=datetime.now(),
                                  fileSize=str(round(len(file) / 1024 / 1024, 3)) + "MB")
        message = {"msg": file.name + title + relateCurriculum}
        message['code'] = 200

        return JsonResponse(message)
    # return render(request, 'index.html', {"AssignmentList": ""})


def summarize(request):
    """所有提交汇总页面"""
    # assigFile = FilesModel.objects.values('relateUserInfo')
    # Get all assignment
    assign_lst = Assignment.objects.all()
    # Get all User
    stu_files = []

    userlst = userInfo.objects.all()
    for i in userlst:
        fileLst = FilesModel.objects.filter(relateUserInfo=i.id)
        file_relateAssignment = [i.relateAssignment for i in fileLst]
        # print(f'{i}相关的作业：{len(fileLst)}个', end='\t')
        fileStatus = []
        n = 0
        for ass in assign_lst:
            if ass in file_relateAssignment:
                fileStatus.insert(n, '有')
            else:
                fileStatus.insert(n, '')
            n += 1
        # print(fileStatus)

        stu_files.append({
            'name': i.name,
            'files': fileStatus,
        })

    # 分组查询 出来  每个用户关联的数据组， 不会用
    # a = FilesModel.objects.values_list("relateUser", ).annotate(counts=Count('id'))  # 检测每个用户作业的数量.values("fileName")
    # for i in a:
    #     print(User.objects.get(id=str(i[0])), "作业数量：", i[1])

    return render(request, 'statistical.html', {
        'assign': assign_lst,
        'stu': stu_files
    })
