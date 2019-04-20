from django.conf.urls import include
from django.urls import path, re_path

from . import views

# room_messages = views.UserChatView.as_view({
#     'get': 'messages'
# })
#
# room_key = views.UserChatView.as_view({
#     'get': 'key'
# })

urlpatterns = [
    re_path(r'^messages/new/dedicated/$', views.new_chat_room, name='new-chat-room'),
    re_path(r'^messages/(?P<label>[\w-]{,50})/$', views.messages, name='room-messages'),
    re_path(r'^messages/key/(?P<label>[\w-]{,50})/$', views.key, name='room-key'),
]

# urlpatterns = format_suffix_patterns([
#     path('', api_root),
#     path('snippets/', snippet_list, name='snippet-list'),
#     path('snippets/<int:pk>/', snippet_detail, name='snippet-detail'),
#     path('snippets/<int:pk>/highlight/', snippet_highlight, name='snippet-highlight'),
#     path('users/', user_list, name='user-list'),
#     path('users/<int:pk>/', user_detail, name='user-detail')
# ])

# urlpatterns = [
#     # path('/',  views.about, name='about'),
#     # path('test_push/', views.UserChatView.push_notification),
#     # re_path(r'^messages/new/', views.UserChatView.new_random_room, name='random_chat_room'),
#     re_path(r'^messages/new/dedicated/$', views.new_chat_room, name='new_chat_room'),
#     re_path(r'^messages/(?P<label>[\w-]{,50})/$', views.UserChatView.as_view(), name='get_messages'),
#     # re_path(r'^key/(?P<label>[\w-]{,50})/$', views.UserChatView.as_view(), name='get_key'),
# ]
