import asyncio
import json
from django.contrib.auth import get_user_model
from django.utils import timezone
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from channels.exceptions import StopConsumer

from user_profile.models import UserProfile
from .models import GameHistory, Participant
from .helper import Card, PlayerServer, GameServer, Deck, CustomEncoder

User = get_user_model()


class GameRoomConsumer(AsyncConsumer):
    """
        A Consumer which will consume (handle) events related to Game Room
    """

    async def websocket_connect(self, event):
        self.me = self.scope['user']

        self.unique_id = self.scope['url_route']['kwargs']['unique_id']

        self.game_type = int(self.scope['url_route']['kwargs']['game_type'])

        self.user_profile_obj = await self.get_user_profile_obj()

        league = None
        if self.game_type == GameServer.PUBLIC:
            league = self.user_profile_obj.current_league

        self.game_room_id = f"game_room_{self.unique_id}"

        self.player_server_obj = PlayerServer(username=self.me.username,
                                              rating_before_start=self.user_profile_obj.current_rating)

        self.game = GameServer.create_new_game(unique_id=self.unique_id, player=self.player_server_obj,
                                               game_type=self.game_type, league=league)

        if self.game is None:
            # Connection is rejected because this room is already full.
            return

        await self.channel_layer.group_add(
            self.game_room_id,
            self.channel_name
        )
        await self.send({
            "type": "websocket.accept"
        })

    async def websocket_receive(self, event):
        front_text = event.get('text', None)

        if front_text:
            loaded_dict_data = json.loads(front_text)
            type_of_event = loaded_dict_data['type']
            text_of_event = loaded_dict_data['text']

            if type_of_event == "start.game":
                # print(f"Before Broadcasting: Going to call start.game")
                self.game.start_game()

                # await self.create_game_history()
                self.game.end_game()
            elif type_of_event == "play.card":
                client_data = text_of_event['data']
                server_data = {
                    "username": self.me.username,
                }
                returned_data = None
                if self.game.is_valid_play_move(client_data=client_data, server_data=server_data):
                    returned_data = self.game.play_card(client_data=client_data)
                    if returned_data:
                        if returned_data['status'] == "won":
                            won_data = returned_data
                            winner_username = won_data['username']
                            winner_score = int(won_data['score'])
                            if winner_score >= GameServer.WINNING_SCORE:
                                text_of_event['status'] = "won_game"
                                type_of_event = "won_game"

                                for player_obj in self.game.players:
                                    if player_obj.username == winner_username:
                                        await self.handle_winning_game(winner_player_obj=player_obj)
                                    else:
                                        await self.handle_losing_game(loser_player_obj=player_obj)

                                # Creating Game History in Database
                                await self.create_game_history()

                                print(f"End Game. {winner_username} has scored winning points.")
                            else:
                                text_of_event['status'] = "won_round"
                                type_of_event = "won_round"

                                await self.handle_winning_round(winner_username=winner_username)

                                print(f"This round ended. Get ready for next round.")

                        elif returned_data['status'] == "skipped":
                            forced_draw_data = returned_data

            if self.game is not None:
                game_data = json.dumps(self.game.prepare_client_data(), cls=CustomEncoder)
            else:
                game_data = None

            response = {
                "status": text_of_event['status'],
                "message": text_of_event['message'],
                "data": text_of_event['data'],
                "gameData": game_data,
            }

            if type_of_event == "won_game":
                extra_data = {
                    "wonGameData": json.dumps(self.game.players, cls=CustomEncoder)
                }
                response.update(extra_data)
                self.game.end_game()


            if won_data:
                extra_data = {
                    "wonData": won_data,
                }
                response.update(extra_data)


            await self.channel_layer.group_send(
                self.game_room_id,
                {
                    "type": type_of_event,
                    "text": json.dumps(response)
                }
            )

            if type_of_event == "user.new":
                if self.game.game_type == GameServer.CUSTOM:
                    if self.game.get_count_of_players() == 10:
                        GameServer.AVAILABLE_FRIEND_GAMES.remove(self.game)

    async def change_scene(self, event):
        await self.send({
            "type": "websocket.send",
            "text": event['text']
        })

    async def update_current_player(self, event):
        await self.send({
            "type": "websocket.send",
            "text": event['text']
        })


    async def user_new(self, event):
        await self.send({
            "type": "websocket.send",
            "text": event['text']
        })

    async def won_game(self, event):
        await self.send({
            "type": "websocket.send",
            "text": event['text']
        })


    async def enter_room(self, event):
        # This method actually sends the message
        await self.send({
            "type": "websocket.send",
            "text": event['text']
        })

    async def broadcast_notification(self, event):
        await self.send({
            "type": "websocket.send",
            "text": event['text']
        })

    async def start_game(self, event):
        text = event.get('text', None)
        if text:
            loaded_dict_data = json.loads(text)
            extra_data = {
                "serializedPlayer": json.dumps(self.player_server_obj, cls=CustomEncoder),
            }
            loaded_dict_data.update(extra_data)
            await self.send({
                "type": "websocket.send",
                "text": json.dumps(loaded_dict_data)
            })

    async def end_game(self, event):
        await self.send({
            "type": "websocket.send",
            "text": event['text']
        })

    async def websocket_disconnect(self, event):
        print("disconnected", event)
        # Leaving current Game
        if self.game is not None:
            me = self.me
            self.game.leave_game(self.player_server_obj)
            del self.player_server_obj
            response = {
                "status": "user_left_room",
                "message": "Disconnecting...",
                "data": {
                    "left_user_username": me.username,
                    "game_room_unique_id": self.game_room_id
                },
                "gameData": json.dumps(self.game.prepare_client_data(), cls=CustomEncoder)
            }
            await self.channel_layer.group_send(
                self.game_room_id,
                {
                    "type": "user_left_room",
                    "text": json.dumps(response)
                }
            )

            await self.channel_layer.group_discard(
                self.game_room_id,
                self.channel_name
            )

    async def user_left_room(self, event):
        await self.send({
            "type": "websocket.send",
            "text": event['text'],
        })

    @database_sync_to_async
    def get_user_profile_obj(self):
        me = self.me
        return UserProfile.objects.get(user=me)

    @database_sync_to_async
    def handle_winning_round(self, winner_username):
        """
        Updates the XP of player who won the round.
        :param winner_username: Username of player who won the round.
        :return:
        """
        round_winner = User.objects.get(username=winner_username)

        round_winner_profile = UserProfile.objects.get(user=round_winner)

        round_winner_profile.xp += UserProfile.WIN_ROUND_XP

        round_winner_profile.save()

    @database_sync_to_async
    def handle_winning_game(self, winner_player_obj):
        """
        Updates the value in the database when a user wins the game.
        :param winner_player_obj: Player Server object of winner.
        :return:
        """
        winner_username = winner_player_obj.username

        # Fetching User object.
        winner = User.objects.get(username=winner_username)

        # Fetching UserProfile object.
        winner_profile = UserProfile.objects.get(user=winner)

        if self.game_type == GameServer.PUBLIC:
            winner_profile.total_public_games_count += 1
            winner_profile.won_public_games_count += 1
        elif self.game_type == GameServer.CUSTOM:
            winner_profile.total_custom_games_count += 1
            winner_profile.won_custom_games_count += 1

        # Updating winning streak
        winner_profile.winning_streak += 1

        # Updating the xp
        winner_profile.xp += (UserProfile.WIN_GAME_XP + UserProfile.PARTICIPATION_XP)

        if self.game_type == GameServer.PUBLIC:
            # Updating current rating
            winner_profile.current_rating += winner_player_obj.rating_change

            # Updating maximum rating
            winner_profile.maximum_rating = max(winner_profile.maximum_rating, winner_profile.current_rating)

            league = winner_profile.current_league
            updated_league = winner_profile.get_current_league()
            if winner_player_obj.rating_change > 0:
                if league != updated_league:
                    winner_profile.is_league_changed = UserProfile.LEAGUE_UPGRADED
            elif winner_player_obj.rating_change < 0:
                if league != updated_league:
                    winner_profile.is_league_changed = UserProfile.LEAGUE_DEGRADED

            winner_profile.current_league = updated_league

        winner_profile.save()

    @database_sync_to_async
    def handle_losing_game(self, loser_player_obj):
        """
        Updates the value in the database when a user loses the game.
        :param loser_player_obj: Player Server object of Loser.
        :return:
        """

        loser_username = loser_player_obj.username

        loser = User.objects.get(username=loser_username)

        loser_profile = UserProfile.objects.get(user=loser)

        # Increasing Game Count
        if self.game_type == GameServer.PUBLIC:
            loser_profile.total_public_games_count += 1
        elif self.game_type == GameServer.CUSTOM:
            loser_profile.total_custom_games_count += 1

        # Resetting Winning streak
        loser_profile.winning_streak = 0

        # Updating xp
        loser_profile.xp += UserProfile.PARTICIPATION_XP

        if self.game_type == GameServer.PUBLIC:
            # Updating current rating
            loser_profile.current_rating += loser_player_obj.rating_change

            # Updating maximum rating
            loser_profile.maximum_rating = max(loser_profile.maximum_rating, loser_profile.current_rating)

            league = loser_profile.current_league
            updated_league = loser_profile.get_current_league()
            if loser_player_obj.rating_change > 0:
                if league != updated_league:
                    loser_profile.is_league_changed = UserProfile.LEAGUE_UPGRADED
            elif loser_player_obj.rating_change < 0:
                if league != updated_league:
                    loser_profile.is_league_changed = UserProfile.LEAGUE_DEGRADED

            loser_profile.current_league = updated_league

        loser_profile.save()

    @database_sync_to_async
    def create_game_history(self):
        if self.game is not None:
            unique_id = self.game.unique_id
            winner_username = self.game.winner
            game_type = None
            if self.game_type == GameServer.PUBLIC:
                game_type = GameHistory.PUBLIC
            elif self.game_type == GameServer.CUSTOM:
                game_type = GameHistory.CUSTOM

            game_room_history = GameHistory.objects.create(unique_game_id=unique_id, game_type=game_type,
                                                           winner_username=winner_username)
            player_objs = self.game.players
            for player_obj in player_objs:
                player_username = player_obj.username
                player_score = player_obj.score
                if self.game_type == GameServer.PUBLIC:
                    player_rating_change = player_obj.rating_change
                    player_seed = player_obj.seed
                else:
                    player_rating_change = 0
                    player_seed = 0.0
                player = User.objects.get(username=player_username)
                Participant.objects.create(user=player, game_room=game_room_history, score=player_score,
                                           rating_change=player_rating_change, seed=player_seed)
        return None