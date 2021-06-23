import pymysql
from django.db import OperationalError
from django.http.request import HttpRequest
from django.http.response import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from class_selection import forms
from class_selection import models
from class_selection.forms import Department, Major
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from info_mgt.models import Campus, Department, Major, Teacher, Course, MajorHasCourse, Class


# TODO: those following pages' templates are not implemented yet.

def index(request):
    return render(request, 'major_scheme.html')


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
    current_user_id = request.user.groups.first()
    if request.method == 'GET':
        return_dict = {'web_title': '教师课表',
                       'page_title': '教师课表',
                       'request_user': request.user,
                       'cur_submodule': 'tea_class', }
        try:
            class_list = models.Class.objects.filter(teacher=request.user.id)
        except OperationalError:
            return_dict['info_retrieve_failure'] = True
        else:
            return_dict['class_list'] = class_list

        return render(request, 'tea_class.html', return_dict)


def stu_detail(req, class_id):
    return_dict = {'web_title': '学生详情',
                   'page_title': '学生详情',
                   }
    students_list = models.StuHasClass.objects.filter(Class=class_id)
    print(students_list)
    return_dict['students_list'] = students_list
    return render(req, 'stu_detail.html', return_dict)


def major_scheme(request):
    return_dict = {
        'web_title': '培养方案',
        'page_title': '培养方案',
        'request_user': request.user,
        'cur_submodule': 'major_scheme',
    }
    if request.method == 'GET':
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
    elif request.method == 'POST':
        mymajor = request.POST.get("major")
        if mymajor != "":
            conn = pymysql.connect(host='43.129.73.191', port=3306, user='fse', passwd='xkxqjdTVgZRfjV2t', db='fse')
            cursor = conn.cursor()
            cursor.execute("select id from info_mgt_major where name ='%s'" % (mymajor))
            major_ret = cursor.fetchall()  # major_ret是已选专业的id
            cursor.execute("select * from info_mgt_majorhascourse where major_id = %d" % (major_ret[0]))
            course_ret = cursor.fetchall()
            return_dict["course_list"] = course_ret
            return render(request, 'major_scheme.html', return_dict)

        else:
            return_dict["Not_Valid_Param"] = '1'
            return render(request, 'major_scheme.html', return_dict)
    else:
        return render(request, 'major_scheme.html', return_dict)
