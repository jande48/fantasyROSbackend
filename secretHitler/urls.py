from django.urls import path
from secretHitler.views import (
    GetGameStatus,
    ResetVotes,
    ChooseVote,
    ResetRoles,
    CreateGame,
)


urlpatterns = [
    path(
        "game-status/<str:game_code>/<str:player_name>/",
        GetGameStatus.as_view(),
    ),
    path(
        "reset-votes/<str:game_code>/",
        ResetVotes.as_view(),
    ),
    path(
        "vote/<str:game_code>/<str:player_name>/<str:vote_choice>/",
        ChooseVote.as_view(),
    ),
    path(
        "reset-roles/<str:game_code>/<str:player_name>/",
        ResetRoles.as_view(),
    ),
    path(
        "create-game/<str:num_of_players>/<str:player_name>/",
        CreateGame.as_view(),
    ),
]
