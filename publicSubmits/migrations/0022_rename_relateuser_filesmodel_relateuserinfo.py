# Generated by Django 4.0.1 on 2022-04-04 14:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publicSubmits', '0021_remove_filesmodel_relateuserinfo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='filesmodel',
            old_name='relateUser',
            new_name='relateUserInfo',
        ),
    ]
