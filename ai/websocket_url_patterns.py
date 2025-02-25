from django.urls import re_path

from ai import consumers

websocket_urlpatterns = [
    re_path(r"ws/v0/chat", consumers.ChatConsumer.as_asgi()),
]
