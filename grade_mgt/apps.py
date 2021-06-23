from django.apps import AppConfig
from material.frontend.apps import ModuleMixin

class GradeMgtConfig(ModuleMixin,AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'grade_mgt'
    icon = '<i class="material-icons">list</i>'
    display_name = '成绩管理'
