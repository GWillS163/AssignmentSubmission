from django.contrib import admin

# Register your models here.
from django.db import models
from django.forms import Textarea

from .models import Professor, Clazz
from publicSubmits.models import Curriculum


class CurriculumAdmin(admin.ModelAdmin):
    list_display = ('brief_name',  'professor', 'full_name')
    list_display_links = ('brief_name', )


class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'clazz', 'gender',)
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 25})},
    }


class ClazzAdmin(admin.ModelAdmin):
    list_display = ('clazz_brief', 'faculty', 'specialist', 'clazz_num', )


admin.site.register(Curriculum, CurriculumAdmin)
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(Clazz, ClazzAdmin)
