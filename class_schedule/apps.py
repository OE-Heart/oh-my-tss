from django.apps import AppConfig
from material.frontend.apps import ModuleMixin


class ClassScheduleConfig(ModuleMixin, AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'class_schedule'
    icon = '<i class="material-icons">schedule</i>'
    display_name = '课程安排'
    submodules = [
        {'name': 'add_room', 'text': '添加教室', 'link': './add_room'},
        {'name': 'modify_room', 'text': '修改教室信息', 'link': './modify_room'},
        {'name': 'auto_schedule', 'text': '自动排课', 'link': './auto_schedule'},
        {'name': 'manipulate_schedule', 'text': '手动课程调整', 'link': './manipulate_schedule'},
        {'name': 'application', 'text': '调课申请', 'link': './application'},
        {'name': 'handle_application', 'text': '处理调课申请', 'link': './handle_application'},
        {'name': 'handle_application', 'text': '处理排课申请', 'link': './handle_application'},
        {'name': 'teacher_class', 'text': '教师课表查询', 'link': './teacher_class'},
        {'name': 'room_class', 'text': '教室课表查询', 'link': './room_class'},
    ]
