from django.urls import path
from rankings.views import GetRankingsView, SendMessage


urlpatterns = [
    path(
        "get_rankings/<str:league_scoring_type>/<str:source>/",
        GetRankingsView.as_view(),
    ),
    path(
        "get_rankings/<str:league_scoring_type>/<str:source>/<str:ranking_timescale>/",
        GetRankingsView.as_view(),
    ),
    path(
        "send_message/",
        SendMessage.as_view(),
    ),
]
