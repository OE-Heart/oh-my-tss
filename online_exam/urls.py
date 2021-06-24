from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    #path('main/', views.index),
    path('del_question/',views.del_question),
    path('generate_paper/', views.generate_paper),
    path('search_out/', views.searchout),
    path('add_question/', views.add_question),
    path('search_out/add_question/', views.add_question),
    path('release_test/', views.release),
    path('test_info/', views.testinfo, name="test_info"),
    path('generate_paper/auto/',views.generate_paper_auto),
    path('generate_paper_auto_end/',views.generate_paper_auto),
    path('generate_paper/handle/',views.generate_paper_handle),
    path('generate_paper/handle_end/',views.generate_paper_handle_end),
    path('combine_analysis/', views.combineanalysis, name="combine_analysis"),
    path('stu_single/', views.stusingle, name="stu_single"),
    path('stu_single_select/', views.stusingleselect, name="stu_single_select")
]

