from __future__ import annotations

from django.db import models


class GameState(models.IntegerChoices):
    IN_PROGRESS = 1
    FINISHED = 2


class Player(models.IntegerChoices):
    HUMAN = 1
    AI = 2


class Game(models.Model):
    state = models.IntegerField(
        choices=GameState.choices, default=GameState.IN_PROGRESS
    )
    next_turn = models.IntegerField(choices=Player.choices, default=Player.HUMAN)
    winner = models.IntegerField(choices=Player.choices, null=True)
    board = models.JSONField()

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_state_valid",
                check=models.Q(state__in=GameState.values),
            ),
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_next_turn_valid",
                check=models.Q(next_turn__in=Player.values),
            ),
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_winner_valid",
                check=(
                    models.Q(winner__isnull=True) | models.Q(winner__in=Player.values)
                ),
            ),
        ]
