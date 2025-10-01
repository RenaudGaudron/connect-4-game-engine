"""Parse move histories encoded as digit strings.

The parsing utilities convert compact move strings into populated board states
and validate that the sequence of moves is legal. Histories list moves as
zero-based column digits in play order, and the starting player is represented
by ``1`` or ``2``. These helpers ensure that input positions are consistent
before running the search algorithm.

"""

from __future__ import annotations

from dataclasses import dataclass

from . import board as board_lib


@dataclass(frozen=True)
class GameState:
    """Represent the reconstructed state derived from a move history.

    Attributes:
        board: Populated board after applying ``moves``.
        next_player: Player identifier whose turn is next (``0`` when the game
            has finished).
        winner: Winner of the game if the history has already finished (``0``
            when no winner exists).
        is_draw: ``True`` when the reconstructed game ended in a draw.
        moves_played: Number of applied moves.

    """

    board: board_lib.Board
    next_player: int
    winner: int
    is_draw: bool
    moves_played: int


def parse_history(
    starter: int,
    moves: str,
    row_count: int,
    column_count: int,
    window_length: int,
) -> GameState:
    """Return a :class:`GameState` reconstructed from ``moves``.

    Args:
        starter: Player identifier (1 or 2) who played the first move.
        moves: String encoding column indices using single digits.
        row_count: Number of rows in the board.
        column_count: Number of columns in the board.
        window_length: Required alignment length to win.

    Returns:
        GameState: Reconstructed state validated against the rules.

    Raises:
        ValueError: If the history contains illegal moves or inconsistent data.

    """

    if starter not in {board_lib.PLAYER_ONE, board_lib.PLAYER_TWO}:
        msg = f"Starter must be 1 or 2, received {starter}"
        raise ValueError(msg)

    board = board_lib.create_board(row_count, column_count)
    current_player = starter
    winner = 0
    is_draw = False

    for index, move_char in enumerate(moves):
        if not move_char.isdigit():
            msg = f"Illegal move token '{move_char}' at index {index}"
            raise ValueError(msg)
        column = int(move_char)
        if column < 0 or column >= column_count:
            msg = f"Move {move_char} is outside the valid column range"
            raise ValueError(msg)
        row = board_lib.get_next_open_row(board, column, row_count)
        if row is None:
            msg = f"Column {column} is full before applying move {index}"
            raise ValueError(msg)
        board_lib.drop_piece(board, row, column, current_player)
        winner, is_draw = board_lib.detect_winner(
            board,
            row_count,
            column_count,
            window_length,
        )
        if winner and index < len(moves) - 1:
            msg = "Moves continue after the game has already been won"
            raise ValueError(msg)
        if is_draw and index < len(moves) - 1:
            msg = "Moves continue after the game has already reached a draw"
            raise ValueError(msg)
        if winner or is_draw:
            current_player = 0
        else:
            current_player = board_lib.opponent(current_player)

    next_player = current_player if current_player != 0 else 0
    return GameState(
        board=board,
        next_player=next_player,
        winner=winner,
        is_draw=is_draw,
        moves_played=len(moves),
    )
