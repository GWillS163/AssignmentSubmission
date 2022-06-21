# Generated by Django 4.0.1 on 2022-03-02 09:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('infoManage', '0002_alter_curriculum_id'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('userManage', '0006_alter_userinfo_recentlogintime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='clazz',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='infoManage.clazz', verbose_name='班级'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='describe',
            field=models.TextField(blank=True, default=None, max_length=200, null=True, verbose_name='描述'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='name',
            field=models.CharField(default=None, max_length=20, null=True, verbose_name='姓名'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='关联用户'),
        ),
    ]