from django.conf.urls import include
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('api/v1/messaging/',  views.about, name='about'),
    path('api/v1/messaging/test_push/', views.push_notification),
    path('api/v1/messaging/messages/new/', views.new_random_room, name='random_chat_room'),
    path('api/v1/messaging/messages/new/dedicated/', views.new_room, name='new_chat_room'),
    re_path(r'^api/v1/messaging/messages/(?P<label>[\w-]{,50})/$', views.chat_room, name='chat_room'),
]
