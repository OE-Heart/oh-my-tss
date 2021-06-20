from django.http.response import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.http.request import HttpRequest
from django.contrib.auth import authenticate
from django.contrib import admin
from .models import Classroom, ClassHasRoom, Application, Building
from info_mgt.models import Campus, Department, Major, Teacher, Course, MajorHasCourse, Class
from django.urls import reverse
# TODO: 所有的函数在最前面都要有用户身份验证。


def index(request):
    return render(request, 'add_room.html')


def add_room(request):  # 打开添加教室的页面
    if request.method == 'GET':
        return_dic = {'web_title': '添加教室',
                      'page_title': '添加教室',
                      'request_user': request.user,
                      'cur_submodule': 'add_room'}
        return render(request, 'add_room.html', return_dic)


def add_room_submit(request):  # 提交添加教室的信息
    if request.method == 'POST':
        # TODO: 在数据库增加新的教室记录
        return HttpResponseRedirect(reverse('add_room'))


def modify_room(request):  # 打开修改教室页面
    if request.method == 'GET':
        return_dic = {'web_title': '修改教室信息',
                      'page_title': '修改教室信息',
                      'request_user': request.user,
                      'cur_submodule': 'modify_room'}
        if request.GET.get('delete_success'):
            return_dic['delete_room_successfully'] = True
        elif request.GET.get('delete_failure'):
            return_dic['delete_room_failed'] = True
        # TODO: 从数据库中查询全部的教室信息并将查询结果（集合）放入return_dic中
        return render(request, 'modify_room.html', return_dic)


def modify_certain_room(request, room_id): # 修改特定教室信息的页面
    if request.method == 'GET':
        return_dic = {'web_title': '修改教室信息',
                      'page_title': '修改教室信息',
                      'request_user': request.user,
                      'cur_submodule': 'modify_room'}
        # TODO: 从数据库把要修改的这一条元组（一个教室类的对象）拿出来并放入return_dic中
        return render(request, 'modify_certain_room.html', return_dic)


def modify_room_submit(request, room_id):  # 提交修改的教室信息
    if not room_id:
        return Http404  # 必须在url中给出教室编号
    if request.method == 'POST':
        # TODO: 把room_id对应的教室元组的属性值按照得到的参数值修改
        return HttpResponseRedirect(reverse('modify_room'))


def delete_room(request, room_id):
    if not room_id:
        return Http404
    # TODO: 从数据库删掉对应的教室并且根据删除是否成功来给重定向的链接加上不同的参数
    success = '?delete_success=true'
    failure = '?delete_failure=true'
    return HttpResponseRedirect(reverse('modify_room') + success)


def auto_schedule(request):   # 打开自动排课页面
    if request.method == 'GET':
        return_dic = {'web_title': '自动排课',
                      'page_title': '自动排课',
                      'request_user': request.user,
                      'cur_submodule': 'auto_schedule'}
        return render(request, 'auto_schedule.html', return_dic)


def do_auto_schedule(request):  # 进行自动排课。。。麻烦（（（
    return HttpResponseRedirect(reverse('auto_schedule'))


def manipulate_schedule(request):   # 打开手动调课页面
    if request.method == 'GET':
        return_dic = {'web_title': '手动课程调整',
                      'page_title': '手动课程调整',
                      'request_user': request.user,
                      'cur_submodule': 'manipulate_schedule'}
        return render(request, 'manipulate_schedule.html', return_dic)


def manipulate_certain_class(request, class_id):   # 打开处理特定课程的页面
    if request.method == 'GET':
        return_dic = {'web_title': '手动课程调整',
                      'page_title': '手动课程调整',
                      'request_user': request.user,
                      'cur_submodule': 'manipulate_schedule'}
        return render(request, 'manipulate.html', return_dic)


def submit_manipulate(request, class_has_room_id):  # 提交手动调课（针对一个时段）
    if not class_has_room_id:
        return Http404
    if request.method == 'POST':
        pass


def application(request):  # 打开提出调课申请页面
    if request.method == 'GET':
        return_dic = {'web_title': '提出调课申请',
                      'page_title': '提出调课申请',
                      'request_user': request.user,
                      'cur_submodule': 'application'}
        return render(request, 'app_init.html', return_dic)


def submit_application(request):  # 提交调课申请
    if request.method == 'POST':
        return HttpResponseRedirect(reverse('application'))


def handle_application(request):  # 打开处理调课申请页面
    if request.method == 'GET':
        return_dic = {'web_title': '处理调课申请',
                      'page_title': '处理调课申请',
                      'request_user': request.user,
                      'cur_submodule': 'handle_application'}
        return render(request, 'handle_application.html', return_dic)


def handle_certain_application(request, application_id):  # 打开一条特定的申请的处理页面
    if request.method == 'GET':
        return_dic = {'web_title': '处理调课申请',
                      'page_title': '处理调课申请',
                      'request_user': request.user,
                      'cur_submodule': 'handle_application'}
        return render(request, 'process.html', return_dic)


def submit_handle(request, application_id):  # 提交申请处理结果
    if not application_id:
        return Http404
    if request.method == 'POST':
        pass


def teacher_class(request):   # 按教师查询课表页面
    if request.method == 'GET':  # 获取3个查询条件
        teacher = request.GET.get('teacher_id')
        year = request.GET.get('year')
        term = request.GET.get('term')


def room_class(request):
    if request.method == 'GET':  # 获取2个查询条件
        year = request.GET.get('year')
        term = request.GET.get('term')
