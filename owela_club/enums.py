from __future__ import annotations

from django.db import models


class GameState(models.IntegerChoices):
    IN_PROGRESS = 1
    FINISHED = 2


class Player(models.IntegerChoices):
    HUMAN = 1
    AI = 2
