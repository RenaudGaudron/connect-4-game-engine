"""Exercise board primitives for win and draw detection.

The tests in this module ensure that win detection and terminal state
calculation behave as expected for representative positions, including the
``detect_winner`` helper that reports both winners and draws.

"""

from __future__ import annotations

from connect4_engine import board


def test_horizontal_win_detection() -> None:
    """Ensure that horizontal alignments are detected correctly.

    Returns:
        None: This test does not return a value.

    """

    game_board = board.create_board(6, 7)
    for column in range(4):
        row = board.get_next_open_row(game_board, column, 6)
        assert row is not None
        board.drop_piece(game_board, row, column, board.PLAYER_ONE)
    assert board.winning_move(game_board, board.PLAYER_ONE, 6, 7, 4)


def test_no_win_on_empty_board() -> None:
    """Verify that an empty board is not considered terminal.

    Returns:
        None: This test does not return a value.

    """

    game_board = board.create_board(6, 7)
    assert not board.winning_move(game_board, board.PLAYER_ONE, 6, 7, 4)
    assert not board.is_terminal(game_board, 6, 7, 4)


def test_detect_winner_reports_draw() -> None:
    """Ensure ``detect_winner`` flags a full-board draw.

    Returns:
        None: This test does not return a value.

    """

    row_count, column_count, window_length = 4, 4, 4
    history = [0, 2, 1, 3, 2, 0, 3, 1, 0, 2, 1, 3, 2, 0, 3, 1]
    game_board = board.create_board(row_count, column_count)
    current = board.PLAYER_ONE
    for move in history:
        row = board.get_next_open_row(game_board, move, row_count)
        assert row is not None
        board.drop_piece(game_board, row, move, current)
        current = board.opponent(current)

    winner, is_draw = board.detect_winner(game_board, row_count, column_count, window_length)
    assert winner == 0
    assert is_draw
