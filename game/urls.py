from django.urls import path, include
from . import views

urlpatterns = [
    path('enter_room/<str:game_type>/<str:unique_id>/', views.enter_game_room, name="enter_game_room"),
    path('proceed_to_game/<str:game_type>/<str:unique_id>/', views.proceed_to_game, name="proceed_to_game"),

    path('play_now/', views.play_now, name="play_now"),



]
