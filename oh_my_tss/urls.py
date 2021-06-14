"""oh_my_tss URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.shortcuts import render
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from material.frontend import urls as frontend_urls

from info_mgt import views as info_mgt_views

def landing(req):
    return render(req, 'skeleton.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing, name="landing"),
    path('', include(frontend_urls)),
    path('login/', info_mgt_views.login_view, name="login"),
    path('logout/', info_mgt_views.logout_view, name="logout"),
    path('info_mgt/', include('info_mgt.urls'), name="信息管理"),
    path('class_schedule', include('class_schedule.urls'), name="课程安排"),
    path('online_exam/', include('online_exam.urls'), name="在线测验")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
