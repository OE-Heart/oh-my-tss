from django.http.request import HttpRequest
from django.http.response import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from info_mgt.forms import LoginForm
from info_mgt.forms import SelfInfoForm, LoginForm, CourseEditForm, ClassAddForm, AddForm, EditACForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group

from oh_my_tss.settings import BASE_DIR
from oh_my_tss.errview import *
from . import models
import os
from .models import Major, Student


def index(req):
    return render(req, 'info_mgt.html', {
        'web_title': '信息管理',
        'page_title': '信息管理',
        # 'form': SignupForm
    })


# TODO: those following pages' templates are not implemented yet.

def info_view(req):
    try:
        avatar = models.Avatar.objects.get(user=req.user)
    except ObjectDoesNotExist:
        pass
    # print(avatar.avatar.name)
    res_url = '/media/img/test.png'
    print(res_url)

    return render(req, 'info_view.html', {
        'web_title': '个人信息',
        'page_title': '个人信息',
        'request_user': req.user,
        'url': res_url
    })


def info_view_with_username(req, username):
    try:
        user = models.User.objects.get(username=username)
    except:
        return HttpResponse(404)

    return render(req, 'info_view.html', {
        'web_title': '个人信息',
        'page_title': '个人信息',
        'request_user': user,
    })


def info_edit(req):
    ''' TODO: repair it '''
    if req.method == 'POST':
        new_username = req.POST['username']
        new_last_name = req.POST['last_name']
        new_first_name = req.POST['first_name']
        new_email = req.POST['email']
        new_avatar = req.FILES.get('avatar')

        query = models.Avatar.objects.filter(user=req.user)

        if len(query) == 0:
            result2 = models.Avatar.objects.create(user=req.user, avatar=new_avatar)
            f = open(os.path.join(BASE_DIR, 'media', 'img', new_avatar.name), 'wb+')
            for chunk in new_avatar.chunks():
                f.write(chunk)
            f.close()
        elif len(new_avatar) != 0:
            result2 = query.update(avatar=new_avatar)
            f = open(os.path.join(BASE_DIR, 'media', 'img', new_avatar.name), 'wb+')
            for chunk in new_avatar.chunks():
                f.write(chunk)
            f.close()
        else:
            result2 = True

        query_set = models.User.objects.filter(id=req.user.id)
        result = query_set.update(username=new_username, last_name=new_last_name,
                                  first_name=new_first_name, email=new_email)

        return render(req, 'info_edit.html', {
            'web_title': '个人信息修改', 'page_title': '个人信息修改', 'request_user': req.user,
            'form': SelfInfoForm(instance=req.user), 'edit': True,
            'edit_result': True if result != 0 and result2 != 0 else False
        })
    elif req.method == 'GET':
        obj = req.user
        # avatar_obj = models.Avatar.objects.filter(user=req.user)
        # print(avatar_obj)
        return render(req, 'info_edit.html', {
            'web_title': '个人信息修改', 'page_title': '个人信息修改', 'request_user': req.user,
            'form': SelfInfoForm(instance=obj), 'edit': False})
    else:
        return HttpRequest(404)


def class_add(req):
    if req.method == 'GET':
        return render(req, 'class_add.html', {
            'web_title': '教学班管理',
            'page_title': '添加教学班',
            'cur_submodule': 'class',
            'form': ClassAddForm
        })
    elif req.method == 'POST':
        course_name = req.POST['course']
        teacher_name = req.POST['teacher']
        year = req.POST['year']
        term = req.POST['term']
        course_ex = models.Course.objects.filter(name=course_name)
        teacher_ex = models.Teacher.objects.filter(name=teacher_name)
        if len(course_ex) == 0:
            return render(req, 'class.html', {
                'web_title': '教学班管理',
                'page_title': '添加教学班',
                'cur_submodule': 'class',
                'form': ClassAddForm,
                'edit_result': 'no_such_course'
            })
        elif len(teacher_ex) == 0:
            return render(req, 'class.html', {
                'web_title': '教学班管理',
                'page_title': '添加教学班',
                'cur_submodule': 'class',
                'form': ClassAddForm,
                'edit_result': 'no_such_teacher'
            })
        else:
            models.Class.objects.create(
                course=course_name,
                teacher=teacher_name,
                year=year,
                term=term
            )
            return render(req, 'class.html', {
                'web_title': '教学班管理',
                'page_title': '添加教学班',
                'cur_submodule': 'class',
                'form': ClassAddForm,
                'edit_result': 'success'
            })


