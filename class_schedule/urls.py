from django.urls import path
from django.views import generic
from . import views

urlpatterns = [
    # path('', generic.RedirectView.as_view(url='./main'), name='index'),
    path('', views.index, name='index'),
    path('add_room/', views.add_room, name='add_room'),
    path('add_room_submit/', views.add_room_submit, name='add_room_submit'),
    path('modify_room/', views.modify_room, name='modify_room'),
    path('modify_room_submit/<int:room_id>', views.modify_room_submit, name='modify_room_submit'),
    path('auto_schedule/', views.auto_schedule, name='auto_schedule'),
    path('do_auto_schedule/', views.do_auto_schedule, name='do_auto_schedule'),
    path('application/', views.application, name='application'),
    path('submit_application', views.submit_application, name='submit_application'),
    path('handle_application/', views.handle_application, name='handle_application'),
    path('submit_handle/<int:application_id>', views.submit_handle, name='submit_handle'),
    path('manipulate_schedule/', views.manipulate_schedule, name='manipulate_schedule'),
    path('submit_manipulate/<int:class_has_room_id>', views.submit_manipulate, name='manipulate_submit'),
    path('teacher_class/', views.teacher_class, name='teacher_class'),
    path('room_class/', views.room_class, name='room_class'),
]
