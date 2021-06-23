from django.conf.urls import url
from django.urls import path
from django.views import generic
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('grade_detail',views.grade_detail,name="grade_detail"),
    path('grade_mgt_teacher',views.index_teacher,name="grade_mgt_teacher"),
    # path('grade_detail_course',views.detailcourseindex,name="grade_detail_course"),
    path('grade_detail_class',views.detailclassindex,name="grade_detail_class"),
    path('grade_detail_class_updating',views.updating,name="updating")
]
