from django.db import OperationalError
from django.http.request import HttpRequest
from django.http.response import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from class_selection import forms
from class_selection.forms import Department, Major
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from info_mgt.models import Campus, Department, Major, Teacher, Course, MajorHasCourse, Class


# TODO: those following pages' templates are not implemented yet.

def index(request):
    return render(request, 'major_scheme.html')


def major_scheme(request):
    current_user_group = request.user.groups.first()
    if not current_user_group or current_user_group.name != 'admin':
        return HttpResponseRedirect(reverse('login'))
    if request.method == 'GET':
        return_dict = {'web_title': '培养方案',
                       'page_title': '培养方案',
                       'request_user': request.user,
                       'cur_submodule': 'major_scheme', }
        try:
            department_list = Department.objects.all()
        except OperationalError:
            return_dict['info_retrieve_failure'] = True
        else:
            return_dict['department_list'] = department_list
        try:
            major_list = Major.objects.all()
        except OperationalError:
            return_dict['info_retrieve_failure'] = True
        else:
            return_dict['major_list'] = major_list
        try:
            course_list = Course.objects.all()
        except OperationalError:
            return_dict['info_retrieve_failure'] = True
        else:
            return_dict['course_list'] = course_list
        return render(request, 'major_scheme.html', return_dict)


def stu_select(req):
    return render(req, 'stu_select.html', {
        'web_title': '课程选择',
        'page_title': '课程选择',
        'request_user': req.user,
    })


def admin_class(req):
    return render(req, 'admin_class.html', {
        'web_title': '管理员界面',
        'page_title': '管理员界面',
        'request_user': req.user,
    })


def stu_class(req):
    return render(req, 'stu_class.html', {
        'web_title': '学生课表',
        'page_title': '学生课表',
        'request_user': req.user,
    })


def tea_class(request):
    if request.method == 'GET':
        return_dict = {'web_title': '教师课表',
                       'page_title': '教师课表',
                       'request_user': request.user,
                       'cur_submodule': 'tea_class', }
        try:
            course_list =Course.objects.all()
        except OperationalError:
            return_dict['info_retrieve_failure'] = True
        else:
            return_dict['course_list'] = course_list

        return render(request, 'tea_class.html', return_dict)
