from __future__ import annotations

import debug_toolbar
from django.urls import include, path

from owela_club import views

urlpatterns = [
    path("", views.index),
    path("num-games-in-progress/", views.num_games_in_progress),
    path("new-game/", views.new_game),
    path("game/<int:game_id>/", views.game),
    path("game/<int:game_id>/move/<int:row>/<int:column>/", views.move),
    path("game/<int:game_id>/ai-move/", views.ai_move),
    path("__debug__/", include(debug_toolbar.urls)),
]
