from django.db import models

from owela_club.enums import GameState, Player
from owela_club.game import new_board


class Game(models.Model):
    state = models.IntegerField(
        choices=GameState.choices, default=GameState.IN_PROGRESS
    )
    next_turn = models.IntegerField(choices=Player.choices, default=Player.HUMAN)
    winner = models.IntegerField(choices=Player.choices, null=True)
    board = models.JSONField(default=new_board)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_state",
                check=(
                    models.Q(state=GameState.IN_PROGRESS, winner__isnull=True)
                    | models.Q(state=GameState.FINISHED, winner__in=Player.values)
                ),
            ),
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_next_turn_valid",
                check=models.Q(next_turn__in=Player.values),
            ),
        ]
