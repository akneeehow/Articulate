import json
import math
import string
from json import JSONEncoder
import random
from django.conf import settings

def delete_object(object_):
    del object_


class CustomEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__



class GameServer:
    PUBLIC, CUSTOM = 0, 1
    PUBLIC_ROOM_LIMIT = 2
    WINNING_SCORE = int(settings.WINNING_THRESHOLD_SCORE)
    AVAILABLE_FRIEND_GAMES = []
    AVAILABLE_PUBLIC_GAMES = []
    # TODO: What will happen if deck runs out of cards. -- Kshitiz

    def __init__(self, unique_id, player, game_type, league=None):
        self.unique_id = unique_id
        self.game_type = game_type
        self.league = league
        self.admin_username = player.username
        self.players = []
        self.player_usernames = []
        self.players.append(player)
        self.player_usernames.append(player.username)

        self.is_game_running = False
        self.direction = "+"
        self.current_player_index = 0
        self.previous_player_index = -1
        self.winner = None

    def __del__(self):
        print(f"Game with unique ID {self.unique_id} is deleted.")

    @classmethod
    def create_new_game(cls, unique_id, player, game_type, league):
        if game_type == cls.PUBLIC:
            for public_game in cls.AVAILABLE_PUBLIC_GAMES:
                if public_game.unique_id == unique_id:
                    if public_game.get_count_of_players() < 10:
                        print("Returning Existing Public Game.")
                        public_game.players.append(player)
                        public_game.player_usernames.append(player.username)
                        return public_game
                    return None
            print("Creating New Public Game.")
            new_public_game = GameServer(unique_id, player=player, game_type=game_type, league=league)
            cls.AVAILABLE_PUBLIC_GAMES.append(new_public_game)
            return new_public_game
        elif game_type == cls.CUSTOM:
            for friend_game in cls.AVAILABLE_FRIEND_GAMES:
                if friend_game.unique_id == unique_id:
                    if friend_game.get_count_of_players() < 10:
                        print("Returning Existing Custom Game.")
                        friend_game.players.append(player)
                        friend_game.player_usernames.append(player.username)
                        return friend_game
                    return None
            print("Creating New Custom Game.")
            new_friend_game = GameServer(unique_id, player=player, game_type=game_type, league=league)
            cls.AVAILABLE_FRIEND_GAMES.append(new_friend_game)
            return new_friend_game