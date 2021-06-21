from django.db import OperationalError, transaction
from django.http.response import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render
from django.http.request import HttpRequest
from django.contrib.auth.models import User, Group
from .models import Classroom, ClassHasRoom, Application, Building
from info_mgt.models import Campus, Department, Major, Teacher, Course, MajorHasCourse, Class
from django.urls import reverse
from django.db.models import Q


def index(request):
    return render(request, 'add_room.html')


def add_room(request):  # 打开添加教室的页面
    current_user_group = request.user.groups.first()
    if not current_user_group or current_user_group.name != 'admin':
        return HttpResponseRedirect(reverse('login'))
    return_dict = {'web_title': '添加教室',
                   'page_title': '添加教室',
                   'request_user': request.user,
                   'cur_submodule': 'add_room', }
    try:
        campus_list = Campus.objects.all().order_by('id')
    except OperationalError:
        return_dict['info_retrieve_failure'] = True
    else:
        return_dict['campus_list'] = campus_list
        try:
            if request.method == 'GET':
                building_list = Building.objects.filter(campus_id=campus_list.first().id)
            elif request.method == 'POST':
                building_list = Building.objects.filter(campus_id=request.POST.get('campus'))
                return_dict['selected_campus'] = int(request.POST.get('campus'))
        except OperationalError:  # 捕捉数据库操作的异常
            return_dict['info_retrieve_failure'] = True
        else:
            return_dict['building_list'] = building_list
    if request.GET.get('succeeded'):  # 之前有教室添加成功
        return_dict['add_success'] = True
    elif request.GET.get('failed'):  # 之前教室因为其他原因添加失败
        return_dict['add_failure'] = True
    elif request.GET.get('duplicated'):  # 之前教室因为门牌号重复而添加失败
        return_dict['info_retrieve_failure'] = True
    return render(request, 'add_room.html', return_dict)


def add_room_submit(request):  # 提交添加教室的信息
    current_user_group = request.user.groups.first()
    if not current_user_group or current_user_group.name != 'admin':
        return HttpResponseRedirect(reverse('login'))
    if request.method == 'POST':
        # room_campus_id = request.POST.get('campus')
        room_building_id = request.POST.get('building')
        room_number = request.POST.get('room_id')
        room_type = request.POST.get('room_type')
        room_capacity = request.POST.get('room_capacity')
        try:
            duplicate_check = Classroom.objects.get(building_id=room_building_id, room_number=room_number)
        except Classroom.DoesNotExist:
            pass
        else:
            if duplicate_check:
                return HttpResponseRedirect(reverse('add_room') + '?duplicated=true')
        new_room = Classroom(building_id=room_building_id, room_number=room_number, type=room_type,
                             capacity=room_capacity)
        try:
            new_room.save()
        except OperationalError:
            return HttpResponseRedirect(reverse('add_room') + '?failed=true')
        else:
            return HttpResponseRedirect(reverse('add_room') + '?succeeded=true')


def modify_room(request, page=0):  # 打开修改教室页面
    current_user_group = request.user.groups.first()
    if not current_user_group or current_user_group.name != 'admin':
        return HttpResponseRedirect(reverse('login'))
    if request.method == 'GET':
        return_dict = {'web_title': '修改教室信息',
                       'page_title': '修改教室信息',
                       'request_user': request.user,
                       'cur_submodule': 'modify_room'}
        if request.GET.get('delete_success'):
            return_dict['delete_room_successfully'] = True
        elif request.GET.get('delete_failure'):
            return_dict['delete_room_failed'] = True
        try:
            room_list = Classroom.objects.all()[page * 10: page * 10 + 10]
        except OperationalError:
            return_dict['info_retrieve_failure'] = True
        else:
            page_sum = len(room_list) // 10 + 1
            if page >= page_sum:
                return HttpResponse(404)
            return_dict['room_list'] = room_list
            return_dict['cur_page'] = page + 1
            return_dict['prev_page'] = (page - 1)
            return_dict['prev_disabled'] = (page == 0)
            return_dict['next_page'] = page + 1
            return_dict['next_disabled'] = (page + 1 >= page_sum)
            return_dict['page_sum'] = page_sum
        if request.GET.get('success'):
            return_dict['modify_succeeded'] = True
        elif request.GET.get('failure'):
            return_dict['modify_failed'] = True
        elif request.GET.get('duplication'):
            return_dict['duplicated'] = True
        elif request.GET.get('no_such_room'):
            return_dict['no_such_room'] = True
        return render(request, 'modify_room.html', return_dict)


