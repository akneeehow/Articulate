from django.contrib import admin
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'maximum_rating','is_email_verified','total_custom_games_count',  'winning_streak']


admin.site.register(UserProfile, UserProfileAdmin)
