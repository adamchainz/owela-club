from __future__ import annotations

import random

from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from owela.core.models import Game, GameState


def new_board():
    return [
        [2] * 12,
        [2] * 5 + [0] * 7,
        [0] * 7 + [2] * 5,
        [2] * 12,
    ]


def next_clockwise_position(row, column):
    if row % 2 == 0:  # row is even
        column -= 1
        if column == -1:
            # left edge
            column += 1
            row += 1
    else:
        column += 1
        if column == 12:
            # right edge
            column -= 1
            row -= 1

    return row, column


def make_move(board, row, column):
    num_seeds = board[row][column]
    board[row][column] = 0

    while num_seeds:
        row, column = next_clockwise_position(row, column)

        if num_seeds == 1 and board[row][column] > 0:
            is_inner_row = row in (1, 2)

            opposite_row = 3 - row
            opposite_outer_row = (
                opposite_row - 1 if opposite_row <= 1 else opposite_row + 1
            )

            if (
                is_inner_row
                and board[opposite_row][column] > 0
                and board[opposite_outer_row][column] > 0
            ):
                # capture
                num_seeds += board[opposite_row][column]
                board[opposite_row][column] = 0
                num_seeds += board[opposite_outer_row][column]
                board[opposite_outer_row][column] = 0

            # pick up own seed
            num_seeds += board[row][column]
            board[row][column] = 0
        else:
            # put down
            board[row][column] += 1
            num_seeds -= 1

    # TODO: capture


def pick_random_ai_move(board):
    candidates = []
    for row in range(2):
        for column in range(12):
            if board[row][column] > 1:
                candidates.append((row, column))

    if not candidates:
        return None

    return random.choice(candidates)


@require_http_methods(["GET"])
def index(request):
    return render(
        request,
        "index.html",
        {"games": Game.objects.all(), "GameState": GameState},
    )


@require_http_methods(["POST"])
def new_game(request):
    game = Game.objects.create(board=new_board())
    return redirect(f"/game/{game.id}/")


@require_http_methods(["GET"])
def game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    return render(request, "game.html", {"game": game})


@require_http_methods(["POST"])
def move(request, game_id, row, column):
    game = get_object_or_404(Game, id=game_id, state=GameState.IN_PROGRESS)
    if row < 2 or row > len(game.board):
        raise Http404("Unknown row")
    if column < 0 or column > len(game.board[0]):
        raise Http404("Unknown column")
    if game.board[row][column] < 2:
        raise Http404("Cannot move on square with < 2 seeds")

    # player move
    make_move(game.board, row, column)

    # “AI” move
    ai_move = pick_random_ai_move(game.board)
    if ai_move is None:
        # human has won
        game.state = GameState.FINISHED
    else:
        make_move(game.board, *ai_move)

    game.save()

    return redirect(f"/game/{game.id}/")