def modify_certain_room(request, room_id):  # 修改特定教室信息的页面
    current_user_group = request.user.groups.first()
    if not current_user_group or current_user_group.name != 'admin':
        return HttpResponseRedirect(reverse('login'))
    return_dict = {'web_title': '修改教室信息',
                   'page_title': '修改教室信息',
                   'request_user': request.user,
                   'cur_submodule': 'modify_room'}
    try:
        room_to_modify = Classroom.objects.get(pk=room_id)
    except OperationalError:
        return_dict['info_retrieve_failure'] = True
    except Classroom.DoesNotExist:
        return HttpResponseRedirect(reverse('modify_room') + '?no_such_room=true')
    else:
        return_dict['original_info'] = room_to_modify
    try:
        if request.method == 'GET':
            campus_list = Campus.objects.all().order_by('id')
            building_list = Building.objects.filter(campus_id=campus_list.first().id)
        elif request.method == 'POST':
            campus_list = Campus.objects.all().order_by('id')
            building_list = Building.objects.filter(campus_id=request.POST.get('campus'))
            return_dict['selected_campus'] = int(request.POST.get('campus'))
    except OperationalError:
        return_dict['info_retrieve_failure'] = True
    else:
        return_dict['campus_list'] = campus_list
        return_dict['building_list'] = building_list
        return render(request, 'modify_certain_room.html', return_dict)


def modify_room_submit(request, room_id):  # 提交修改的教室信息
    current_user_group = request.user.groups.first()
    if not current_user_group or current_user_group.name != 'admin':
        return HttpResponseRedirect(reverse('login'))
    if not room_id:
        return HttpResponse(404)  # 必须在url中给出教室编号
    if request.method == 'POST':
        try:
            room_to_modify = Classroom.objects.get(pk=room_id)
        except OperationalError:
            return HttpResponseRedirect(reverse('modify_room') + '?failure=true')
        except Classroom.DoesNotExist:
            return HttpResponseRedirect(reverse('modify_room') + '?no_such_room=true')
        new_room_number = request.POST.get('room_number')
        new_building_id = request.POST.get('building')
        try:
            duplicate = Classroom.objects.get(building_id=new_building_id, room_number=new_room_number)
        except Classroom.DoesNotExist:
            pass
        except Classroom.MultipleObjectsReturned:
            return HttpResponseRedirect(reverse('modify_room') + 'duplication')
        room_to_modify.building_id = request.POST.get('building')
        room_to_modify.room_number = request.POST.get('room_number')
        room_to_modify.type = request.POST.get('room_type')
        room_to_modify.capacity = request.POST.get('room_capacity')
        try:
            room_to_modify.save()
        except OperationalError:
            return HttpResponseRedirect(reverse('modify_room') + '?failure=true')
        else:
            return HttpResponseRedirect(reverse('modify_room') + '?success=true')
    else:
        return HttpResponseRedirect(reverse('modify_room'))


def delete_room(request, room_id):
    current_user_group = request.user.groups.first()
    if not current_user_group or current_user_group.name != 'admin':
        return HttpResponseRedirect(reverse('login'))
    if not room_id:
        return HttpResponseRedirect(reverse('modify_room'))
    if request.method == 'GET':
        success = '?delete_success=true'
        failure = '?delete_failure=true'
        try:
            Classroom.objects.get(pk=room_id).delete()
        except Classroom.DoesNotExist:
            return HttpResponseRedirect(reverse('modify_room') + '?no_such_room=true')
        except OperationalError:
            return HttpResponseRedirect(reverse('modify_room') + failure)
        else:
            return HttpResponseRedirect(reverse('modify_room') + success)


