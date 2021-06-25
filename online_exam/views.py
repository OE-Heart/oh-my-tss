import datetime
import random

import pymysql
from django.db import connection
from django.shortcuts import render,redirect
from info_mgt.models import Course
from online_exam.models import Question,Paper
from django.utils import timezone

# Create your views here.
def index(request):
    if request.method == 'POST':
        course = request.POST.get("course")
        chapter = request.POST.get("chapter")
        if course != '' or chapter != '':
            result = []
            if course!='' and chapter=='':
                message = Course.objects.get(name=course)
                resultset = Question.objects.filter(course_id=message.id)
                print(resultset)
                for i in resultset:
                    result.append((i.content,i.id))
            elif course=='' and chapter!='':
                return render(request, 'online_exam_main.html', {
                    'web_title': '在线测验系统',
                    'page_title': '在线测验子系统',
                    'test_param': 'TEST PARAM',
                    'emptysearch': '2'
                })
            else:
                message = Course.objects.filter(name=course)
                print(message)
                for i in message:
                    course_id = i.id
                resultset = Question.objects.filter(course_id=course_id,chapter=chapter)
                print(resultset)
                for i in resultset:
                    result.append((i.content,i.id))
            return render(request,'online_exam_search_out.html',{
                'web_title': '在线测验系统',
                'page_title': '进入题库',
                'test_param': 'TEST PARAM',
                'question_content': result,
                'course': course,
                'chapter': chapter
            })
        else:
            return render(request, 'online_exam_main.html', {
                'web_title': '在线测验系统',
                'page_title': '在线测验子系统',
                'test_param': 'TEST PARAM',
                'emptysearch': '1'
            })
    return render(request, 'online_exam_main.html', {
        'web_title': '在线测验系统',
        'page_title': '在线测验子系统',
        'test_param': 'TEST PARAM',
        'emptysearch': '0'
    })

def del_question(req):
    nid = req.GET.get('nid',None)
    course = req.GET.get('course',None)
    chapter = req.GET.get('chapter',None)
    delobj = Question.objects.get(id=nid)
    delobj.delete()
    #result = []
    # if course!='' and chapter=='':
    #     message = Course.objects.get(name=course)
    #     resultset = Question.objects.filter(course_id=message.id)
    #     print(resultset)
    #     for i in resultset:
    #         result.append((i.content,i.id))
    # else:
    #     message = Course.objects.filter(name=course)
    #     print(message)
    #     for i in message:
    #         course_id = i.id
    #     resultset = Question.objects.filter(course_id=course_id,chapter=chapter)
    #     print(resultset)
    #     for i in resultset:
    #         result.append((i.content,i.id))
    return redirect('/online_exam/')

def generate_paper(req):
    return render(req, 'online_exam_generate_paper.html', {
        'web_title': '在线测验系统',
        'page_title': '生成试卷',
        'test_param': 'TEST PARAM',
    })

def searchout(req):
    return render(req, 'online_exam_search_out.html', {
        'web_title': '在线测验系统',
        'page_title': '在线测验子系统',
        'test_param': 'TEST PARAM',
    })


def release(req):
    return render(req, 'online_exam_release_test.html', {
        'web_title': '在线测验系统',
        'page_title': '在线测验子系统',
        'test_param': 'TEST PARAM',
    })

def testinfo(req):
    conn = pymysql.connect(host='43.129.73.191', port=3306, user='fse', passwd='xkxqjdTVgZRfjV2t', db='fse')
    cursor = conn.cursor()
    list = []
    cursor.execute("select * from online_exam_test")
    tests = cursor.fetchall()
    for item in tests:
        cursor.execute("select course_id from online_exam_test_courses where test_id='%s'"%(item[0]))
        courseid = cursor.fetchall()
        cursor.execute("select count(*) from online_exam_test_students where test_id='%s'"%(item[0]))
        stu_num = cursor.fetchall()
        list.append((item[0],item[1],item[2],courseid[0][0],stu_num[0][0],item[3]))
    conn.close()
    time1 = datetime.datetime.now()
    return render(req, 'online_exam_test_info.html', {
        'list': list,
        'time1': time1,
        'web_title': '在线测验系统',
        'page_title': '在线测验子系统',
        'test_param': 'TEST PARAM',
    })