def account_edit(req, username='#'):
    if req.user.has_perm('info_mgt.change_student') and req.user.has_perm('info_mgt.change_teacher'):
        if req.method == 'POST':
            new_username = req.POST['username']
            new_last_name = req.POST['last_name']
            new_first_name = req.POST['first_name']
            new_email = req.POST['email']
            new_avatar = req.FILES.get('avatar')
            new_major = req.POST['major']
            this_user = models.User.objects.get(username=username)
            if this_user:
                this_user.username = new_username
                this_user.last_name = new_last_name
                this_user.first_name = new_first_name
                this_user.email = new_email
                if this_user.groups.filter(name="student").exists():
                    this_user.student.major = new_major
                elif this_user.groups.filter(name="teacher").exists():
                    this_user.teacher.department = new_major
                this_user.save()
                result_0 = True
            else:
                result_0 = False

            query = models.Avatar.objects.filter(user=this_user)
            if len(query) == 0 and new_avatar is not None and result_0:
                result_2 = models.Avatar.objects.create(user=this_user, avatar=new_avatar)
                f = open(os.path.join(BASE_DIR, 'media', 'img', new_avatar.name), 'wb+')
                for chunk in new_avatar.chunks():
                    f.write(chunk)
                f.close()
            elif new_avatar is not None:
                result_2 = query.update(avatar=new_avatar)
                f = open(os.path.join(BASE_DIR, 'media', 'img', new_avatar.name), 'wb+')
                for chunk in new_avatar.chunks():
                    f.write(chunk)
                f.close()
            else:
                result_2 = True
            return render(req, 'account_edit.html', {
                'web_title': '用户信息修改',
                'page_title': '用户信息修改',
                'request_user': req.user,
                'forms': SelfInfoForm(instance=this_user),
                'edit': True,
                'edit_result': True if result_0 != 0 and result_2 != 0 else False
            })
        elif req.method == 'GET':
            if username != '#':
                obj = models.User.objects.get(username=username)
                return render(req, 'account_edit.html', {
                    'web_title': '用户信息修改',
                    'page_title': '用户信息修改',
                    'request_user': req.user,
                    'forms': SelfInfoForm(instance=obj),
                    'edit': False
                })
            else:
                obj = req.user
                return render(req, 'account_edit.html', {
                    'web_title': '用户信息修改',
                    'page_title': '用户信息修改',
                    'request_user': req.user,
                    'forms': SelfInfoForm,
                    'edit': False
                })
        else:
            return HttpResponseRedirect(404)
    else:
        return HttpResponseRedirect(403)


def account_add(req):
    if req.user.has_perm('info_mgt.add_student') or req.user.has_perm('info_mgt.add_teacher'):
        if req.method == 'POST':
            new_username = req.POST['username']
            new_last_name = req.POST['last_name']
            new_first_name = req.POST['first_name']
            new_email = req.POST['email']
            new_major = req.POST['major']
            new_avatar = req.FILES.get('avatar')
            new_group = req.POST['role']

            result_0 = models.User.objects.create(username=new_username, last_name=new_last_name,
                                                  first_name=new_first_name, email=new_email)

            this_user = models.User.objects.get(username=new_username)

            if this_user and new_group:
                if new_group == 'teacher':
                    target_group = Group.objects.get(id=2)
                    this_user.groups.add(target_group)
                    this_user.teacher.department.name = new_major
                    this_user.save()
                elif new_group == 'student':
                    target_group = Group.objects.get(id=1)
                    print(target_group)
                    this_user.groups.add(target_group)
                    this_user.student.major.name = new_major
                    this_user.save()

            query = models.Avatar.objects.filter(user=this_user)
            if len(query) == 0 and new_avatar is not None and result_0:
                result_2 = models.Avatar.objects.create(user=this_user, avatar=new_avatar)
                f = open(os.path.join(BASE_DIR, 'media', 'img', new_avatar.name), 'wb+')
                for chunk in new_avatar.chunks():
                    f.write(chunk)
                f.close()
            elif new_avatar is not None and result_0:
                result_2 = query.update(avatar=new_avatar)
                f = open(os.path.join(BASE_DIR, 'media', 'img', new_avatar.name), 'wb+')
                for chunk in new_avatar.chunks():
                    f.write(chunk)
                f.close()
            else:
                result_2 = True
            return render(req, 'account_add.html', {
                'web_title': '用户信息添加',
                'page_title': '用户信息添加',
                'request_user': req.user,
                'forms': AddForm,
                'result': 'success',
                'edit_result': True if result_0 != 0 and result_2 != 0 else False
            })
        elif req.method == 'GET':
            obj = req.user
            return render(req, 'account_add.html', {
                'web_title': '用户信息添加',
                'page_title': '用户信息添加',
                'request_user': req.user,
                'result': 'wait',
                'forms': AddForm,
                'edit_result': True
            })
        else:
            return HttpRequest(404)
    else:
        return HttpRequest(403)


