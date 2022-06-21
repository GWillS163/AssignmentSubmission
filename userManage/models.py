from django.db import models
from django.contrib.auth.models import User
from infoManage.models import Clazz, Curriculum


class userInfo(models.Model):
    """学号为用户名"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="关联用户")
    name = models.CharField(max_length=20, default=None, null=True, blank=False, verbose_name="姓名")
    describe = models.TextField(max_length=200, default=None, null=True, blank=True, verbose_name="描述")
    # 学生选班级
    clazz = models.ForeignKey(Clazz, on_delete=models.CASCADE, default=None, null=True, blank=True, verbose_name="班级")
    # clazz = models.gr
    # 老师选教授班级 实现不了
    # teachClazz = models.ManyToOneRel(Clazz, to="clazz_brief", field_name="clazz_brief")
    # teachClazz = forms.ModelMultipleChoiceField(queryset=Clazz.objects.all(),
    #                                             required=False,
    #                                             widget=FilteredSelectMultiple("Groups", is_stacked=False))
    # teachCurriculum = forms.ModelMultipleChoiceField(queryset=Curriculum.objects.all(),
    #                                                  required=False,
    #                                                  widget=FilteredSelectMultiple("Groups", is_stacked=False))

    registredTime = models.DateTimeField(auto_now=True)
    # TODO: 未做
    recentLoginTime = models.DateTimeField(blank=True, null=True, verbose_name="最近登录")

    def __str__(self):
        return self.name

# from django.contrib.auth.models import AbstractUser
#
# class UserProfile(AbstractUser):
#     nick_name = models.CharField(max_length=50, verbose_name=u'昵称')
#     birthday = models.DateField(verbose_name=u'生日', null=True, blank=True)
#     gender = models.CharField(max_length=10, choices=(("male", u'男'), ("female", u'女')), default='female')
#     address = models.CharField(max_length=11, verbose_name=u'地址', null=True, blank=True)
#     # image = models.ImageField(upload_to='image/%Y/%m', default=u"image/default.png", max_length=100)
#     phone = models.CharField(max_length=11, verbose_name=u"手机号码", null=True, blank=True)
#     # image依赖Pillow
#
#     class Meta:
#         verbose_name = u"用户信息"
#         verbose_name_plural = verbose_name
#
#     def __unicode__(self):
#         return self.username