from rest_framework import serializers
from secretHitler.models import Player, Game


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = [
            "id",
            "created_at",
            "name",
            "vote",
            "party",
            "role",
        ]


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = [
            "id",
            "created_at",
            "num_of_players",
            "code",
        ]
