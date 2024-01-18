# Generated by Django 3.1.2 on 2020-10-25 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0003_userprofile_total_games_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='current_league',
            field=models.IntegerField(choices=[(1, 'Noobie'), (2, 'Expert'), (3, 'Champion'), (4, 'Universe Boss')], default=1, verbose_name='Current League'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='maximum_league',
            field=models.IntegerField(choices=[(1, 'Noobie'), (2, 'Expert'), (3, 'Champion'), (4, 'Universe Boss')], default=1, verbose_name='Maximum League'),
        ),
    ]
