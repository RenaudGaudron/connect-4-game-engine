"""Implement minimax search with alpha-beta pruning for Connect 4.

The heuristics favour controlling the centre columns, creating open-ended
threats, and preventing the opponent from forming immediate wins. These
utilities are used by :class:`connect4_engine.engine.Connect4Engine` to analyse
positions efficiently.

"""

from __future__ import annotations

from math import inf
from typing import Iterable

from . import board as board_lib

CENTER_WEIGHT: int = 3
"""Weight applied to center column control in the evaluation function."""

SCORE_FOUR: int = 10_000
"""Score returned for a four-in-a-row alignment."""

SCORE_THREE: int = 100
"""Bonus for a three-in-a-row with an empty slot to extend."""

SCORE_TWO: int = 10
"""Bonus for a two-in-a-row with two empty slots."""

PENALTY_THREE: int = -120
"""Penalty applied when the opponent has an immediate three threat."""


def evaluate_window(window: Iterable[int], piece: int) -> int:
    """Return the heuristic contribution for a four-cell ``window``.

    Args:
        window: Iterable of four board values.
        piece: Piece identifier we are evaluating the board for.

    Returns:
        int: Score representing the desirability of ``window`` for ``piece``.

    """

    window_list = list(window)
    opp_piece = board_lib.opponent(piece)
    piece_count = board_lib.count_cells(window_list, piece)
    empty_count = board_lib.count_cells(window_list, board_lib.EMPTY)
    opp_count = board_lib.count_cells(window_list, opp_piece)

    if piece_count == 4:
        return SCORE_FOUR
    if piece_count == 3 and empty_count == 1:
        return SCORE_THREE
    if piece_count == 2 and empty_count == 2:
        return SCORE_TWO
    if opp_count == 3 and empty_count == 1:
        return PENALTY_THREE
    return 0


def _score_center(board: board_lib.Board, piece: int, row_count: int, column_count: int) -> int:
    """Return a bonus for occupying the center column when available.

    Args:
        board: Current game board.
        piece: Player identifier to evaluate.
        row_count: Number of rows in the board.
        column_count: Number of columns in the board.

    Returns:
        int: Weighted count of pieces in the center column.

    """

    center_column = column_count // 2
    column_cells = [board[row][center_column] for row in range(row_count)]
    return board_lib.count_cells(column_cells, piece) * CENTER_WEIGHT


def _score_all_windows(
    board: board_lib.Board,
    piece: int,
    row_count: int,
    column_count: int,
    window_length: int,
) -> int:
    """Return the aggregated heuristic for all board windows.

    Args:
        board: Current game board.
        piece: Player identifier to evaluate.
        row_count: Number of rows in the board.
        column_count: Number of columns in the board.
        window_length: Length of each evaluated window.

    Returns:
        int: Sum of heuristics for every possible window.

    """

    score = 0
    # Horizontal
    for row in range(row_count):
        for column in range(column_count - window_length + 1):
            window = board[row][column : column + window_length]
            score += evaluate_window(window, piece)
    # Vertical
    for column in range(column_count):
        for row in range(row_count - window_length + 1):
            window = (board[row + offset][column] for offset in range(window_length))
            score += evaluate_window(window, piece)
    # Positive diagonal
    for row in range(row_count - window_length + 1):
        for column in range(column_count - window_length + 1):
            window = (board[row + offset][column + offset] for offset in range(window_length))
            score += evaluate_window(window, piece)
    # Negative diagonal
    for row in range(window_length - 1, row_count):
        for column in range(column_count - window_length + 1):
            window = (board[row - offset][column + offset] for offset in range(window_length))
            score += evaluate_window(window, piece)
    return score


def score_position(
    board: board_lib.Board,
    piece: int,
    row_count: int,
    column_count: int,
    window_length: int,
) -> int:
    """Return the heuristic evaluation for ``piece`` on ``board``.

    Args:
        board: Current game board.
        piece: Player identifier to evaluate.
        row_count: Number of rows in the board.
        column_count: Number of columns in the board.
        window_length: Length of each evaluated window.

    Returns:
        int: Heuristic score combining center control and window evaluations.

    """

    return _score_center(board, piece, row_count, column_count) + _score_all_windows(
        board,
        piece,
        row_count,
        column_count,
        window_length,
    )


def order_moves_center_first(valid_locations: Iterable[int], column_count: int) -> list[int]:
    """Return valid moves ordered by distance from the center column.

    Args:
        valid_locations: Iterable of legal column indices.
        column_count: Total number of columns on the board.

    Returns:
        list[int]: Valid moves ordered to improve alpha-beta pruning.

    """

    center = column_count // 2
    return sorted(valid_locations, key=lambda column: abs(center - column))


def minimax(
    board: board_lib.Board,
    depth: int,
    alpha: float,
    beta: float,
    maximizing_piece: int,
    current_piece: int,
    row_count: int,
    column_count: int,
    window_length: int,
) -> tuple[int | None, float]:
    """Return the minimax evaluation and best move for ``maximizing_piece``.

    Args:
        board: Current game board.
        depth: Remaining search depth.
        alpha: Alpha bound for alpha-beta pruning.
        beta: Beta bound for alpha-beta pruning.
        maximizing_piece: Piece for which the evaluation should be maximized.
        current_piece: Piece whose turn it is at this node.
        row_count: Number of rows in the board.
        column_count: Number of columns in the board.
        window_length: Alignment length required to win.

    Returns:
        tuple[int | None, float]: Best column and its evaluation score.

    """

    valid_locations = board_lib.get_valid_locations(board, row_count, column_count)
    terminal = board_lib.is_terminal(board, row_count, column_count, window_length)

    if depth == 0 or terminal:
        max_score = score_position(board, maximizing_piece, row_count, column_count, window_length)
        opp_score = score_position(
            board,
            board_lib.opponent(maximizing_piece),
            row_count,
            column_count,
            window_length,
        )
        evaluation = max_score - opp_score
        if terminal:
            if board_lib.winning_move(board, maximizing_piece, row_count, column_count, window_length):
                evaluation = inf
            elif board_lib.winning_move(
                board,
                board_lib.opponent(maximizing_piece),
                row_count,
                column_count,
                window_length,
            ):
                evaluation = -inf
            else:
                evaluation = 0
        return None, evaluation

    if current_piece == maximizing_piece:
        value = -inf
        chosen_column = valid_locations[0]
        for column in order_moves_center_first(valid_locations, column_count):
            row = board_lib.get_next_open_row(board, column, row_count)
            if row is None:
                continue
            temp_board = board_lib.copy_board(board)
            board_lib.drop_piece(temp_board, row, column, current_piece)
            _, new_score = minimax(
                temp_board,
                depth - 1,
                alpha,
                beta,
                maximizing_piece,
                board_lib.opponent(current_piece),
                row_count,
                column_count,
                window_length,
            )
            if new_score > value:
                value = new_score
                chosen_column = column
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return chosen_column, value

    value = inf
    chosen_column = valid_locations[0]
    for column in order_moves_center_first(valid_locations, column_count):
        row = board_lib.get_next_open_row(board, column, row_count)
        if row is None:
            continue
        temp_board = board_lib.copy_board(board)
        board_lib.drop_piece(temp_board, row, column, current_piece)
        _, new_score = minimax(
            temp_board,
            depth - 1,
            alpha,
            beta,
            maximizing_piece,
            board_lib.opponent(current_piece),
            row_count,
            column_count,
            window_length,
        )
        if new_score < value:
            value = new_score
            chosen_column = column
        beta = min(beta, value)
        if alpha >= beta:
            break
    return chosen_column, value
