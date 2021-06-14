from django.apps import AppConfig
from material.frontend.apps import ModuleMixin


class OnlineExamConfig(ModuleMixin, AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'online_exam'
    icon = '<i class="material-icons">adb</i>'
    display_name = '在线测验'
    index_url = '../online_exam'
    submodules = [
        {'name': 'main', 'text': '进入题库', 'link': './'},
        {'name': 'generate_paper', 'text': '生成试卷', 'link': './generate_paper'},
        {'name': 'release_test', 'text': '发布测试', 'link': './release_test'},
        {'name': 'test_info', 'text': '考试信息', 'link': './test_info'},
        {'name': 'paper_ana', 'text': '试卷分析', 'link': './paper_ana'},
    ]
