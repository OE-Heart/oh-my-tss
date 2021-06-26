from django.shortcuts import render

def err_403 (req):
    res = render(req, 'default_err_page.html', {
        'err_text': '没有权限访问该页面。'
    });
    res.status_code = 403
    return res

def err_404 (req):
    res = render(req, 'default_err_page.html', {
        'err_text': '找不到该页面。'
    })
    res.status_code = 404
    return res

def err_50x (req, code):
    res = render(req, 'default_err_page.html', {
        'err_text': '服务器错误。请联系管理员。'
    })
    res.status_code = code
    return res
