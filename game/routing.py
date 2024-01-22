from .consumers import GameConsumer, OnlineRoomConsumer
from django.urls import path

websocket_urlpatterns=[
    path('ws/clicked/<room_name>/',GameConsumer.as_asgi(),name="clicked"),
    path('ws/online-rooms/',OnlineRoomConsumer.as_asgi())

]