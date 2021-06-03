from django.shortcuts import render
from info_mgt.forms import SignupForm

# Create your views here.


def index(req):
    return render(req, 'info_mgt.html', {
        'web_title': '信息管理系统',
        'page_title': '信息管理子系统',
        'test_param': 'TEST PARAM',
        'form': SignupForm
    })
