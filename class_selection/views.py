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
    return render(request, 'index.html', {
        'web_title': '在线选课',
        'page_title': '在线选课',
        'request_user': request.user,
    })


def major_scheme(request):
    #显示页面
    if request.method == 'GET':
        return_dict = {
            'web_title': '培养方案',
            'page_title': '培养方案',
            'request_user': request.user,
            'cur_submodule': 'major_scheme',
        }
        try:
            department_list = Department.objects.all()
        except OperationalError:
            return_dict['info_retrieve_failure'] = True
        else:
            return_dict['department_list'] = department_list
            #print(department_list)
        try:
            major_list = Major.objects.all()
        except OperationalError:
            return_dict['info_retrieve_failure'] = True
        else:
            return_dict['major_list'] =major_list
            #print(major_list)
        try:
            course_list = Course.objects.all()
        except OperationalError:
            return_dict['info_retrieve_failure'] = True
        else:
            return_dict['course_list'] = course_list
            #print(course_list)
        return render(request, 'major_scheme.html', return_dict)

    elif request.method == 'POST':
        return_dict = {
            'web_title': '培养方案',
            'page_title': '培养方案',
            'request_user': request.user,
            'cur_submodule': 'major_scheme',
        }

        if request.POST.get('dept'):#点击第一个下拉框，第二个下拉框会筛选major信息
            department_list = Department.objects.filter(id=request.POST.get('dept'))
            return_dict['department_list'] = department_list
            major_list = Major.objects.filter(department=department_list[0])
            return_dict['major_list'] = major_list
            return_dict['selected_dept'] = int(request.POST.get('dept'))
            return render(request, 'major_scheme.html', return_dict)

        else:#点击查看培养方案，重置两个下拉框内容并返回培养方案内课程表及课程信息
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
            mymajor = request.POST.get("major")
            if mymajor != None:
                try:
                    major_ret = MajorHasCourse.objects.filter(major = int(mymajor))
                except OperationalError:
                    return_dict['info_retrieve_failure'] = True
                else:
                    course_info = []
                    for i in range(0, len(major_ret)):
                        try:
                            course_ret = Course.objects.filter(id =major_ret[i].course_id)
                        except OperationalError:
                            return_dict['info_retrieve_failure'] = True
                        else:
                            course_info += course_ret
                    print(course_info)
                return_dict["course_list"] = course_info
                return_dict["major_name"] = Major.objects.filter(id = int(mymajor))[0].name
                return render(request, 'major_scheme.html', return_dict)
            else:
                return HttpResponseRedirect('/class_selection/major_scheme')


def stu_select(req):
    return render(req, 'stu_select.html', {
        'web_title': '课程选择',
        'page_title': '课程选择',
        'request_user': req.user,
    })


def admin_class(req):
    if req.method == 'GET':
        return render(req, 'admin_class.html', {
            'web_title': '手动选课',
            'page_title': '手动选课',
            'request_user': req.user,
        })


def time_control(req):
    if req.method == 'GET':
        return render(req, 'time_control.html', {
            'web_title': '管理时间',
            'page_title': '管理时间',
            'request_user': req.user,
        })


def stu_class(req):
    return render(req, 'stu_class.html', {
        'web_title': '学生课表',
        'page_title': '学生课表',
        'request_user': req.user,
    })


def tea_class(request):
    current_user_id = request.user.groups.first()
    if request.method == 'GET':
        return_dict = {'web_title': '教师课表',
                       'page_title': '教师课表',
                       'request_user': request.user,
                       'cur_submodule': 'tea_class', }
        try:
            course_list = Course.objects.all()
        except OperationalError:
            return_dict['info_retrieve_failure'] = True
        else:
            return_dict['course_list'] = course_list

        return render(request, 'tea_class.html', return_dict)
