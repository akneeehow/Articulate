from django.db import models
from django.contrib.auth import get_user_model

# 3rd party imports
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

User = get_user_model()


def user_directory_path(instance, filename):
    """
        A function to return path where image will be stored after uploading.
    """
    ext = filename.split(".")[-1]
    username = instance.user.username
    return f"img/profile_avatars/{username}/avatar_{username}.{ext}"


class UserProfile(models.Model):

    # User whose profile is to be created.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # User's Avatar
    avatar = ProcessedImageField(
        default='default_male.jpg',
        upload_to=user_directory_path,
        processors=[ResizeToFill(100, 100)],
        format='JPEG',
        options={'quality': 100},
        blank=True,
        null=True,
    )

    # Whether Email has been verified or not
    is_email_verified = models.BooleanField(default=False)

    total_custom_games_count = models.IntegerField(default=0, verbose_name="# of Custom Games Played")

    # Winning streak of player.
    winning_streak = models.IntegerField(default=0, verbose_name="Winning Streak")


    maximum_rating = models.IntegerField(default=500, verbose_name="Maximum Rating")

    is_online = models.BooleanField(default=False, verbose_name="Is Online")


    def __str__(self):
        return self.user.username

    



