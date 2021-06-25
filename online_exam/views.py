import pymysql
import requests
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
    return render(req, 'online_exam_test_info.html', {
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
        #generate_auto(course,user_id,chapterstart,chapterend);
        generate_auto(course,1,chapterstart,chapterend);
        return render(request,'online_exam_generate_paper_auto_end.html',{
            'web_title': '在线测验系统',
            'page_title': '生成试卷',
            'test_param': 'TEST PARAM',
        })

def generate_auto(course,teacher_id,chapterstart,chapterend):
    message = Course.objects.get(name=course)
    course_id = message.id
    chapterstart = int(chapterstart)
    chapterend = int(chapterend)
    questionlist = []
    questionidlist = []
    paperadd = Paper.objects.create(name='自动出卷',course_id=course_id,teacher_id=teacher_id,generate_time=timezone.now())
    for i in range(chapterstart,chapterend+1):
        quest = Question.objects.filter(course_id=course_id,chapter=i)
        print(quest)
        paperadd.questions.add(*quest)
    return

def generate_paper_handle(request):#手动出卷
    if request.method == 'POST':
        course = request.POST.get("course")
        message = Course.objects.get(name=course)
        resultset = Question.objects.filter(course_id=message.id)
        result = []
        for i in resultset:
            result.append((i.content,i.value,i.id))
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
    # paperID = req.GET.get('paperID')
    conn = pymysql.connect(host='43.129.73.191', port=3306, user='fse', password='xkxqjdTVgZRfjV2t', db='fse')
    cursor = conn.cursor()

    # cursor.execute(
    #     "select first_name,last_name,date,score from auth_user natural join online_exam_score where paper_id=%d" % paperID)
    # cursor.execute(
    #     "select first_name,last_name,date,score from auth_user natural join online_exam_score where paper_id=1234")
    cursor.execute("select first_name, last_name, date, score, student_id from auth_user, online_exam_score "
                   "where online_exam_score.student_id = auth_user.id and paper_id=1234")
    rst1 = cursor.fetchall()

    # cursor.execute(
    #     "select question_id,count(id) from online_exam_studentanswer "
    #     "where paper_id=%d and is_right=1 group by question_id" % paperID)
    cursor.execute(
        "select question_id,count(id) from online_exam_studentanswer where is_right=1 group by question_id")
    rst2 = cursor.fetchall()

    cursor.close()
    conn.close()
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

    conn = pymysql.connect(host='43.129.73.191', port=3306, user='fse', passwd='xkxqjdTVgZRfjV2t', db='fse')
    cursor = conn.cursor()
    # cursor.execute("select id from online_exam_paper where name='%s'" % (name))
    # result = cursor.fetchall()
    # cursor.execute("select student_id,date,score from online_exam_score where paper_id=%d" % (result[0][0]))
    # result2 = cursor.fetchall()
    cursor.execute("select id,name from online_exam_paper")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
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
        conn = pymysql.connect(host='43.129.73.191', port=3306, user='fse', passwd='xkxqjdTVgZRfjV2t', db='fse')
        cursor = conn.cursor()
        # cursor.execute("select id from online_exam_paper where name='%s'" % (name))
        # result = cursor.fetchall()
        # cursor.execute("select student_id,date,score from online_exam_score where paper_id=%d" % (result[0][0]))
        # result2 = cursor.fetchall()
        cursor.execute("select content,score,is_right from online_exam_studentanswer,online_exam_question "
                       "where student_id= %s and online_exam_studentanswer.question_id = online_exam_question.id and paper_id = %s", [student_id, id_select])
        result = cursor.fetchall()
        cursor.close()
        conn.close()
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
        conn = pymysql.connect(host='43.129.73.191', port=3306, user='fse', passwd='xkxqjdTVgZRfjV2t', db='fse')
        cursor = conn.cursor()
        # cursor.execute("select id from online_exam_paper where name='%s'" % (name))
        # result = cursor.fetchall()
        # cursor.execute("select student_id,date,score from online_exam_score where paper_id=%d" % (result[0][0]))
        # result2 = cursor.fetchall()
        # cursor.execute("select content,score,is_right from online_exam_studentanswer,online_exam_question where student_id= 1 and online_exam_studentanswer.question_id = online_exam_question.id and paper_id = %s",[id_select,])

        cursor.execute("select content,score,is_right from online_exam_studentanswer,online_exam_question "
                       "where student_id= %s and online_exam_studentanswer.question_id = online_exam_question.id and paper_id = %s",
                       [student_id, id_select])


        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return render(req, 'online_exam_stu_single.html', {
            'web_title': '在线测验系统',
            'page_title': '在线测验子系统',
            'test_param': 'TEST PARAM',
            'id_select': id_select,
            'student_id': student_id,
            'score_content': result
        })