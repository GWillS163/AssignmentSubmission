# from django.contrib import admin
# from xml.etree.ElementInclude import
# from django.conf.global_settings import MEDIA_ROOT
from django.views.generic.base import RedirectView

# from AssignmentSubmission.settings import MEDIA_ROOT
from django.template.defaulttags import url
from django.urls import include, path, re_path
from django.views.static import serve

from infoManage import views

urlpatterns = [
    # re_path(r"^$", views.publicSubmits),
    path(r'backstage/', views.backstage),
    # path(r"uploads/", views.uploads_bg),
    # re_path(r'^uploads/(?P<path>.*)$',  serve, {"document_root": MEDIA_ROOT}),
    # path(r"uploads/", views.submitfile),
    # path(r"", views.Assignment_list),
]

