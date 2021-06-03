from django.http.request import HttpRequest
from django.http.response import Http404
from django.shortcuts import render
from info_mgt.forms import SignupForm
from django.contrib.auth import authenticate, login, logout


def index(req):
    return render(req, 'info_mgt.html', {
        'web_title': '信息管理',
        'page_title': '信息管理',
        'form': SignupForm
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


def course_edit(req, option):
    ''' TODO: render by another template '''

    if option == 'edit':
        page_title = '修改课程详情'
    elif option == 'new':
        page_title = '添加课程'
    else:
        # TODO: report a 404 error
        return HttpRequest(404);

    return render(req, 'info_mgt.html', {
        'web_title': '课程管理',
        'page_title': '修改课程详情' if option == 'edit' else '添加课程',
        'cur_submodule': 'course'
    })


def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # TODO: Redirect to a success page.
    else:
        # TODO: Return an 'invalid login' error message.
        pass


def logout_view(request):
    logout(request)
    # TODO: Redirect to a success page.


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
