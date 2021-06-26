import os
from django.http.response import HttpResponseNotModified
from django.shortcuts import redirect, render
from .models import *
from info_mgt.models import *
from django.views.decorators.http import require_GET,require_POST
from grade_mgt.models import *
from class_selection.models import *
from django.http import HttpResponse
from grade_mgt.views import *
from django.core.files import File
from django.utils.http import urlquote
# Create your views here.
def index(request):
    return render(request,"resource_share.html",{
        'web_title':'资源共享',
        'page_title':'资源共享'
    })
    
def rsdetail(request):
    # parent_object = None
    # folder_id = request.GET.get('folder', "")
    # if folder_id.isdecimal():
    #     parent_object = models.Source.objects.filter(id=int(folder_id), file_type=2)

    # if request.method == "GET":
    #     parent = parent_object

    #     # 当前目录下所有的文件 & 文件夹获取到即可
    #     queryset = models.Source.objects.filter(class=request.tracer.class_id) # 获取课程id
    #     if parent_object:
    #         # 进入了某目录
    #         files = queryset.filter(parent=parent_object, file_type_choice=1).order_by('-file_type')
    #         folder= queryset.filter(parent=parent_object, file_type_choice=2).order_by('-file_type')
    #     else:
    #         # 根目录
    #         file_object_list = queryset.filter(parent__isnull=True).order_by('-file_type')
        

    #     context = {
    #         'web_title':'资源共享',
    #         'page_title':'资源共享',
    #         "files": file_object_list,
    #         'folder': parent_object
    #     }
    #     return render(request, 'file.html', context)



    files = os.listdir("media")
    folder=[]
    realfile=[]
    for file in files:
        if os.path.isdir("media"+"\\"+file):
            folder.append(file)
        else:
            realfile.append(file)
    print(files)
    return render(request,"resource_share_detail.html",{
        'web_title':'资源共享',
        'page_title':'资源共享',
        'files':realfile,
        'folder':folder
    })
@require_POST
def up(request):
    file = request.FILES.get('myfile')
    destination = open(os.path.join("media",file.name),'wb+')
    for chunk in file.chunks():
        destination.write(chunk)
    destination.close()
    return render_home_template(request)

@require_GET
def down(request,filename):
    file_path = os.path.join("media",filename)
    with open(file_path,'rb') as f:
        file = File(f)
        response = HttpResponse(file.chunks(),content_type="APPLICATION/OCET-STREAM")
        response['Content-Disposition'] = 'attachment; filename=' + urlquote(filename)
        response['Content-Length']=os.path.getsize(file_path)
    return response

def render_home_template(request):
    # parent_object = None
    # folder_id = request.GET.get('folder')
    # if folder_id.isdecimal():
    #     parent_object = models.Source.objects.filter(id=int(folder_id), file_type=2)

    # if request.method == "GET":
    #     parent = parent_object

    #     # 当前目录下所有的文件 & 文件夹获取到即可
    #     queryset = models.Source.objects.filter(class=request.tracer.class_id) # 获取课程id
    #     if parent_object:
    #         # 进入了某目录
    #         files = queryset.filter(parent=parent_object, file_type_choice=1).order_by('-file_type')
    #         folder= queryset.filter(parent=parent_object, file_type_choice=2).order_by('-file_type')
    #     else:
    #         # 根目录
    #         file_object_list = queryset.filter(parent__isnull=True).order_by('-file_type')
        

    #     context = {
    #         'web_title':'资源共享',
    #         'page_title':'资源共享',
    #         "files": file_object_list,
    #         'folder': parent_object
    #     }
    #     return render(request, 'file.html', context)


    files = os.listdir("media")
    folder=[]
    realfile=[]
    for file in files:
        if os.path.isdir("media"+"\\"+file):
            folder.append(file)
        else:
            realfile.append(file)
    print(files)
    return render(request,"resource_share.html",{'files':realfile,'folder':folder})

def new(request):
    foldername=''
    dict_P = request.POST
    for k,v in dict_P.items():
        if k=="newfolder":
            foldername=v
    os.mkdir("media"+'\\'+foldername)
    # print(foldername)
    return HttpResponse("!")

