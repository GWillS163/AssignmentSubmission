from django import forms
from django.contrib import admin
from django.contrib.admin import display
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from infoManage.models import Clazz
from .models import userInfo


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton


class UserInline(admin.StackedInline):
    model = userInfo
    can_delete = False
    verbose_name_plural = 'user'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    """困扰已久的 外键字段排序搞懂了"""
    inlines = (UserInline,)
    list_display = ("name", "clazz", "username", "email", "last_login",)
    list_display_links = ["name"]

    def name(self, obj):
        return userInfo.objects.get(user=obj).name
    name.short_description = '姓名'

    @display(ordering='userinfo__clazz', description='班级')
    def clazz(self, obj):
        return userInfo.objects.get(user=obj).clazz



class UserInfoAdmin(admin.ModelAdmin):
    # inlines = (UserInline,)
    list_display = ("name",)
    # list_display_links = ("username", )


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(userInfo, UserInfoAdmin)

#
# from xadmin.plugins.auth import UserAdmin
#
#
# class UserProfileAdmin(UserAdmin):
#     pass
