from django.urls import path
from info_mgt import views

urlpatterns = [
    path('', views.index)
]