def homework(request):
    userid=request.user.id
    stu_list=list(Student.objects.values().filter(user_id=userid))
    if stu_list:
        studentid=stu_list[0]['id']
        # print(studentid)
        classlist=list(StuHasClass.objects.values('Class_id').filter(Student_id=studentid))
        print(classlist)
        listtoshow=[]
        classtakentime=[]
        classidlist=[]
        wlist=[]
        for class1 in classlist:
            classid=class1['Class_id']
            classidlist.append(classid)
            courselist=list(Class.objects.values('course_id').filter(id=classid))
            courseid=courselist[0]['course_id']
            courseinfo=list(Course.objects.values('name').filter(id=courseid))
            classres=list(ClassHasRoom.objects.values('id','day','start_at','duration','Class_id').filter(Class_id=classid))
            # print(classres)
            for classres1 in classres:
                classres1['date']=numswitch(classres1['day'])
                classres1['timespan']=getspan(classres1['start_at'],classres1['duration'])
                classtakentime.append({'Class_id':classres1['Class_id'],'date':numswitch(classres1['day']),'timespan':getspan(classres1['start_at'],classres1['duration'])})
            listtoshow.append(classres1)
            # print(listtoshow)
        print(classtakentime)
        for classid1 in classidlist:
            wlist.append({'Class_id':classid1,'time':[]})
        # print(wlist)
        # print(classtakentime)
        for wlist1 in wlist:
            classid=wlist1['Class_id']
            courselist=list(Class.objects.values('course_id').filter(id=classid))
            courseid=courselist[0]['course_id']
            courseinfo=list(Course.objects.values('name').filter(id=courseid))
            coursename=courseinfo[0]['name']
            wlist1['course_id']=courseid
            wlist1['coursename']=coursename
            anwserlist=[]
            for classtaken in classtakentime:
                if (classtaken['Class_id']==wlist1['Class_id']):
                    anwserlist.append({'date':classtaken['date'],'timespan':classtaken['timespan']})
            wlist1['time']=anwserlist
        print(wlist)
        return render(request,"homework.html",{
            'web_title':'课程作业',
            'page_title':'课程作业',
            'wlist':wlist
        })
    else:
        courselist=list(Class.objects.values().filter(teacher_id=userid).order_by('course_id'))
        listtoshow=[]
        classtakentime=[]
        wlist=[]
        classidlist=[]
        for course in courselist:
            classid=course['id']            
            classidlist.append(classid)
            classres=list(ClassHasRoom.objects.values('id','day','start_at','duration','Class_id').filter(Class_id=classid))            
            for classres1 in classres:
                classres1['date']=numswitch(classres1['day'])
                classres1['timespan']=getspan(classres1['start_at'],classres1['duration'])
                classtakentime.append({'Class_id':classres1['Class_id'],'date':numswitch(classres1['day']),'timespan':getspan(classres1['start_at'],classres1['duration'])})
            listtoshow.append(classres1)
        for classid1 in classidlist:
            wlist.append({'Class_id':classid1,'time':[]})
        for wlist1 in wlist:
            anwserlist=[]
            for classtaken in classtakentime:
                if (classtaken['Class_id']==wlist1['Class_id']):
                    anwserlist.append({'date':classtaken['date'],'timespan':classtaken['timespan']})
            wlist1['time']=anwserlist
        course_dict={}
        for course in courselist:
            course_dict[course['course_id']]=[]
        for course in courselist:
            course_dict[course['course_id']].append(course)
        coursename=[]
        i=0
        for course_id,courseinfo in course_dict.items():
            course=list(Course.objects.values('name').filter(id=course_id))
            course[0]['info_list']=courseinfo
            templist=[]
            for wlist1 in wlist:
                for courseinfo1 in courseinfo:
                    if wlist1['Class_id']==courseinfo1['id']:
                       templist.append(wlist1)
            course[0]['class_list']=templist  
            coursename.append(course[0])
        print(coursename)
        return render(request,"homework_teacher.html",{
            'web_title':'课程作业',
            'page_title':'课程作业',
            'wholelist':coursename
        })

def hwdetail(request):
    return render(request,"homework_detail.html",{
        'web_title':'作业详情',
        'page_title':'作业详情'
    })

def hwlist(request):
    if request.POST:
        dict_P = request.POST
        classid=0
        for k,v in dict_P.items():
            if (v=='查看作业'):
                classid=k
        request.session['pastinfo']=classid
        courselist=list(Class.objects.values('course_id').filter(id=classid))
        course_id=courselist[0]['course_id']
        request.session['pastcourseinfo']=course_id
    else:
        classid = request.session.get('pastinfo')
    print(classid)
    asslist=list(Ass)
    return render(request,"homework_list.html",{
        'web_title':'课程作业列表',
        'page_title':'课程作业列表'
    })

