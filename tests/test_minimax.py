"""Test heuristic helpers powering the minimax search.

The tests focus on the deterministic scoring utilities used during search and a
smoke test for the top-level minimax function.

"""

from __future__ import annotations

from connect4_engine import board
from connect4_engine.minimax import evaluate_window, minimax, order_moves_center_first


def test_evaluate_window_rewards_winning_alignment() -> None:
    """Ensure four in a row yields the maximum heuristic score.

    Returns:
        None: This test does not return a value.

    """

    window = [board.PLAYER_ONE] * 4
    score = evaluate_window(window, board.PLAYER_ONE)
    assert score > 0


def test_order_moves_prefers_center_column() -> None:
    """Verify move ordering sorts columns by distance from the centre.

    Returns:
        None: This test does not return a value.

    """

    ordered = order_moves_center_first([0, 1, 2, 3, 4, 5, 6], column_count=7)
    assert ordered[0] == 3
    assert ordered[-1] in {0, 6}


def test_minimax_detects_immediate_win() -> None:
    """Check that minimax reports a winning move when available.

    Returns:
        None: This test does not return a value.

    """

    game_board = board.create_board(6, 7)
    for column in range(3):
        row = board.get_next_open_row(game_board, column, 6)
        assert row is not None
        board.drop_piece(game_board, row, column, board.PLAYER_ONE)
    best_move, score = minimax(
        game_board,
        depth=2,
        alpha=float("-inf"),
        beta=float("inf"),
        maximizing_piece=board.PLAYER_ONE,
        current_piece=board.PLAYER_ONE,
        row_count=6,
        column_count=7,
        window_length=4,
    )
    assert best_move == 3
    assert score == float("inf")
