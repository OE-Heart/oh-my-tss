from django.apps import AppConfig
from material.frontend.apps import ModuleMixin


class ClassSelectionConfig(ModuleMixin, AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'class_selection'
    display_name = '在线选课'
    submodules = [
        {'name': 'stu_select', 'text': '学生选课', 'link': 'stu_select'},
    ]
