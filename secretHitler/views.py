from django.shortcuts import render
from secretHitler.models import Game, Player
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from secretHitler.serializers import PlayerSerializer
import random


class GetGameStatus(APIView):
    def get(
        self,
        request,
        game_code=None,
        player_name=None,
    ):
        if not game_code or not player_name:
            return Response(
                {"message": "need game code and player name"},
                status=status.HTTP_403_FORBIDDEN,
            )

        num_of_ja_votes = Player.objects.filter(game__code=game_code, vote="ja").count()
        num_of_nein_votes = Player.objects.filter(
            game__code=game_code, vote="nein"
        ).count()
        player = Player.objects.get(player_name=player_name, game__code=game_code)
        return Response(
            {
                "player": PlayerSerializer(player).data,
                "num_of_ja_votes": num_of_ja_votes,
                "num_of_nein_votes": num_of_nein_votes,
            },
            status=status.HTTP_200_OK,
        )


class ResetVotes(APIView):
    def get(
        self,
        request,
        game_code=None,
    ):
        if not game_code:
            return Response(
                {"message": "need game code and player name"},
                status=status.HTTP_403_FORBIDDEN,
            )

        Player.objects.filter(game__code=game_code).update(vote=None)

        return Response(
            {
                "num_of_ja_votes": 0,
                "num_of_nein_votes": 0,
            },
            status=status.HTTP_200_OK,
        )


class ChooseVote(APIView):
    def get(self, request, game_code=None, player_name=None, vote_choice=None):
        if not game_code or not player_name or not vote_choice:
            return Response(
                {"message": "need game code and player name and vote choice"},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            player = Player.objects.get(player_name=player_name, game__code=game_code)
        except:
            return Response(
                {"message": "could not find the player with that name and code"},
                status=status.HTTP_403_FORBIDDEN,
            )
        player.vote = vote_choice
        player.save()
        num_of_ja_votes = Player.objects.filter(game__code=game_code, vote="ja").count()
        num_of_nein_votes = Player.objects.filter(
            game__code=game_code, vote="nein"
        ).count()
        return Response(
            {
                "num_of_ja_votes": num_of_ja_votes,
                "num_of_nein_votes": num_of_nein_votes,
            },
            status=status.HTTP_200_OK,
        )


class ResetRoles(APIView):
    def get(self, request, game_code=None, player_name=None):
        if not game_code or not player_name:
            return Response(
                {"message": "need game code and player name"},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            game = Game.objects.get(code=game_code)
        except:
            return Response(
                {"message": "no game with that code"},
                status=status.HTTP_403_FORBIDDEN,
            )

        num_of_liberals, num_of_fascists = game.getNumOfLiberalsFascists
        players = Player.objects.filter(game=game)

        players_obj = [{"pk": p.pk, "rando": random.random()} for p in players]
        players_sorted = sorted(players_obj, key=lambda x: x["rando"])
        for index, player_pk_num in enumerate(players_sorted):
            player = Player.objects.get(pk=player_pk_num["pk"])
            if index == 0:
                player.update(role="hitler", party="fascist")
            elif index <= num_of_liberals:
                player.update(role="liberal", party="liberal")
            else:
                player.update(role="fascist", party="fascist")

        og_player = Player.objects.get(player_name=player_name, game=game)
        return Response(
            {
                "role": og_player.role,
                "party": og_player.party,
            },
            status=status.HTTP_200_OK,
        )


class CreateGame(APIView):
    def get(self, request, num_of_players=None, player_name=None):
        if not num_of_players or not player_name:
            return Response(
                {"message": "need game code and player name"},
                status=status.HTTP_403_FORBIDDEN,
            )

        game = Game.objects.create()
        player = Player.objects.create(game=game, player_name=player_name)

        return Response(
            {"role": player.role, "party": player.party, "game_code": game.code},
            status=status.HTTP_200_OK,
        )
