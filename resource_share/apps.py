from django.apps import AppConfig
from material.frontend.apps import ModuleMixin


class ResourceShareConfig(ModuleMixin,AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'resource_share'
    icon = '<i class="material-icons">folder</i>'
    display_name = '课程资源'
    submodules = [
        {'name':'homework','text':'作业管理','link':'homework'},
        {'name':'class_resource','text':'资源共享','link':''},
        
    ]

