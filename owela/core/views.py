from django.db.models import Case, When
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from owela.core.enums import GameState, Player
from owela.core.game import find_winner, make_move, pick_ai_move
from owela.core.models import Game


@require_http_methods(["GET"])
def index(request):
    games = Game.objects.annotate(
        in_progress_first=Case(When(state=GameState.IN_PROGRESS, then=0), default=1)
    ).order_by("in_progress_first", "id")

    return render(
        request,
        "index.html",
        {
            "games": games,
            "GameState": GameState,
        },
    )


@require_http_methods(["POST"])
def new_game(request):
    game = Game.objects.create()
    return redirect(f"/game/{game.id}/")


@require_http_methods(["GET"])
def game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    human_can_move = (
        game.state == GameState.IN_PROGRESS and game.next_turn == Player.HUMAN
    )
    ai_total = sum(game.board[row][column] for row in range(2) for column in range(12))
    human_total = sum(
        game.board[row][column] for row in range(2, 4) for column in range(12)
    )
    return render(
        request,
        "game.html",
        {
            "game": game,
            "human_can_move": human_can_move,
            "ai_total": ai_total,
            "human_total": human_total,
            "GameState": GameState,
            "Player": Player,
        },
    )


@require_http_methods(["POST"])
def move(request, game_id, row, column):
    game = get_object_or_404(
        Game,
        id=game_id,
        state=GameState.IN_PROGRESS,
        next_turn=Player.HUMAN,
    )
    if row < 2 or row > len(game.board):
        return HttpResponseBadRequest("Bad row")
    if column < 0 or column > len(game.board[0]):
        return HttpResponseBadRequest("Bad column")
    if game.board[row][column] < 2:
        return HttpResponseBadRequest("Cannot move on square with < 2 seeds")

    make_move(game.board, row, column)
    game.next_turn = Player.AI

    winner = find_winner(game.board)
    if winner is not None:
        game.winner = winner
        game.state = GameState.FINISHED

    game.save()

    return redirect(f"/game/{game.id}/")


@require_http_methods(["POST"])
def ai_move(request, game_id):
    game = get_object_or_404(
        Game,
        id=game_id,
        state=GameState.IN_PROGRESS,
        next_turn=Player.AI,
    )

    make_move(game.board, *pick_ai_move(game.board))
    game.next_turn = Player.HUMAN

    winner = find_winner(game.board)
    if winner is not None:
        game.winner = winner
        game.state = GameState.FINISHED

    game.save()

    return redirect(f"/game/{game.id}/")
