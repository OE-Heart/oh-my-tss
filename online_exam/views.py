import pymysql
from django.shortcuts import render,redirect


# Create your views here.
def index(request):
    if request.method == 'POST':
        course = request.POST.get("course")
        chapter = request.POST.get("chapter")
        if course != '' or chapter != '':
            #数据库操作
            conn = pymysql.connect(host='43.129.73.191',port=3306,user='fse',passwd='xkxqjdTVgZRfjV2t',db='fse')
            cursor = conn.cursor()

            if course!='' and chapter=='':
                cursor.execute("select id,name from info_mgt_course where name='%s'"%(course))
                result = cursor.fetchall()
                cursor.execute("select content from online_exam_question where course_id=%d"%(result[0][0]))
                result2 = cursor.fetchall()
            elif course=='' and chapter!='':
                return render(request, 'online_exam_main.html', {
                    'web_title': '在线测验系统',
                    'page_title': '在线测验子系统',
                    'test_param': 'TEST PARAM',
                    'emptysearch': '2'
                })
            else:
                cursor.execute("select id,name from info_mgt_course where name='%s'"%(course))
                result = cursor.fetchall()
                cursor.execute("select content,id from online_exam_question where course_id=%d and chapter=%d"%(result[0][0],int(chapter)))
                result2 = cursor.fetchall()
            cursor.close()
            conn.close()
            print(result2)
            return render(request,'online_exam_search_out.html',{
                'web_title': '在线测验系统',
                'page_title': '在线测验子系统',
                'test_param': 'TEST PARAM',
                'question_content': result2,
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
    nid = req.GET.get('nid')
    course = req.GET.get('course')
    chapter = req.GET.get('chapter')
    conn = pymysql.connect(host='43.129.73.191',port=3306,user='fse',passwd='xkxqjdTVgZRfjV2t',db='fse')
    cursor = conn.cursor()

    cursor.execute("delete from online_exam_question where id=%d"%(int(nid)))
    conn.commit()
    if chapter=='':
        cursor.execute("select id,name from info_mgt_course where name='%s'"%(course))
        result = cursor.fetchall()
        cursor.execute("select content from online_exam_question where course_id=%d"%(result[0][0]))
        result2 = cursor.fetchall()
    else:
        cursor.execute("select id,name from info_mgt_course where name='%s'"%(course))
        result = cursor.fetchall()
        cursor.execute("select content,id from online_exam_question where course_id=%d and chapter=%d"%(result[0][0],int(chapter)))
        result2 = cursor.fetchall()
    cursor.close()
    conn.close()
    return render(req,'online_exam_search_out.html',{
        'web_title': '在线测验系统',
        'page_title': '在线测验子系统',
        'test_param': 'TEST PARAM',
        'question_content': result2,
        'course': course,
        'chapter': chapter
    })


def generate_paper(req):
    return render(req, 'online_exam_generate_paper.html', {
        'web_title': '在线测验系统',
        'page_title': '在线测验子系统',
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

def paperanalysis(req):
    return render(req, 'online_exam_paper_analysis.html', {
        'web_title': '在线测验系统',
        'page_title': '在线测验子系统',
        'test_param': 'TEST PARAM',
    })
