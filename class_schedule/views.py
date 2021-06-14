from django.http.response import HttpResponse
from django.shortcuts import render
from django.http.request import HttpRequest
from django.contrib.auth import authenticate
from django.http.response import Http404, HttpResponse
from .models import Classroom, ClassHasRoom, Application, Building
from info_mgt.models import Campus, Department, Major, Teacher, Course, MajorHasCourse, Class


def index(request):
    return HttpResponse('Still under construction.')   # 这句话是用来占位的，到时候用我们实际的页面替换


def add_room(request):  # 打开添加教室的页面
    if request.method == 'GET':
        pass


def add_room_submit(request):  # 提交添加教室的信息
    if request.method == 'POST':
        pass


def modify_room(request): # 打开修改教室页面
    if request.method == 'GET':
        pass


def modify_room_submit(request, room_id):  # 提交修改的教室信息
    if not room_id:
        return Http404  # 必须在url中给出教室编号
    if request.method == 'POST':
        pass


def auto_schedule(request):   # 打开自动排课页面
    if request.method == 'GET':
        pass


def do_auto_schedule(request):  # 进行自动排课。。。麻烦（（（
    pass


def manipulate_schedule(request):   # 打开手动调课页面
    if request.method == 'GET':
        pass


def submit_manipulate(request, class_has_room_id):  # 提交手动调课（针对一个时段）
    if not class_has_room_id:
        return Http404
    if request.method == 'POST':
        pass


def application(request):  # 打开提出调课申请页面
    if request.method == 'GET':
        pass


def submit_application(request):  # 提交调课申请
    if request.method == 'POST':
        pass


def handle_application(request):  # 打开处理调课申请页面
    if request.method == 'GET':
        pass


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
