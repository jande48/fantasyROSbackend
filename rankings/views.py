from django.db.models import (
    BooleanField,
    Case,
    Count,
    Exists,
    ExpressionWrapper,
    F,
    Func,
    IntegerField,
    OuterRef,
    Q,
    Subquery,
    Value,
    When,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rankings.serializers import PlayerRankSerializer
from rankings.models import PlayerRank

class GetRankingsView(APIView):

    def get(self, request, league_scoring_type=None, source=None):
        if not league_scoring_type or not source:
            return Response({'message': 'need league type and source'},status=status.HTTP_403_FORBIDDEN)
        players = PlayerRank.objects.filter(league_scoring_type=league_scoring_type,source=source).order_by("rank")
        return Response(
            {
                "players": PlayerRankSerializer(players,many=True).data,
            },status=status.HTTP_200_OK,
        )