from django.db.models import Count, Aggregate
from django.shortcuts import render
from publicSubmits.models import Assignment, FilesModel

# Create your views here.
from userManage.models import userInfo


def backstage(request):
    """老师下载，观看统计的后台"""
    assign_file_data = []
    assign_lst = Assignment.objects.all()
    for assign_item in assign_lst:

        assign_file_data.append(
            dict(assign_obj=assign_item.title,
                 summbit_stu_list=userInfo.objects.filter(relateUser__relateAssignment=assign_item).distinct(),
                 unsummbit_stu_list=userInfo.objects.all().exclude(relateUser__relateAssignment=assign_item)))
    return render(request, "backstage.html",
                  {
                      "assign_file_data": assign_file_data,
                  })
