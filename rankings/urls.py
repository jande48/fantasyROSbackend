from django.urls import path
from rankings.views import GetRankingsView


urlpatterns = [
    path(
        "get_rankings/<str:league_scoring_type>/<str:source>/",
        GetRankingsView.as_view(),
    ),
]