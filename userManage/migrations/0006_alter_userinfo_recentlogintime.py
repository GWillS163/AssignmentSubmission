# Generated by Django 4.0.1 on 2022-03-02 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userManage', '0005_rename_student_userinfo_delete_professor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='recentLoginTime',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