def hwlist_t(request):
    if request.POST:
        dict_P = request.POST
        classid=0
        for k,v in dict_P.items():
            if (v=='布置作业'):
                classid=k
        request.session['pastinfo']=classid
        courselist=list(Class.objects.values('course_id').filter(id=classid))
        course_id=courselist[0]['course_id']
        request.session['pastcourseinfo']=course_id
    else:
        classid = request.session.get('pastinfo')
    classinfo=list(Class.objects.values().filter(id=classid))
    courseid=classinfo[0]['course_id']
    courseinfo=list(Course.objects.values('name').filter(id=courseid))
    classtaketimetemp=[]
    classtime=[]
    classtimeinfo=list(ClassHasRoom.objects.values('id','day','start_at','duration','Class_id').filter(Class_id=classid))
    for classtime_info in classtimeinfo:
        classtime_info['date']=numswitch(classtime_info['day'])
        classtime_info['timespan']=getspan(classtime_info['start_at'],classtime_info['duration'])
        classtaketimetemp.append({'Class_id':classtime_info['Class_id'],'date':numswitch(classtime_info['day']),'timespan':getspan(classtime_info['start_at'],classtime_info['duration'])})
    for i in classtaketimetemp:
        classtime.append({'date':i['date'],'timespan':i['timespan']})
    assignmentlist=list(Assignment.objects.values('id','assignment_name','assignment_start','assignment_end').filter(Class=classid))
    # print(assignmentlist)
    wlist=[]
    for ass in assignmentlist:
        wlist.append(
            {'name':ass['assignment_name'],
            'start':str(ass['assignment_start']),
            'end':str(ass['assignment_end']),
            'id':ass['id'],
            })
    print(wlist)
    return render(request,"homework_list_t.html",{
        'web_title':'课程作业',
        'page_title':'课程作业',
        'classinfo':classinfo,
        'courseinfo':courseinfo,
        'classtime':classtime,
        'asslist':wlist
    })

def hwass(request):
    return render(request,"homework_assign.html",{
        'web_title':'布置课程作业',
        'page_title':'布置课程作业'
    })
def addassignment(request):
    classid = request.session.get('pastinfo')
    courselist=list(Class.objects.values('course_id').filter(id=classid))
    courseid=courselist[0]['course_id']
    dict_p = request.POST
    print(dict_p)
    homeworkname=""
    starttime=""
    endtime=""
    homeworkratio=""
    homeworkintro=""
    for k,v in dict_p.items():
        if (k=='作业名'):
            homeworkname=v
        elif (k=='开始时间'):
            starttime=v
        elif (k=='截止时间'):
            endtime=v
        elif (k=='作业占比'):
            homeworkratio=v
        elif (k=='作业详情'):
            homeworkintro=v
    homeworking=Assignment.objects.create(assignment_start=starttime,assignment_end=endtime,assignment_intro=homeworkintro,assignment_ratio=homeworkratio,assignment_name=homeworkname)
    courses = Course.objects.filter(id=courseid).first()
    classes = Class.objects.filter(id=classid).first()
    homeworking.course.add(courses)
    homeworking.Class.add(classes)
    homeworking = Assignment.objects.values().filter(Class=classid)
    # return HttpResponse(dict_p)
    return redirect("hwlist_t")
def hwdetail_t(request):
    if request.POST:
        dict_p = request.POST
        homeworkid=0
        print(dict_p)
        for k,v in dict_p.items():
            if (v=='查看详情'):
                homeworkid=k
        request.session['pasthw']=homeworkid
    else:
        homeworkid = request.session.get('pasthw')
    # print(homeworkid)
    info=list(Assignment.objects.values('id','assignment_name','assignment_start','assignment_end','assignment_intro','course','assignment_ratio').filter(id=homeworkid))
    # print(info)
    info[0]['start']=str(info[0]['assignment_start'])
    info[0]['end']=str(info[0]['assignment_end'])
    courselist=list(Course.objects.values('name').filter(id=info[0]['course']))
    info[0]['coursename']=courselist[0]['name']
    print(info)
    return render(request,"homework_detail_t.html",{
        'web_title':'作业详情',
        'page_title':'作业详情',
        'info':info
    })
def homework_detail_update(request):
    dict_p = request.POST
    homeworkid=0
    homeworkname=""
    start=""
    end=""
    homeworkratio=0
    homeworkintro=""
    is_start=0
    is_end=0
    flag=0
    for k,v in dict_p.items():
        if (flag==0 and v=='保存修改'):
            homeworkid = k
            flag=1
        elif (k=='作业名称'):
            homeworkname=v
        elif (k=='开始时间'):
            if (v != ""):
                is_start=1
                start=v
        elif (k=='截止时间'):
            if (v != ""):
                is_end=1
                end=v
        elif (k=='作业占比'):
            homeworkratio=v
        elif (k=='作业详情'):
            homeworkintro=v
    res = Assignment.objects.values().filter(id=homeworkid)
    if res:
        res.update(assignment_intro=homeworkintro,assignment_ratio=homeworkratio,assignment_name=homeworkname)
        if is_start:
            res.update(assignment_start=start)
        if is_end:
            res.update(assignment_end=end)
    res = list(Assignment.objects.values().filter(id=homeworkid))
    print(res)
    return redirect("hwlist_t")

def homeworkdelete(request):
    dict_p = request.POST
    homeworkid = 0
    print(dict_p)
    for k,v in dict_p.items():
        if (v=='删除'):
            homeworkid=k
    homeworktodel = Assignment.objects.get(id=homeworkid)
    homeworktodel.Class.clear()
    homeworktodel.course.clear()
    homeworktodel.delete()
    return redirect("hwlist_t")