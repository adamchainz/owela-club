from __future__ import annotations

from django.test import SimpleTestCase

from owela_club.enums import Player
from owela_club.game import (
    find_winner,
    make_move,
    new_board,
    next_anti_clockwise_position,
    pick_ai_move,
)


class NewBoardTests(SimpleTestCase):
    def test_success(self):
        board = new_board()

        assert len(board) == 4
        for row in board:
            assert len(row) == 12


class NextAntiClockwisePositionTests(SimpleTestCase):
    def test_0_0(self):
        assert next_anti_clockwise_position(0, 0) == (1, 0)

    def test_1_0(self):
        assert next_anti_clockwise_position(1, 0) == (1, 1)

    def test_0_1(self):
        assert next_anti_clockwise_position(0, 1) == (0, 0)

    def test_1_11(self):
        assert next_anti_clockwise_position(1, 11) == (0, 11)

    def test_0_11(self):
        assert next_anti_clockwise_position(0, 11) == (0, 10)

    def test_2_0(self):
        assert next_anti_clockwise_position(2, 0) == (3, 0)


class MakeMoveTests(SimpleTestCase):
    def test_human_first(self):
        board = new_board()

        make_move(board, 2, 7)

        assert board == [
            [2] * 12,
            [2] * 5 + [0] * 7,
            [0] * 5 + [1] * 2 + [0] + [2] * 4,
            [2] * 12,
        ]

    def test_inner_row(self):
        board = [
            [2] * 12,
            [0] * 12,
            [1] * 12,
            [0] * 12,
        ]

        make_move(board, 2, 1)

        assert board == [
            [2] * 12,
            [0] * 12,
            [0] * 2 + [1] * 10,
            [1] * 2 + [0] * 10,
        ]

    def test_capture_inner(self):
        # human captures the leftmost column
        board = [
            [0] * 12,
            [2] * 12,
            [1] * 2 + [0] * 10,
            [0] * 12,
        ]

        make_move(board, 2, 1)

        assert board == [
            [0] * 12,
            [0] + [2] * 11,
            [0] * 12,
            [1] * 4 + [0] * 8,
        ]

    def test_capture_inner_and_outer(self):
        # human captures the leftmost column
        board = [
            [2] * 12,
            [2] * 12,
            [1] * 2 + [0] * 10,
            [0] * 12,
        ]

        make_move(board, 2, 1)

        assert board == [
            [0] + [2] * 11,
            [0] + [2] * 11,
            [0] * 12,
            [1] * 6 + [0] * 6,
        ]


class PickAiMoveTests(SimpleTestCase):
    def test_simple(self):
        # board with just one move for AI
        board = [
            [0] * 11 + [2],
            [0] * 12,
            [0] * 12,
            [0] * 12,
        ]

        result = pick_ai_move(board)

        assert result == (0, 11)


class FindWinnerTests(SimpleTestCase):
    def test_no_winner(self):
        board = new_board()

        result = find_winner(board)

        assert result is None

    def test_ai_winner(self):
        # ai has all the seeds
        board = [
            [0] * 11 + [68],
            [0] * 12,
            [0] * 12,
            [0] * 12,
        ]

        result = find_winner(board)

        assert result == Player.AI

    def test_human_winner(self):
        # human has all the seeds
        board = [
            [0] * 12,
            [0] * 12,
            [0] * 12,
            [68] + [0] * 11,
        ]

        result = find_winner(board)

        assert result == Player.HUMAN
