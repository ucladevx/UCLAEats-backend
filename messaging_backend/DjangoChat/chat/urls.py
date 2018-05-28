from django.conf.urls import include
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('',  views.about, name='about'),
    path('test_push/', views.push_notification),
    path('messages/new/', views.new_random_room, name='random_chat_room'),
    path('messages/new/dedicated/', views.new_room, name='new_chat_room'),
    re_path(r'^messages/(?P<label>[\w-]{,50})/$', views.chat_room, name='chat_room'),
]
