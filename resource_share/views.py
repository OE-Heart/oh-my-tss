from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,"resource_share.html",{
        'web_title':'资源共享',
        'page_title':'资源共享'
    })
    
def rsdetail(request):
    return render(request,"resource_share_detail.html",{
        'web_title':'资源共享',
        'page_title':'资源共享'
    })

def homework(request):
    return render(request,"homework.html",{
        'web_title':'课程作业',
        'page_title':'课程作业'
    })

def hwdetail(request):
    return render(request,"homework_detail.html",{
        'web_title':'作业详情',
        'page_title':'作业详情'
    })

def hwlist(request):
    return render(request,"homework_list.html",{
        'web_title':'课程作业列表',
        'page_title':'课程作业列表'
    })

def hwlist_t(request):
    return render(request,"homework_list_t.html",{
        'web_title':'课程作业',
        'page_title':'课程作业'
    })

def hwass(request):
    return render(request,"homework_assign.html",{
        'web_title':'布置课程作业',
        'page_title':'布置课程作业'
    })

def hwdetail_t(request):
    return render(request,"homework_detail_t.html",{
        'web_title':'作业详情',
        'page_title':'作业详情'
    })