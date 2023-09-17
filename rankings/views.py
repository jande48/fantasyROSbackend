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
from rankings.models import PlayerRank, Messages


class GetRankingsView(APIView):
    def get(self, request, league_scoring_type=None, source=None):
        if not league_scoring_type or not source:
            return Response(
                {"message": "need league type and source"},
                status=status.HTTP_403_FORBIDDEN,
            )
        players = PlayerRank.objects.filter(
            league_scoring_type=league_scoring_type, source=source
        ).order_by("rank")
        return Response(
            {
                "players": PlayerRankSerializer(players, many=True).data,
            },
            status=status.HTTP_200_OK,
        )


class SendMessage(APIView):
    def post(self, request):
        # this is the post body {"message": "heres the message","email_address":"jacob@gmail.com"}
        try:
            email = request.data["email_address"]
            message = request.data["message"]
            message_obj = Messages(email_address=email, message=message)
            message_obj.save()
            return Response(
                {
                    "message": "success",
                },
                status=status.HTTP_200_OK,
            )
        except:
            return Response(
                {
                    "message": "failure",
                },
                status=status.HTTP_200_OK,
            )
