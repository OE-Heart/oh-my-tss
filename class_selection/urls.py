"""class_selection URL Configuration

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
from django.urls import path
from django.views import generic
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('major_scheme/', views.major_scheme),
    path('stu_class/', views.stu_class),
    path('tea_class/', views.tea_class, name='tea_class'),
    path('time_control/', views.time_control),
    path('admin_class/', views.admin_class),
    path('stu_select/', views.stu_select,name="stu_select"),
    path('tea_class/detail/<str:class_id>', views.stu_detail, name='stu_display'),
    path('stu_select/choose_class', views.choose_class, name='choose_class'),
    path('stu_class_list/', views.stu_class_list, name='stu_class_list'),
]
