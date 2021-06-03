from django.shortcuts import render
from info_mgt.forms import SignupForm
from django.contrib.auth import authenticate, login, logout


def index(req):
    return render(req, 'info_mgt.html', {
        'web_title': '信息管理系统',
        'page_title': '信息管理子系统',
        'test_param': 'TEST PARAM',
        'form': SignupForm
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
