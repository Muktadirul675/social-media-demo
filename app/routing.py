from django.urls import re_path 
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/room_chat/(?P<key>\w+[0-9]+)/', consumers.ChatConsumer.as_asgi())
]