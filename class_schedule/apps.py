from django.apps import AppConfig
from material.frontend.apps import ModuleMixin


class ClassScheduleConfig(ModuleMixin, AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'class_schedule'
    # icon = '<i class="material-icons">account_circle</i>'
    display_name = '课程安排'
    submodules = [

    ]
