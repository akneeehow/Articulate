from django.urls import path, include
from . import views

urlpatterns = [
    path('play_now/', views.play_now, name="play_now"),
    path('create_room', views.CreateRoomView , name="create_room"),
    path('<str:room_name>/', views.GameView , name="game"),
    path('room/check_room/<room_name>/', views.roomExist , name="check_room"),

]
