# Generated by Django 4.0.1 on 2022-02-20 11:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, verbose_name='作业简称')),
                ('file_type', models.CharField(blank=True, help_text='一般为.pdf .doc .docx 这些文件', max_length=20, null=True, verbose_name='允许文件类型')),
                ('despatchDate', models.DateTimeField(auto_now=True, verbose_name='发布时间')),
                ('courseName', models.CharField(blank=True, max_length=20, verbose_name='课程')),
                ('assginName', models.CharField(blank=True, max_length=20, verbose_name='作业名规则')),
                ('describe', models.TextField(blank=True, max_length=200, verbose_name='作业描述')),
                ('deadLine', models.DateTimeField(blank=True, default='', help_text='默认空值为<即将收集>的作业', max_length=200, null=True, verbose_name='提出期限')),
                ('status', models.IntegerField(blank=True, choices=[(0, '按DDL自动判断'), (1, '尚未募集'), (2, '即将截止'), (3, '正在募集'), (4, '已经截止')], default=0, help_text='建议为默认值，过期则不显示收集。指定状态后则不受<提出日期>的限制，手动开放或关闭收集', verbose_name='强制作业状态')),
            ],
            options={
                'verbose_name_plural': '作业收集规则',
            },
        ),
        migrations.CreateModel(
            name='Curriculum',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='id')),
                ('full_name', models.CharField(blank=True, default='', max_length=20, null=True, verbose_name='课程完整名')),
                ('brief_name', models.CharField(max_length=20, verbose_name='课程简名')),
            ],
            options={
                'verbose_name_plural': '课程管理',
            },
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='暂无老师', max_length=20, null=True, verbose_name='课程完整名')),
                ('clazz', models.CharField(blank=True, max_length=30, null=True, verbose_name='教授班级')),
                ('description', models.TextField(blank=True, help_text='填写办公室信息，邮箱电话等', max_length=200, null=True, verbose_name='描述')),
            ],
        ),
        migrations.CreateModel(
            name='FilesModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='id')),
                ('file', models.FileField(upload_to='uploads/')),
                ('uploadDateTime', models.DateTimeField(auto_now=True, verbose_name='上传时间')),
                ('fileSize', models.CharField(blank=True, max_length=20, verbose_name='文件大小')),
                ('relateAssignment', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='publicSubmits.assignment', verbose_name='所属作业')),
                ('relateCurriculum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='publicSubmits.curriculum', verbose_name='所属课程')),
                ('relateUser', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='所属用户')),
            ],
            options={
                'verbose_name_plural': '作业提交',
                'db_table': 'files_storage',
            },
        ),
        migrations.AddField(
            model_name='curriculum',
            name='professor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='教授', to='publicSubmits.professor'),
        ),
    ]