def calGrade(req):
    cursor = connection.cursor()
    dict = {'0': 'A', '1': 'B', '2': 'C', '3': 'D', '4': 'T', '5': 'F'}
    if req.method == 'POST':
        list = []
        num = req.POST.get('num')
        for i in range(int(num)):
            list.append(req.POST.get(str(i + 1)))
        conn = pymysql.connect(host='43.129.73.191', port=3306, user='fse', passwd='xkxqjdTVgZRfjV2t', db='fse')
        cursor = conn.cursor()
        testid = req.POST.get('testid')
        cursor.execute("select paper_id from online_exam_test where id='%s'" % (testid))
        pid = cursor.fetchall()
        cursor.execute("select * from online_exam_paper_questions where paper_id='%s'" % (pid[0][0]))
        result = cursor.fetchall()
        res = 0
        score = 0
        i = 0
        s_id = req.user.id
        for question in result:
            cursor.execute("select * from online_exam_question where id = '%s'" % (question[2]))
            result1 = cursor.fetchall()
            res += result1[0][4]
            q_id = question[0]
            if list[i][0] == dict[result1[0][3]]:
                score+=result1[0][4]
                #it = StudentAnswer.objects.create(paper_id = pid[0][0],question_id = q_id,is_right=True,student_id= s_id,score=result[0][4])
            else:
                pass
                #it = StudentAnswer.objects.create(paper_id=pid[0][0], question_id=q_id, is_right=False, student_id=s_id,
                #score=0)
            i+=1
            #it.save()
        weight = score/res
        time1 = datetime.datetime.now()
        print(score,weight)
        #it = Score.objects.create(paper_id=pid[0][0],student_id=s_id,score=score,weight=weight,date=time1)
        #it.save()
    return redirect('../stu_analysis/')

def stu_testinfo(req):
    conn = pymysql.connect(host='43.129.73.191', port=3306, user='fse', passwd='xkxqjdTVgZRfjV2t', db='fse')
    cursor = conn.cursor()
    list = []
    cursor.execute("select * from online_exam_test")
    tests = cursor.fetchall()
    time1 = datetime.datetime.now()
    for item in tests:
        cursor.execute("select course_id from online_exam_test_courses where test_id='%s'" % (item[0]))
        courseid = cursor.fetchall()
        cursor.execute("select count(*) from online_exam_test_students where test_id='%s'" % (item[0]))
        stu_num = cursor.fetchall()
        join = time1<item[1] and time1>item[2]
        list.append((item[0], item[1], item[2], courseid[0][0], stu_num[0][0], item[3],join))
    conn.close()
    return render(req,'online_exam_stu_testinfo.html', {
        'list':list,
        'web_title': '在线测验系统',
        'page_title': '在线测验子系统',
        'test_param': 'TEST PARAM',
    })
def stu_exam(req):
    if req.method == "GET":
        testid = req.GET.get('test_id')
        conn = pymysql.connect(host='43.129.73.191', port=3306, user='fse', passwd='xkxqjdTVgZRfjV2t', db='fse')
        cursor = conn.cursor()
        list = []
        time1 = datetime.datetime.now()
        cursor.execute("select course_id from online_exam_test_courses where test_id='%s'" % (testid))
        courseid = cursor.fetchall()
        cursor.execute("select count(*) from online_exam_test_students where test_id='%s'" % (testid))
        stu_num = cursor.fetchall()
        cursor.execute("select paper_id from online_exam_test where id='%s'" % (testid))
        pid = cursor.fetchall()
        cursor.execute("select start from online_exam_test where id='%s'" % (testid))
        start = cursor.fetchall()
        cursor.execute("select end from online_exam_test where id='%s'" % (testid))
        end = cursor.fetchall()
        cursor.execute("select count(*) from online_exam_paper_questions where paper_id='%s'"%(pid[0][0]))
        itemn = cursor.fetchall()
        list.append((testid, start[0][0], end[0][0], courseid[0][0], stu_num[0][0], pid[0][0],itemn[0][0],time1))
        list1 = []
        cursor.execute("select * from online_exam_paper_questions where paper_id='%s'" % (pid[0][0]))
        result = cursor.fetchall()
        for question in result:
            cursor.execute("select * from online_exam_question where id = '%s'" % (question[2]))
            result1 = cursor.fetchall()
            list1.append(( result1[0][2], result1[0][4]))
    return render(req,'online_exam_stu_exam.html', {
        'list1':list1,
        'list':list,
        'web_title': '在线测验系统',
        'page_title': '在线测验子系统',
        'test_param': 'TEST PARAM',
    })
