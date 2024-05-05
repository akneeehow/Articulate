from django.urls import path
from . import views



urlpatterns = [
    path('play_now/', views.play_now, name="play_now"),
    path('create_room/', views.CreateRoomView , name="create_room"),

]
