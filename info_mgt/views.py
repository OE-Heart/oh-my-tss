from django.http.request import HttpRequest
from django.http.response import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from info_mgt.forms import LoginForm
from info_mgt.forms import SelfInfoForm
from django.contrib.auth import authenticate, login, logout
from . import models
from .models import Major


def index(req):
    return render(req, 'info_mgt.html', {
        'web_title': '信息管理',
        'page_title': '信息管理',
        # 'form': SignupForm
    })

# TODO: those following pages' templates are not implemented yet.


def info_view(req):
    if req.method == 'POST' and req.POST['name']:
        courses = models.Course.objects.filter(name=req.POST['name'])
    else:
        courses = models.Course.objects.all()
    return render(req, 'info_view.html', {
        'web_title': '个人信息',
        'page_title': '个人信息',
        'request_user': req.user,
    })

def info_edit(req):
    return render(req, 'info_edit.html', {
        'web_title': '个人信息修改',
        'page_title': '个人信息修改'
    })

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


def course_list(req, page):
    if req.user.has_perm('info_mgt.view_course'):

        if req.method == 'POST' and req.POST['name']:
                courses = models.Course.objects.filter(name=req.POST['name'])
        else:
            courses = models.Course.objects.all()[page: page + 10]

        page_sum = len(courses) // 10 + 1

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
        return HttpResponse(403)


def course_display(req):
    ''' TODO: render by another template '''
    return render(req, 'info_mgt.html', {
        'web_title': '课程管理',
        'page_title': '课程详情',
        'cur_submodule': 'course'
    })


def course_edit(req, option):
    ''' TODO: render by another template '''

    if option == 'edit':
        page_title = '修改课程详情'
    elif option == 'new':
        page_title = '添加课程'
    else:
        # TODO: report a 404 error
        return HttpRequest(404)

    return render(req, 'info_mgt.html', {
        'web_title': '课程管理',
        'page_title': '修改课程详情' if option == 'edit' else '添加课程',
        'cur_submodule': 'course'
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
