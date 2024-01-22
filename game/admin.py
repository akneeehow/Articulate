from django.contrib import admin
from.models import GameRoom,TrackPlayers

class TrackPlayersAdmin(admin.TabularInline):
    model = TrackPlayers

class RoomAdmin(admin.ModelAdmin):
   inlines = [TrackPlayersAdmin,]

admin.site.register(GameRoom,RoomAdmin)