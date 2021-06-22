from django.apps import AppConfig
from material.frontend.apps import ModuleMixin


class ClassSelectionConfig(ModuleMixin, AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'class_selection'
    display_name = '在线选课'
    submodules = [
        {'name': 'stu_select', 'text': '学生选课', 'link': 'stu_select'},
        {'name': 'stu_class', 'text': '学生课表', 'link': 'stu_class'},
        {'name': 'major_scheme', 'text': '培养方案', 'link': 'major_scheme'},
        {'name': 'tea_class', 'text': '教师课程', 'link': 'tea_class'},
        {'name': 'admin_class', 'text': '手动选课', 'link': 'admin_class'},
        {'name': 'time_control', 'text': '管理时间', 'link': 'time_control'},

    ]
