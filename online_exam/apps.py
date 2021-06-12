from django.apps import AppConfig
from material.frontend.apps import ModuleMixin


class OnlineExamConfig(ModuleMixin, AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'online_exam'
    icon = '<i class="material-icons">adb</i>'
    index_url = '../online_exam/'
    display_name = '在线测验'
    submodules = [
        {'name': 'gointo_question_db', 'text': '进入题库', 'link': './main'},
        {'name': 'gointo_question_db', 'text': '生成试卷', 'link': './generate_paper'},
        {'name': 'gointo_question_db', 'text': '发布测试', 'link': './release_test'},
        {'name': 'gointo_question_db', 'text': '考试信息', 'link': './test_info'},
        {'name': 'gointo_question_db', 'text': '试卷分析', 'link': './paper_ana'},
    ]
