from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$',  views.about, name='about'),
    url(r'^new/$', views.new_random_room, name='random_chat_room'),
    url(r'^new/dedicated/$', views.new_room, name='new_chat_room'),
    url(r'^(?P<label>[\w-]{,50})/$', views.chat_room, name='chat_room'),
    url(r'^test_push/$', views.push_notification),
]
