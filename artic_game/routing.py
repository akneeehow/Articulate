from django.conf.urls import url
from django.urls import path,re_path

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator

from game.consumers import GameConsumer, OnlineRoomConsumer
from django.urls import path

websocket_urlpatterns=[
    path('ws/clicked/<room_name>/',GameConsumer.as_asgi(),name="clicked"),
    path('ws/online-rooms/',OnlineRoomConsumer.as_asgi())

]

application = ProtocolTypeRouter({

    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns
                [ 
                    path('game/create_room/',OnlineRoomConsumer.as_asgi())
                ]
            )
        )
    )
})
