from rest_framework import serializers
from rankings.models import PlayerRank


class PlayerRankSerializer(serializers.ModelSerializer):
    # name = serializers.SerializerMethodField("get_name")
    # def get_name(self, obj=None):
    #     if obj and obj.first_name:
    #         first_name = obj.first_name
    #     else:
    #         first_name = " "
    #     if obj and obj.last_name:
    #         last_name = obj.last_name
    #     else:
    #         last_name = " "
    #     return first_name + " " + last_name

    class Meta:
        model = PlayerRank
        fields = [
            "id",
            "source",
            "league_scoring_type",
            "rank",
            "full_name",
            "team_name_abbreviation",
            "first_name",
            "last_name",
            "player_position",
            "player_image",
            "sleeper_id",
            "player_yahoo_id"
        ]
