from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('main/', views.index),
    path('del_question/',views.del_question),
    path('generate_paper/', views.generate_paper),
    path('search_out/', views.searchout),
    path('release_test/', views.release),
    path('test_info/', views.testinfo, name="test_info"),
    path('paper_ana/', views.paperanalysis, name="paper_ana")
]
