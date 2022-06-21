from django.db import models

# Create your models here.


class Clazz(models.Model):
    faculty = models.CharField(max_length=20, blank=False, null=False, verbose_name='系别', help_text="信息技术与计算机系")
    specialist = models.CharField(max_length=20, blank=False, null=False, verbose_name='专业', help_text="例:软件工程")
    clazz_num = models.CharField(max_length=20, blank=False, null=False, verbose_name='数字班号', help_text="例:1909")
    clazz_brief = models.CharField(max_length=20, blank=False, null=False, verbose_name='简称', help_text="例:软件1909班")

    class Meta:
        verbose_name = '班级'
        verbose_name_plural = "班级管理"

    def __str__(self):
        return self.clazz_brief


class Professor(models.Model):
    """教授数据 可以不与账户关联"""
    # id = models.AutoField(primary_key=True, verbose_name="id")
    # name = models.CharField(max_length=20, blank=True, null=True, default="暂无老师", verbose_name="课程完整名")
    # TODO:clazz = models.ForeignKey()
    clazz = models.CharField(max_length=30, blank=True, null=True, verbose_name="教授班级")
    description = models.TextField(max_length=200, blank=True, null=True, verbose_name="描述", help_text="填写办公室信息，邮箱电话等")

    name = models.CharField(max_length=25, verbose_name='姓名')
    gender_choices = (
        (1, '男'),
        (2, '女')
    )
    gender = models.IntegerField(choices=gender_choices, blank=True, null=True, verbose_name='性别')

    class Meta:
        # db_table = 'Teacher'
        verbose_name = '教师'
        verbose_name_plural = "教师管理"

    def __str__(self):
        return self.name


class Curriculum(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="id")
    full_name = models.CharField(max_length=20, blank=True, null=True, default="", verbose_name="课程完整名")
    brief_name = models.CharField(max_length=20, blank=False, null=False, verbose_name="课程简名")
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE,blank=True, null=True, related_name="教授")

    class Meta:
        verbose_name_plural = u'课程管理'
        # ordering = ['-id']

    def __str__(self):
        return self.brief_name