def auto_schedule(request):  # 打开自动排课页面
    current_user_group = request.user.groups.first()
    if not current_user_group or current_user_group.name != 'admin':
        return HttpResponseRedirect(reverse('login'))
    if request.method == 'GET':
        return_dict = {'web_title': '自动排课',
                       'page_title': '自动排课',
                       'request_user': request.user,
                       'cur_submodule': 'auto_schedule'}
        class_list = Class.objects.all()
        for i in class_list:
            rooms = ClassHasRoom.objects.filter(Class_id=i.id)
            if not rooms:  # 如果教学班没有时段记录，则生成时段记录
                times = i.course.duration.split()
                with transaction.atomic():  # 通过事务避免只生成了部分时段记录
                    for j in times:
                        new_section = ClassHasRoom(Class_id=i.id, duration=int(j))
                        new_section.save()
            not_scheduled = ClassHasRoom.objects.filter(Class_id=i.id, classroom__isnull=True)
        try:
            schedule_list = Class.objects.filter(classhasroom__classroom__isnull=True)
            for i in schedule_list:
                i.not_scheduled = True
            scheduled_list = Class.objects.filter(classhasroom__classroom__isnull=False)
            for i in scheduled_list:
                i.not_scheduled = False
        except OperationalError:
            pass
        else:
            schedule_list = schedule_list.union(scheduled_list)
            return_dict['schedule_list'] = schedule_list
        return render(request, 'auto_schedule.html', return_dict)


@transaction.atomic
def do_auto_schedule(request):  # 进行自动排课。。。麻烦（（（
    current_user_group = request.user.groups.first()
    if not current_user_group or current_user_group.name != 'admin':
        return HttpResponseRedirect(reverse('login'))
    return HttpResponseRedirect(reverse('auto_schedule'))


def manipulate_schedule(request):  # 打开手动调课页面
    current_user_group = request.user.groups.first()
    if not current_user_group or current_user_group.name != 'admin':
        return HttpResponseRedirect(reverse('login'))
    if request.method == 'GET':
        return_dict = {'web_title': '手动课程调整',
                       'page_title': '手动课程调整',
                       'request_user': request.user,
                       'cur_submodule': 'manipulate_schedule'}
        selection1 = request.GET.get('cx_cxlb_1')
        if selection1:
            condition1 = request.GET.get('cx_cxnr_1')
            try:
                if selection1 == 'skjs':
                    class_selection1 = Class.objects.filter(teacher__first_name__in=condition1)
                    class_selection1 = class_selection1.union(Class.objects.filter(teacher__last_name__contains=condition1))
                elif selection1 == 'kcmc':
                    class_selection1 = Class.objects.filter(course__name__contains=condition1)
                elif selection1 == 'sksj':
                    class_selection1 = Class.objects.filter(classhasroom__day=int(request.GET.get('day1')))
                elif selection1 == 'kcdd':
                    room_selection1 = Classroom.objects.filter(building__campus__name__in=condition1)
                    room_selection2 = Classroom.objects.filter(building__name__in=condition1)
                    room_selection3 = Classroom.objects.filter(room_number__in=condition1)
                    if not room_selection1 and not room_selection2 and not room_selection3:
                        room_selection1.intersection(room_selection2)
                        room_selection1.intersection(room_selection3)
                    elif not room_selection1 or not room_selection2 or not room_selection3:
                        if not room_selection1:
                            room_selection1 = room_selection2.intersection(room_selection3)
                        elif not room_selection2:
                            room_selection1 = room_selection1.intersection(room_selection3)
                        elif not room_selection3:
                            room_selection1 = room_selection2.intersection(room_selection1)
                    elif room_selection1 or room_selection2 or room_selection3:
                        if room_selection2:
                            room_selection1 = room_selection2
                        elif room_selection3:
                            room_selection1 = room_selection3
                    class_selection1 = Class.objects.filter(classhasroom__classroom__in=room_selection1)
            except OperationalError:
                pass
        selection2 = request.GET.get('cx_cxlb_2')
        if selection2:
            condition2 = request.GET.get('cx_cxnr_2')
            try:
                if selection2 == 'skjs':
                    class_selection2 = Class.objects.filter(teacher__first_name__in=condition2)
                    class_selection2 = class_selection2.union(Class.objects.filter(teacher__last_name__contains=condition2))
                elif selection2 == 'kcmc':
                    class_selection2 = Class.objects.filter(course__name__contains=condition2)
                elif selection2 == 'sksj':
                    class_selection2 = Class.objects.filter(classhasroom__day=int(request.GET.get('day2')))
                elif selection2 == 'kcdd':
                    room_selection1 = Classroom.objects.filter(building__campus__name__in=condition2)
                    room_selection2 = Classroom.objects.filter(building__name__in=condition2)
                    room_selection3 = Classroom.objects.filter(room_number__in=condition2)
                    if not room_selection1 and not room_selection2 and not room_selection3:
                        room_selection1.intersection(room_selection2)
                        room_selection1.intersection(room_selection3)
                    elif not room_selection1 or not room_selection2 or not room_selection3:
                        if not room_selection1:
                            room_selection1 = room_selection2.intersection(room_selection3)
                        elif not room_selection2:
                            room_selection1 = room_selection1.intersection(room_selection3)
                        elif not room_selection3:
                            room_selection1 = room_selection2.intersection(room_selection1)
                    elif room_selection1 or room_selection2 or room_selection3:
                        if room_selection2:
                            room_selection1 = room_selection2
                        elif room_selection3:
                            room_selection1 = room_selection3
                    class_selection2 = Class.objects.filter(classhasroom__classroom__in=room_selection1)
            except OperationalError:
                pass
            if request.GET.get('logic') == 'and':
                class_selection1 = class_selection1.intersection(class_selection2)
            elif request.GET.get('logic') == 'or':
                class_selection1 = class_selection1.union(class_selection2)
            for i in class_selection1:
                i.teacher = i.teacher.first_name + i.teacher.last_name
            return_dict['courses'] = class_selection1
        return render(request, 'manipulate_schedule.html', return_dict)


