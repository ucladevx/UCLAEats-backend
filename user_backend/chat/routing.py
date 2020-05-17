from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'chat/(?P<room_label>\w+)/$', consumers.ChatConsumer), # api/vx/chat/chat/<room_label>
]
