from django.conf.urls import include
from django.urls import path, re_path
from . import views

urlpatterns = [
    # path('/',  views.about, name='about'),
    # path('test_push/', views.UserChatView.push_notification),
    # re_path(r'^messages/new/', views.UserChatView.new_random_room, name='random_chat_room'),
    re_path(r'^messages/new/dedicated/$', views.UserChatView.new_room, name='new_chat_room'),
    re_path(r'^messages/(?P<label>[\w-]{,50})/$', views.UserChatView.chat_room, name='chat_room'),
]
