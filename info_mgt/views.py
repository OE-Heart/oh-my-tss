from django.shortcuts import render
from info_mgt.forms import SignupForm

# Create your views here.


def index(req):
    return render(req, 'info_mgt.html', {
        'web_title': '信息管理',
        'page_title': '信息管理',
        'test_param': 'TEST PARAM',
        'form': SignupForm
    })

def account(req):
    return render(req, 'info_mgt.html', {
        'web_title': '信息管理',
        'page_title': '账户信息管理',
        'test_param': 'asdfea',
        'cur_submodule': 'account'
    })
