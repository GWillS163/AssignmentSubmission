import csv

from django.core.management import BaseCommand
from userManage.models import userInfo, Clazz
from django.contrib.auth.models import User


# python manage.py import_class --path
class Command(BaseCommand):
    help = '从一个csv文件的内容中读取班级人员列表,格式为[\'姓名,班级,学号\'] 导入到数据库中'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        with open(path, 'rt', encoding='GBK') as f:
            reader = csv.reader(f, dialect='excel', delimiter=',')
            for row in reader:
                print(row[0], row[1], row[2])
                try:
                    current_user = User.objects.get(username=row[2])
                    current_user.first_name = row[0][1:]
                    current_user.last_name = row[0][0]
                    current_user.save()
                except:
                    pass
                    current_user = User.objects.create_user(
                        username=row[2],
                        email=f"{row[2]}@czjtu.edu.cn",
                        password=row[2]+row[2],  # TODO: 后续改密码给邮箱发邮件再说
                    )
                try:
                    current_clazz = Clazz.objects.get(clazz_num=row[1])
                except:
                    current_clazz = Clazz.objects.create(clazz_num=row[1],
                                                 )
                try:
                    candidate = userInfo.objects.create(
                        user=current_user,
                        name=row[0],
                        clazz=current_clazz,
                        describe="Auto_created")
                except Exception as E:
                    print(current_user, E)
                # print(candidate)
