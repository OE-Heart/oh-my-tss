from django.conf.urls import url
from django.urls import path
from django.views import generic
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('resource_share_detail/',views.rsdetail,name="rsdetail"),
    path('homework',views.homework,name="homework"),
    path('homework_detail',views.hwdetail,name="hwdetail"),
    path('homework_list',views.hwlist,name="hwlist"),
    path('homework_list_t',views.hwlist_t,name="hwlist_t"),
    path('homework_assign',views.hwass,name="homework_assign"),
    path('homework_detail_t',views.hwdetail_t,name="hwdetail_t"),
    path('addassignment',views.addassignment,name="addassignment"),
    path('homework_detail_t_update',views.homework_detail_update,name="homework_detail_t_update"),
    path('homework_delete',views.homeworkdelete,name="homework_delete"),
    path('up/', views.up, name="up"),
    # path('download/', views.down,name="download"),
    path('download/(?P<filename>.+)', views.down,name="download"),
    path("new/", views.new, name="new")


]
