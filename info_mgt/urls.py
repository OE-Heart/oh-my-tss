from django.urls import path
from django.views import generic
from . import views

urlpatterns = [
    # path('', generic.RedirectView.as_view(url='./main'), name='index'),
    path('', views.index, name='index'),
    path('account', views.account_list, name='account_list'),
    path('course/<int:page>', views.course_list, name='course_list'),
]
