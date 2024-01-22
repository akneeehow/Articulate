from django.conf import settings
from django.shortcuts import render, reverse, HttpResponseRedirect, HttpResponse, Http404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.conf import settings
from .models import GameRoom
from user_profile.models import UserProfile
from channels.layers import get_channel_layer
from django.http import JsonResponse
from asgiref.sync import async_to_sync
import re
from django.views.decorators.csrf import csrf_exempt

ERROR = "error"
SUCCESS = "success"
MAX_JOINED_PLAYER_COUNT = 10
MINIMUM_ONLINE_PLAYER_REQUIRED = 0

channel_layer = get_channel_layer()

@login_required
def play_now(request):
    player = request.user
    if not player.is_authenticated:
        message = f"You need to login first!"
        return render(request, '404.html', {"message": message})

    player_profile = UserProfile.objects.get(user=player)
    if not player_profile.is_email_verified:
        messages.info(request, f"Your email is not verified.")
        return HttpResponseRedirect(reverse('user_profile', kwargs={"username": player.username}))

    if player_profile.is_league_changed != UserProfile.LEAGUE_STABLE:
        league_change_context = {
            "player": player,
            "profile": player_profile,
            "is_league_changed": player_profile.is_league_changed,
        }
        player_profile.is_league_changed = UserProfile.LEAGUE_STABLE
        player_profile.save()
        return render(request, 'game/league_changed.html', league_change_context)

    top_ratings = UserProfile.objects.order_by('-current_rating').filter(total_public_games_count__gt=0).values_list('current_rating', flat=True).distinct()
    top_players = UserProfile.objects.order_by('-current_rating').filter(total_public_games_count__gt=0).filter(current_rating__in=top_ratings[:10])
    context = {
        "top_players": top_players,
    }
    return render(request, 'game/play_now.html', context=context)

def CreateRoomView(request):
    return render(request,'game/create_room.html')

def GameView(request,room_name):
    if not re.match(r'^[\w-]*$', room_name):
        return render(request,'game/play_now.html')
    return render(request,'game/game.html')

@csrf_exempt
def roomExist(request,room_name):
    print(room_name)
    
    return JsonResponse({
        "room_exist":GameRoom.objects.filter(room_name=room_name).exists()
    })