def account_list(req, page=0):
    accounts = []

    if req.user.has_perm('info_mgt.view_student') and req.user.has_perm('info_mgt.view_teacher'):

        account_sum = len(User.objects.all())

        for i in range(account_sum):
            groups = User.objects.all()[i].groups.all()
            account = User.objects.all()[i]

            name = account.first_name + ' ' + account.last_name
            major = ''
            username = account.username

            try:
                major = account.student.major.name
            except:
                try:
                    major = account.teacher.department.name
                except:
                    major = ''

            accounts.append({
                'name': name,
                'major': major,
                'username': username
            })
        # accounts.append(User.objects.all()[4].student)

        if req.method == 'POST' and req.POST['name']:
            accounts = [x for x in accounts if x['name'] == req.POST['name']]

        page_sum = max((len(accounts) - 1) // 10 + 1, 1)

        if page >= page_sum:
            return err_404(req)

    else:
        return err_403(req)

    disp_accounts = accounts[page * 10:(page + 1) * 10]

    # if req.user.has_perm('info_mgt.view_course'):

    #     if req.method == 'POST' and req.POST['name']:
    #         courses = models.Course.objects.filter(name=req.POST['name'])
    #     else:
    #         courses = models.Course.objects.all()[page * 10: page * 10 + 10]

    #     page_sum = len(courses) // 10 + 1

    #     if page >= page_sum:
    #         return HttpResponse(404)

    return render(req, 'accountlist.html', {
        'web_title': '信息管理',
        'page_title': '账户信息管理',
        'cur_submodule': 'account',
        'accounts': disp_accounts,
        'cur_page': page + 1,
        'prev_page': page - 1,
        'prev_disabled': page == 0,
        'next_page': page + 1,
        'next_disabled': page + 1 >= page_sum,
        'page_sum': page_sum,
        'last_search': req.POST['name'] if req.method == 'POST' else None,
    })


def account_delete(req, username):
    if req.user.has_perm('info_mgt.delete_student') and req.user.has_perm(
            'info_mgt.delete_teacher') and req.method == 'GET':
        User.objects.filter(username=username).delete()
        return HttpResponseRedirect('/info_mgt/account')
    else:
        return HttpResponse(403)


def course_list(req, page=0):
    if req.user.has_perm('info_mgt.view_course'):

        if req.method == 'POST' and req.POST['name']:
            courses = models.Course.objects.filter(name=req.POST['name'])
        else:
            courses = models.Course.objects.all()[page * 10: page * 10 + 10]

        page_sum = max((len(courses) - 1) // 10 + 1, 1)

        if page >= page_sum:
            return err_404(req)
        return render(req, 'courselist.html', {
            'web_title': '课程管理',
            'page_title': '课程信息管理',
            'cur_submodule': 'course',
            'courses': courses,
            'cur_page': page + 1,
            'prev_page': page - 1,
            'prev_disabled': page == 0,
            'next_page': page + 1,
            'next_disabled': page + 1 >= page_sum,
            'page_sum': page_sum,
            'last_search': req.POST['name'] if req.method == 'POST' else None,
        })
    else:
        return err_403(req)


def course_detail(req, name):
    if req.user.has_perm('info_mgt.view_course'):
        course = models.Course.objects.get(name=name)
        return render(req, 'course_detail.html', {
            'web_title': '课程管理',
            'page_title': '课程详情',
            'cur_submodule': 'course',
            'request_course': course
        })
    else:
        return HttpResponse(403)


def course_edit(req, option, in_course_name):
    if req.user.has_perm('info_mgt.change_course'):
        if req.method == 'POST':
            course_name = req.POST.get('name')
            course_desc = req.POST.get('description')
            course_credit = req.POST.get('credit')
            course_capacity = req.POST.get('capacity')
            course_duration = req.POST.get('duration')
            if option == 'edit':
                query_set = models.Course.objects.filter(name=in_course_name)
                n_updates = query_set.update(
                    name=course_name,
                    description=course_desc,
                    credit=course_credit,
                    capacity=course_capacity,
                    duration=course_duration
                )
                return render(req, 'course_edit.html', {
                    'web_title': '课程管理',
                    'page_title': '修改课程详情',
                    'cur_submodule': 'course',
                    'form': CourseEditForm(instance=models.Course.objects.filter(name=course_name)[0]),
                    'edit_result': True if n_updates != 0 else False
                })
            elif option == 'new':
                ins = models.Course.objects.create(
                    name=course_name,
                    description=course_desc,
                    credit=course_credit,
                    capacity=course_capacity,
                    duration=course_duration
                )
                return render(req, 'course_edit.html', {
                    'web_title': '课程管理',
                    'page_title': '添加课程',
                    'cur_submodule': 'course',
                    'form': CourseEditForm,
                    'new_result': True if ins else False
                })
            elif option == 'delete':
                return HttpResponse(403)
            else:
                # TODO: report a 404 error
                return HttpResponse(404)
        elif req.method == 'GET':
            if option == 'edit':
                page_title = '修改课程详情'
                course_data = models.Course.objects.get(name=in_course_name)
                form_obj = CourseEditForm(instance=course_data)
                return render(req, 'course_edit.html', {
                    'web_title': '课程管理',
                    'page_title': '修改课程详情',
                    'cur_submodule': 'course',
                    'form': form_obj
                })
            elif option == 'new':
                page_title = '添加课程'
                return render(req, 'course_edit.html', {
                    'web_title': '课程管理',
                    'page_title': '添加课程',
                    'cur_submodule': 'course',
                    'form': CourseEditForm
                })
            elif option == 'delete':
                models.Course.objects.get(name=in_course_name).delete()
                return HttpResponseRedirect('/info_mgt/course')
        else:
            return HttpResponse(403)
    else:
        return HttpResponse(403)


def course_delete(req, name):
    if req.user.has_perm('info_mgt.delete_course') and req.method == 'GET':
        models.Course.objects.get(name=name).delete()
        return HttpResponseRedirect('/info_mgt/course')
    else:
        return HttpResponse(403)


def class_list(req, page=0):
    classes = models.Class.objects.all()[page * 10: page * 10 + 10]
    page_sum = (len(classes) - 1) // 10 + 1
    if page >= page_sum:
        return HttpResponse(404)
    return render(req, 'classlist.html', {
        'web_title': '教学班级',
        'page_title': '教学班级管理',
        'cur_submodule': 'class',
        'classes': classes,
        'cur_page': page + 1,
        'prev_page': page - 1,
        'prev_disabled': page == 0,
        'next_page': page + 1,
        'next_disabled': page + 1 >= page_sum,
        'page_sum': page_sum,
    })


def login_view(req):
    if req.method == 'GET':
        return render(req, 'login.html', {
            'form': LoginForm
        })
    elif req.method == 'POST':
        # Authentication
        username = req.POST['username']
        password = req.POST['password']
        user = authenticate(req, username=username, password=password)
        if user is not None:
            login(req, user)
            # TODO: Redirect to a success page.
            return HttpResponseRedirect('/info_mgt')
        else:
            # TODO: Return an 'invalid login' error message.
            return render(req, 'login.html', {
                'form': LoginForm,
                'login_err_tips': True
            })
    else:
        pass


def logout_view(request):
    logout(request)
    # TODO: Redirect to a success page.
    return HttpResponseRedirect('/info_mgt')


'''
{% if blog.article %}  <!-- permission to visit articles in the blog -->
    <p>You have permission to do something in this blog app.</p>
    {% if perms.blog.add_article %}
        <p>You can add articles.</p>
    {% endif %}
    {% if perms.blog.comment_article %}
        <p>You can comment articles!</p>
    {% endif %}
{% else %}
    <p>You don't have permission to do anything in the blog app.</p>
{% endif %}
'''
