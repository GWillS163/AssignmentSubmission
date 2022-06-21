# Generated by Django 4.0.1 on 2022-02-20 13:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('publicSubmits', '0008_assignment_relatecurriculum_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filesmodel',
            name='relateUser',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='entries', to=settings.AUTH_USER_MODEL, verbose_name='所属用户'),
        ),
    ]
