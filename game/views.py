
from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from user_profile.models import UserProfile
from channels.layers import get_channel_layer





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


    return render(request, 'game/play_now.html')

def CreateRoomView(request):
    if request.method == 'POST':
            player = request.user
            player_profile = UserProfile.objects.get(user=player)
            player_profile.total_custom_games_count += 1
            player_profile.save()
    return render(request,'game/create_room.html')