def manipulate_certain_class(request, class_id):  # 打开处理特定课程的页面
    current_user_group = request.user.groups.first()
    if not current_user_group or current_user_group.name != 'admin':
        return HttpResponseRedirect(reverse('login'))
    if request.method == 'GET':
        return_dict = {'web_title': '手动课程调整',
                       'page_title': '手动课程调整',
                       'request_user': request.user,
                       'cur_submodule': 'manipulate_schedule'}
        try:
            class_to_modify = Class.objects.get(pk=class_id)
            rooms_to_modify = ClassHasRoom.objects.filter(class_id=class_id)
            campus_list = Campus.objects.all()
            building_list = Building.objects.all()

        except OperationalError:
            pass
        else:
            return_dict['course'] = class_to_modify
            return_dict['rooms'] = rooms_to_modify
            return_dict['campus'] = campus_list
        return render(request, 'manipulate.html', return_dict)


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


def handle_application(request, page=0):  # 打开处理调课申请页面
    current_user_group = request.user.groups.first()
    if not current_user_group or current_user_group.name != 'admin':
        return HttpResponseRedirect(reverse('login'))
    if request.method == 'GET':
        return_dict = {'web_title': '处理调课申请',
                       'page_title': '处理调课申请',
                       'request_user': request.user,
                       'cur_submodule': 'handle_application'}
        try:
            application_list = Application.objects.filter(reply__isnull=True)
        except OperationalError:
            pass
        else:
            return_dict['applications_list'] = application_list
            page_sum = len(application_list) // 10 + 1
            if page >= page_sum:
                return HttpResponse(404)
            return_dict['cur_page'] = page + 1
            return_dict['prev_page'] = (page - 1)
            return_dict['prev_disabled'] = (page == 0)
            return_dict['next_page'] = page + 1
            return_dict['next_disabled'] = (page + 1 >= page_sum)
            return_dict['page_sum'] = page_sum
        return render(request, 'handle_application.html', return_dict)


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


def teacher_class(request):  # 按教师查询课表页面
    if request.method == 'GET':  # 获取3个查询条件
        teacher = request.GET.get('teacher_id')
        year = request.GET.get('year')
        term = request.GET.get('term')


def room_class(request):
    if request.method == 'GET':  # 获取2个查询条件
        year = request.GET.get('year')
        term = request.GET.get('term')
