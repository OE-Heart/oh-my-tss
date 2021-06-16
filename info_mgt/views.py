from django.http.request import HttpRequest
from django.http.response import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from info_mgt.forms import LoginForm, CourseEditForm
from django.contrib.auth import authenticate, login, logout
from info_mgt import models


def index(req):
    return render(req, 'info_mgt.html', {
        'web_title': '信息管理',
        'page_title': '信息管理',
        # 'form': SignupForm
    })

# TODO: those following pages' templates are not implemented yet.


def account_list(req):
    ''' TODO: render by another template '''
    return render(req, 'info_mgt.html', {
        'web_title': '信息管理',
        'page_title': '账户信息管理',
        'cur_submodule': 'account'
    })


def account_display(req):
    ''' TODO: render by another template '''
    return render(req, 'info_mgt.html', {
        'web_title': '信息管理',
        'page_title': '账户信息',
        'cur_submodule': 'account'
    })


def account_edit(req, option):
    ''' TODO: render by another template '''
    return render(req, 'info_mgt.html', {
        'web_title': '信息管理',
        'page_title': '修改账户信息' if option == 'edit' else '添加账户',
        'cur_submodule': 'account'
    })


def course_list(req):
    ''' TODO: render by another template '''
    return render(req, 'info_mgt.html', {
        'web_title': '课程管理',
        'page_title': '课程信息管理',
        'cur_submodule': 'course'
    })


def course_display(req):
    ''' TODO: render by another template '''
    return render(req, 'info_mgt.html', {
        'web_title': '课程管理',
        'page_title': '课程详情',
        'cur_submodule': 'course'
    })


def course_edit(req, option, in_course_name):
    ''' TODO: render by another template '''
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
        else:
            # TODO: report a 404 error
            return HttpRequest(404)
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
