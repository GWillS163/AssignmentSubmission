"""AssignmentSubmission URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.template.defaulttags import url
from django.urls import path, include, re_path
# from Assignment.views import Assignment_list
from django.views.generic.base import RedirectView

urlpatterns = [
    # path('grappelli', include('grappelli.urls')),
    # path('storage/', include('publicSubmits.urls')),

    re_path(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico')),
    path("", include("publicSubmits.urls")),
    path("publicSubmits/", include("publicSubmits.urls")),
    path("manage/", include("infoManage.urls")),
    # path('api/upload/', views.upload),
    path('admin/', admin.site.urls),
    # path('favicon.ico', serve,
    #                    {'path': 'images/favicon.ico', 'document_root': os.path.join(settings.BASE_DIR, "static")}),
]
admin.site.site_header = '駿清清作业管理系统'