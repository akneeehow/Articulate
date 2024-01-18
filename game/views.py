from django.conf import settings
from django.shortcuts import render, reverse, HttpResponseRedirect, HttpResponse, Http404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.conf import settings
from .models import GameRoom, Player, id_generator

from user_profile.models import UserProfile

from channels.layers import get_channel_layer
import json
from asgiref.sync import async_to_sync

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





def proceed_to_game(request, game_type, unique_id):
    """
    View to show game room tutorial.
    :param request:
    :param game_type:
    :param unique_id:
    :return:
    """
    context = {
        "game_type": game_type,
        "unique_id": unique_id,
    }
    return render(request, 'game/info.html', context)


@login_required
def enter_game_room(request, game_type, unique_id):
    player = request.user
    player_profile = UserProfile.objects.get(user=player)
    
    if not player_profile.is_email_verified:
        messages.info(request, "Your email is not verified.")
        return HttpResponseRedirect(reverse('user_profile', kwargs={"username": player.username}))
    
    if not player.is_authenticated:
        error_message = "Login / Signup to enter a Game Room."
        return render(request, '404.html', {"message": error_message})
    
    context = {
        'unique_id': unique_id,
        'peer_js_host_name': settings.PEER_JS_HOST_NAME,
        'peer_js_port_number': settings.PEER_JS_PORT_NUMBER,
    }
    return render(request, 'game/enter_game_room.html', context)
