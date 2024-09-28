
from django.urls import path
from a_wechat import consumers


websocket_urlpatterns = [
    path("ws/chatroom/<str:chatroom_name>/", consumers.ChatroomConsumer.as_asgi())
]