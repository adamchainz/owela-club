from __future__ import annotations

from django.urls import path

from owela.core import views

urlpatterns = [
    path("", views.index),
    path("new-game/", views.new_game),
    path("game/<int:game_id>/", views.game),
    path("game/<int:game_id>/move/<int:row>/<int:column>/", views.move),
]