def teach_detail(req):
    dict = {'0':'A','1' : 'B','2' : 'C', '3':'D','4':'T','5':'F'}
    if req.method == "GET":
        testid = req.GET.get('test_id')
        conn = pymysql.connect(host='43.129.73.191', port=3306, user='fse', passwd='xkxqjdTVgZRfjV2t', db='fse')
        cursor = conn.cursor()
        list = []
        time1 = datetime.datetime.now()
        cursor.execute("select course_id from online_exam_test_courses where test_id='%s'" % (testid))
        courseid = cursor.fetchall()
        cursor.execute("select count(*) from online_exam_test_students where test_id='%s'" % (testid))
        stu_num = cursor.fetchall()
        cursor.execute("select paper_id from online_exam_test where id='%s'"%(testid))
        pid = cursor.fetchall()
        cursor.execute("select start from online_exam_test where id='%s'"%(testid))
        start = cursor.fetchall()
        cursor.execute("select end from online_exam_test where id='%s'"%(testid))
        end = cursor.fetchall()
        list.append((testid,start[0][0],end[0][0] , courseid[0][0], stu_num[0][0],pid[0][0]))
        list1 = []
        cursor.execute("select * from online_exam_paper_questions where paper_id='%s'"%(pid[0][0]))
        result = cursor.fetchall()
        for question in result:
            cursor.execute("select * from online_exam_question where id = '%s'"%(question[2]))
            result1 = cursor.fetchall()
            list1.append((result1[0][1],result1[0][2],result1[0][4]))
    return render(req,'online_exam_teach_detail.html',{
        'list':list,
        'list1':list1,
        'web_title': '在线测验系统',
        'page_title': '在线测验子系统',
        'test_param': 'TEST PARAM',
    })

def generate_paper_auto(request):
    user_id = request.user.id
    if request.method == 'GET':
        return render(request,'online_exam_generate_paper_auto.html',{
            'web_title': '在线测验系统',
            'page_title': '自动生成试卷',
            'test_param': 'TEST PARAM',
            'majorlist': [{'id':1,'title':'123'},
                          {'id':2,'title':'123'}],
            'user_id': user_id
        })
    else:
        course = request.POST.get("course")
        chapterstart = request.POST.get("chapter1")
        chapterend = request.POST.get("chapter2")
        hard = request.POST.get('hard')
        totalscore = request.POST.get('totalscore')
        generate_auto(course,user_id,chapterstart,chapterend,hard,int(totalscore))
        return render(request,'online_exam_generate_paper_auto_end.html',{
            'web_title': '在线测验系统',
            'page_title': '生成试卷',
            'test_param': 'TEST PARAM',
        })

def generate_auto(course,teacher_id,chapterstart,chapterend,hard,totalscore):
    message = Course.objects.get(name=course)
    course_id = message.id
    chapterstart = int(chapterstart)
    chapterend = int(chapterend)
    questionlist = []
    name = '自动出卷'+str(timezone.now())
    total_score = 0
    paperadd = Paper.objects.create(name=name,course_id=course_id,teacher_id=teacher_id,generate_time=timezone.now())
    for i in range(chapterstart,chapterend+1):
        quest = Question.objects.filter(course_id=course_id,chapter=i)
        for j in quest:
            k = random.randint(1,10)
            if k>5:
                if total_score+j.value<=totalscore:
                    total_score+=j.value
                    paperadd.questions.add(j)
    return

def generate_paper_handle(request):#手动出卷
    if request.method == 'POST':
        course = request.POST.get("course")
        message = Course.objects.get(name=course)
        resultset = Question.objects.filter(course_id=message.id)
        result = []
        for i in resultset:
            result.append((i.content,i.value,i.id,i.difficulty))
        return render(request,'online_exam_generate_paper_handle_search.html',{
            'web_title': '在线测验系统',
            'page_title': '手动生成试卷',
            'test_param': 'TEST PARAM',
            'course': course,
            'questionlist': result
        })
    else:
        return render(request,'online_exam_generate_paper_handle.html',{
            'web_title': '在线测验系统',
            'page_title': '手动生成试卷',
            'test_param': 'TEST PARAM',
        })

def generate_paper_handle_end(request):
    if request.method == 'POST':
        course = request.POST.get('course')
        course_id = Course.objects.get(name=course).id
        uid = request.POST.getlist('uid')
        paperadd = Paper.objects.create(name='手动出卷',course_id=course_id,teacher_id=1,generate_time=timezone.now())
        for id in uid:
            quest = Question.objects.filter(id=int(id))
            paperadd.questions.add(*quest)
        return render(request,'online_exam_generate_paper_handle_end.html',{
            'web_title': '在线测验系统',
            'page_title': '手动生成试卷',
            'test_param': 'TEST PARAM',
        })

