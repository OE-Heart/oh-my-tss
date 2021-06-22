from class_schedule.models import ClassHasRoom
from typing import Coroutine
from django.db import models
from django.shortcuts import render
from django.http.response import HttpResponse
# from grade_mgt.models import CourseResult
from info_mgt.models import Class, Course, Teacher
from grade_mgt.models import CourseResult
from .models import *
from django.contrib.auth.models import User
# Create your views here.

def index(request):
    # return HttpResponse(request.user.id)
    userid=request.user.id
    stu_list=list(Student.objects.values().filter(user_id=userid))
    if stu_list:
        graderesult=CourseResult.objects.all()
        gradelist=list(CourseResult.objects.values('final_result'))
        courseresult2=[]
        i=0
        gp=0
        for graderes in graderesult:
            courseresult1=list(graderes.course.all().values('id','name','credit'))
            courseresult1[0]['final_result']=gradelist[i]['final_result']
            grade=gradelist[i]['final_result']
            gp = calculategp(grade)
            courseresult1[0]['gp']=gp
            courseresult2.append(courseresult1[0])
            i=i+1
            # print(courseresult1)
        # print(courseresult2)
        # # resultid=graderesult1[0]['id']
        # # test1=list(Course.objects.values())
        # # courseresult1=list(CourseResult.objects.values())
        # print(gradelist)
        # # return HttpResponse(graderesult1)
        return render(request,"grade_mgt.html",{
            'web_title':'成绩管理',
            'page_title':"成绩管理",
            'course_list':courseresult2,
            'grade_list':gradelist
        })
    else:
        userid=request.user.id
        # print(userid)
        courselist=list(Class.objects.values().filter(teacher_id=userid).order_by('course_id'))
        # print(courselist)
        listtoshow=[]
        for course in courselist:
            classid=course['id']
            # print(classid)
            classres=list(ClassHasRoom.objects.values('id','day','start_at','duration','Class_id').filter(Class_id=classid))
            # print(classres)
            for classres1 in classres:
                classres1['date']=numswitch(classres1['day'])
                classres1['timespan']=getspan(classres1['start_at'],classres1['duration'])
            listtoshow.append(classres)
        # print(listtoshow)
        course_dict={}
        for course in courselist:
            course_dict[course['course_id']]=[]
        for course in courselist:
            course_dict[course['course_id']].append(course)
        # print(course_dict)
        coursename=[]
        i=0
        for course_id,courseinfo in course_dict.items():
            # print(course_id)
            # print(courseinfo)
            course=list(Course.objects.values('name').filter(id=course_id))
            # classinfo=list(Class.objects.values('year','term').filter(course_id=course_id).filter(teacher_id=userid))
            # print(course)
            # extrainfo=list(ClassHasRoom.objects.values().filter())
            # course[0]['time']=classinfo
            course[0]['info_list']=courseinfo
            course[0]['class_list']=listtoshow[i]
            i+=1
            coursename.append(course[0])


        
        print(coursename)
        return render(request, "grade_detail_course.html", {
        'web_title': '成绩管理',
        'page_title': "成绩管理",
        'wholelist':coursename
    }) 

def grade_detail(request):
    courseid=0
    dict_p = request.POST
    for k,v in dict_p.items():
        if (v=='查看详情'):
            courseid=k
    courseinfo=list(Course.objects.values('id','name','credit').filter(id=courseid))
    classinfo=list(Class.objects.values('year','term').filter(course_id=courseid))
    # print(classinfo)
    courseinfo[0]['year']=classinfo[0]['year']
    courseinfo[0]['term']=classinfo[0]['term']
    gradeinfo=CourseResult.objects.all()
    # print("courseid:"+courseid)
    gradeinfolist=[]
    for gradein in gradeinfo:
        gradelist1=list(gradein.course.all().values('id','courseresult'))
        # print(gradelist1[0]['id'])
        # print(type(courseid))
        # print(type(gradelist1[0]['id']))
        if (gradelist1[0]['id'] == int(courseid)):
            courseresultid=gradelist1[0]['courseresult']
            gradeinfolist=list(CourseResult.objects.values().filter(id=courseresultid))
    # print(gradeinfolist)
    courseinfo[0]['class_performance']=gradeinfolist[0]['class_performance']
    courseinfo[0]['exam_result']=gradeinfolist[0]['exam_result']
    courseinfo[0]['final_result']=gradeinfolist[0]['final_result']
    courseinfo[0]['gp']=calculategp(gradeinfolist[0]['final_result'])
        # print(gradelist1)
    # print("gradeinfo"+gradeinfo)
    # print(courseinfo)

    return render(request,"grade_detail.html",{
        'web_title':'成绩详情',
        'page_title':'成绩详情',
        'detail_info':courseinfo
    })

# def detailcourseindex(request):
#     userid=request.user.id
#     courselist=Class.objects.values().filter(teacher_id=userid)
#     return render(request, "grade_detail_course.html", {
#         'web_title': '成绩管理',
#         'page_title': "成绩管理",
#     })

def detailclassindex(request):


    return render(request, "grade_detail_class.html", {
        'web_title': '成绩管理',
        'page_title': "成绩管理",
    })
def index_teacher(request):
    return render(request, "grade_mgt_teacher.html", {
        'web_title': '成绩管理',
        'page_title': "成绩管理",
    })

def updating(request):
    return render(request,"grade_detail_class_updating.html",{
        'webtitle':'成绩录入',
        'pagetitile':'成绩录入'
    })
def getspan(start,duration):
    i=duration-1
    res=start
    p=start
    while(i>0):
       res=res*10
       p=p+1
       res=res+p
       i-=1 
    return res
def numswitch(num):
    res="一"
    if (num==1):
        res="一"
    elif (num==2):
        res="二"
    elif (num==3):
        res="三"
    elif (num==4):
        res="四"
    elif (num==5):
        res="五"
    elif (num==6):
        res="六"
    else:
        res="七"
    return res
def calculategp(grade):
    gp=0
    if (grade>=95):
            gp=5.0
    elif (grade>=92):
        gp=4.8
    elif (grade>=89):
        gp=4.5
    elif (grade>=86):
        gp=4.2
    elif (grade>=83):
        gp=3.9
    elif (grade>=80):
        gp=3.6
    elif (grade>=77):
        gp=3.3
    elif (grade>=74):
        gp=3.0
    elif (grade>=71):
        gp=2.7
    elif (grade>=68):
        gp=2.4
    elif (grade>=65):
        gp=2.1
    elif (grade>=62):
        gp=1.8
    elif (grade>=60):
        gp=1.5
    else:
        gp=0
    return gp