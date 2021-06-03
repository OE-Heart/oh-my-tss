from django.apps import AppConfig
from material.frontend.apps import ModuleMixin

class InfoMgtConfig(ModuleMixin, AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'info_mgt'
    icon = '<i class="material-icons">account_circle</i>'
    display_name = '信息管理'