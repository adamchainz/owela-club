import random

from owela_club.enums import Player


def new_board():
    return [
        [2] * 12,
        [2] * 5 + [0] * 7,
        [0] * 7 + [2] * 5,
        [2] * 12,
    ]


def next_anti_clockwise_position(row, column):
    """
    Given any position on the board, go to the next one following the
    anti-clockwise pattern.
    """
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
    """
    Follow through a move, including captures.
    """
    hand_seeds = board[row][column]
    board[row][column] = 0

    while hand_seeds:
        row, column = next_anti_clockwise_position(row, column)

        if hand_seeds == 1 and board[row][column] > 0:
            is_inner_row = row in (1, 2)

            opposite_row = 3 - row
            opposite_outer_row = (
                opposite_row - 1 if opposite_row <= 1 else opposite_row + 1
            )

            if is_inner_row and board[opposite_row][column] > 0:
                # capture
                hand_seeds += board[opposite_row][column]
                board[opposite_row][column] = 0

                hand_seeds += board[opposite_outer_row][column]
                board[opposite_outer_row][column] = 0

            # pick up own seed
            hand_seeds += board[row][column]
            board[row][column] = 0
        else:
            # put down
            board[row][column] += 1
            hand_seeds -= 1


def pick_ai_move(board):
    """
    Randomly pick a legitimate AI move.
    TODO: deep learning.
    """
    candidates = []
    for row in range(2):
        for column in range(12):
            if board[row][column] > 1:
                candidates.append((row, column))

    return random.choice(candidates)


def find_winner(board):
    """
    Return the Player value for the winner of this board, or None if no one has
    won yet.
    """
    ai_cannot_move = all(
        board[row][column] < 2 for row in range(2) for column in range(12)
    )
    if ai_cannot_move:
        return Player.HUMAN

    human_cannot_move = all(
        board[row][column] < 2 for row in range(2, 4) for column in range(12)
    )
    if human_cannot_move:
        return Player.AI

    return None
