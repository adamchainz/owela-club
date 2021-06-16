from http import HTTPStatus

from django.test import TestCase

from owela_club.enums import GameState, Player
from owela_club.models import Game


class IndexTests(TestCase):
    def test_empty(self):
        response = self.client.get("/")

        assert response.status_code == HTTPStatus.OK
        content = response.content.decode()
        assert "No games are in progress." in content
        assert "No games have yet been finished." in content

    def test_success(self):
        game1 = Game.objects.create()
        game2 = Game.objects.create(
            state=GameState.FINISHED,
            winner=Player.HUMAN,
        )
        game3 = Game.objects.create(
            state=GameState.FINISHED,
            winner=Player.AI,
        )

        response = self.client.get("/")

        assert response.status_code == HTTPStatus.OK
        content = response.content.decode()
        assert f"Game {game1.id}" in content
        assert f"Game {game2.id}" in content
        assert "🥳 you won" in content
        assert f"Game {game3.id}" in content
        assert "🤖 AI won" in content


class NewGameTests(TestCase):
    def test_success(self):
        response = self.client.post("/new-game/")

        game = Game.objects.get()
        assert response.status_code == HTTPStatus.FOUND
        assert response["Location"] == f"/game/{game.id}/"


class GameTests(TestCase):
    def test_new(self):
        game = Game.objects.create()

        response = self.client.get(f"/game/{game.id}/")

        assert response.status_code == HTTPStatus.OK
        content = response.content.decode()
        assert "👉 It is your turn." in content

    def test_ai_turn(self):
        game = Game.objects.create(next_turn=Player.AI)

        response = self.client.get(f"/game/{game.id}/")

        assert response.status_code == HTTPStatus.OK
        content = response.content.decode()
        assert "💬 The AI is thinking..." in content

    def test_human_win(self):
        game = Game.objects.create(state=GameState.FINISHED, winner=Player.HUMAN)

        response = self.client.get(f"/game/{game.id}/")

        assert response.status_code == HTTPStatus.OK
        content = response.content.decode()
        assert "Game over" in content
        assert "you win! 🎉" in content

    def test_ai_win(self):
        game = Game.objects.create(state=GameState.FINISHED, winner=Player.AI)

        response = self.client.get(f"/game/{game.id}/")

        assert response.status_code == HTTPStatus.OK
        content = response.content.decode()
        assert "Game over" in content
        assert "you lose... 😭" in content


class MakeMoveTests(TestCase):
    def test_bad_row(self):
        game = Game.objects.create()

        response = self.client.post(f"/game/{game.id}/move/0/0/")

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.content.decode() == "Bad row"

    def test_bad_column(self):
        game = Game.objects.create()

        response = self.client.post(f"/game/{game.id}/move/2/20/")

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.content.decode() == "Bad column"

    def test_bad_square(self):
        game = Game.objects.create()

        response = self.client.post(f"/game/{game.id}/move/2/0/")

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.content.decode() == "Cannot move on square with < 2 seeds"

    def test_success(self):
        game = Game.objects.create()

        response = self.client.post(f"/game/{game.id}/move/2/7/")

        assert response.status_code == HTTPStatus.FOUND
        assert response["Location"] == f"/game/{game.id}/"
        game.refresh_from_db()
        assert game.next_turn == Player.AI
        assert game.state == GameState.IN_PROGRESS
        assert game.winner is None

    def test_success_win(self):
        game = Game.objects.create(
            board=[
                [0] * 12,
                [0] * 12,
                [2] + [0] * 11,
                [0] * 12,
            ],
        )

        response = self.client.post(f"/game/{game.id}/move/2/0/")

        assert response.status_code == HTTPStatus.FOUND
        assert response["Location"] == f"/game/{game.id}/"
        game.refresh_from_db()
        assert game.next_turn == Player.AI
        assert game.state == GameState.FINISHED
        assert game.winner == Player.HUMAN


class AiMoveTests(TestCase):
    def test_success(self):
        game = Game.objects.create(next_turn=Player.AI)

        response = self.client.post(f"/game/{game.id}/ai-move/")

        assert response.status_code == HTTPStatus.FOUND
        assert response["Location"] == f"/game/{game.id}/"
        game.refresh_from_db()
        assert game.next_turn == Player.HUMAN
        assert game.state == GameState.IN_PROGRESS
        assert game.winner is None

    def test_success_win(self):
        game = Game.objects.create(
            next_turn=Player.AI,
            board=[
                [2] * 12,
                [2] + [0] * 11,
                [0] * 12,
                [0] * 12,
            ],
        )

        response = self.client.post(f"/game/{game.id}/ai-move/")

        assert response.status_code == HTTPStatus.FOUND
        assert response["Location"] == f"/game/{game.id}/"
        game.refresh_from_db()
        assert game.next_turn == Player.HUMAN
        assert game.state == GameState.FINISHED
        assert game.winner == Player.AI
