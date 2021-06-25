from django.contrib import admin
from .models import Building, Classroom, ClassHasRoom, Application
from info_mgt.models import Class, Campus, Major, MajorHasCourse, Department, Course

# Register your models here.
admin.site.register(Building)
admin.site.register(Classroom)
admin.site.register(ClassHasRoom)
admin.site.register(Application)
admin.site.register(Class)
admin.site.register(Campus)
admin.site.register(Major)
admin.site.register(MajorHasCourse)
admin.site.register(Department)
admin.site.register(Course)