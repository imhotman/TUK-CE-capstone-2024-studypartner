# chatting/routing.py

from django.urls import re_path
from . import consumers

# websocket_urlpatterns = [
#     re_path(r'ws/chat/(?P<room_name>\d+)/$', consumers.ChatConsumer.as_asgi()),
# ]

# websocket_urlpatterns = [
#     re_path(r'^ws/chat/(?P<room_name>[^/]+)/$', consumers.ChatConsumer.as_asgi()),
# ]

# from django.urls import re_path

# from . import consumers

# websocket_urlpatterns = [
#     re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
# ]
# chat/routing.py


websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
]