def add_question(request):
    if request.method == 'POST':
        course = request.POST.get('course')
        value = request.POST.get('value')
        chapter = request.POST.get('chapter')
        m_course = Course.objects.get(name=course)
        question_type = request.POST.get('question_type')
        right_answer = request.POST.get('right_answer')
        content = request.POST.get('content')
        dif = request.POST.get('difficulty')
        if len(content)>0 and right_answer!=None:
            Question.objects.create(course=m_course,type=question_type,content=content,answer=str(int(right_answer)-1),value=value,chapter=chapter,difficulty=dif)
        return redirect('/online_exam/')
    else:
        course = request.GET.get('course',None)
        return render(request,'online_exam_add_question.html',{
            'web_title': '在线测验系统',
            'page_title': '添加题目',
            'test_param': 'TEST PARAM',
            'course': course
        })

def combineanalysis(req):
    # 这里估计要根据html相应的改，暂且发送的请求里叫做paperID吧
    paperID = req.GET.get('paperID')
    cursor = connection.cursor()

    #cursor.execute(
    #     "select first_name,last_name,date,score from auth_user natural join online_exam_score where paper_id=%d" % paperID)
    #cursor.execute(
    #     "select first_name,last_name,date,score from auth_user natural join online_exam_score where paper_id=1234")
    cursor.execute("select first_name, last_name, date, score, student_id from auth_user, online_exam_score "
                   "where online_exam_score.student_id = auth_user.id and paper_id=%s",[paperID])
    rst1 = cursor.fetchall()
    print(rst1)
    # cursor.execute(
    #     "select question_id,count(id) from online_exam_studentanswer "
    #     "where paper_id=%d and is_right=1 group by question_id" % paperID)
    cursor.execute(
        "select question_id,count(id) from online_exam_studentanswer where is_right=1 group by question_id")
    rst2 = cursor.fetchall()
    return render(req, 'online_exam_combine_analysis.html', {
        'web_title': '在线测验系统',
        'page_title': '在线测验子系统',
        'test_param': 'TEST PARAM',
        'score_content': rst1,
        'correct': rst2
    })

def stusingleselect(req):

    # nid = req.GET.get('nid')
    # name = req.GET.get('name')
    student_id = req.GET.get('student_id')
    cursor = connection.cursor()
    # cursor.execute("select id from online_exam_paper where name='%s'" % (name))
    # result = cursor.fetchall()
    # cursor.execute("select student_id,date,score from online_exam_score where paper_id=%d" % (result[0][0]))
    # result2 = cursor.fetchall()
    cursor.execute("select id,name from online_exam_paper")
    result = cursor.fetchall()
    return render(req, 'online_exam_stu_single_select.html', {
        'web_title': '在线测验系统',
        'page_title': '在线测验子系统',
        'test_param': 'TEST PARAM',
        'student_id': student_id,
        'score_content': result
    })

def stusingle(req):
    if req.method == "GET":
        # nid = req.GET.get('nid')
        # name = req.GET.get('name')
        student_id = req.GET.get('student_id')

        id_select = '1234'
        cursor = connection.cursor()
        # cursor.execute("select id from online_exam_paper where name='%s'" % (name))
        # result = cursor.fetchall()
        # cursor.execute("select student_id,date,score from online_exam_score where paper_id=%d" % (result[0][0]))
        # result2 = cursor.fetchall()
        cursor.execute("select content,score,is_right from online_exam_studentanswer,online_exam_question "
                       "where student_id= %s and online_exam_studentanswer.question_id = online_exam_question.id and paper_id = %s", [student_id, id_select])
        result = cursor.fetchall()
        return render(req, 'online_exam_stu_single.html', {
            'web_title': '在线测验系统',
            'page_title': '在线测验子系统',
            'test_param': 'TEST PARAM',
            'id_select': 100000,
            'student_id': student_id,
            'score_content': result
        })
    else:
        # nid = req.GET.get('nid')
        # name = req.GET.get('name')
        id_select = req.POST.get("id_select")
        student_id = req.POST.get("student_id")
        cursor = connection.cursor()
        # cursor.execute("select id from online_exam_paper where name='%s'" % (name))
        # result = cursor.fetchall()
        # cursor.execute("select student_id,date,score from online_exam_score where paper_id=%d" % (result[0][0]))
        # result2 = cursor.fetchall()
        # cursor.execute("select content,score,is_right from online_exam_studentanswer,online_exam_question where student_id= 1 and online_exam_studentanswer.question_id = online_exam_question.id and paper_id = %s",[id_select,])

        cursor.execute("select content,score,is_right from online_exam_studentanswer,online_exam_question "
                       "where student_id= %s and online_exam_studentanswer.question_id = online_exam_question.id and paper_id = %s",
                       [student_id, id_select])


        result = cursor.fetchall()
        return render(req, 'online_exam_stu_single.html', {
            'web_title': '在线测验系统',
            'page_title': '在线测验子系统',
            'test_param': 'TEST PARAM',
            'id_select': id_select,
            'student_id': student_id,
            'score_content': result
        })
