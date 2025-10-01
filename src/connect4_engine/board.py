"""Provide core board primitives for the Connect 4 engine.

The helpers in this module implement the low-level operations required by the
minimax search, including board creation, move validation, move application, and
win detection. The functions operate on plain Python lists for portability and
are intentionally side-effect free unless explicitly documented.

"""

from __future__ import annotations

from typing import Iterable

EMPTY: int = 0
"""Integer used to represent an empty cell on the board."""

PLAYER_ONE: int = 1
"""Identifier for player one."""

PLAYER_TWO: int = 2
"""Identifier for player two."""

Board = list[list[int]]
"""Type alias describing the two-dimensional board structure."""


def create_board(row_count: int, column_count: int) -> Board:
    """Create an empty Connect 4 board represented as a list of lists.

    Args:
        row_count: Number of rows in the board.
        column_count: Number of columns in the board.

    Returns:
        Board: Newly allocated board filled with :data:`EMPTY` cells.

    """

    return [[EMPTY for _ in range(column_count)] for _ in range(row_count)]


def copy_board(board: Board) -> Board:
    """Return a deep copy of a board.

    Args:
        board: Board to copy.

    Returns:
        Board: Cloned board that can be mutated independently.

    """

    return [row.copy() for row in board]


def is_valid_location(board: Board, column: int, row_count: int) -> bool:
    """Return whether ``column`` has available space for a new piece.

    Args:
        board: Current game board.
        column: Column index to inspect.
        row_count: Number of rows in the board.

    Returns:
        bool: ``True`` when the column is not full.

    """

    if column < 0 or column >= len(board[0]):
        return False
    return board[row_count - 1][column] == EMPTY


def get_next_open_row(board: Board, column: int, row_count: int) -> int | None:
    """Return the lowest available row index in ``column``.

    Args:
        board: Current game board.
        column: Column index of interest.
        row_count: Number of rows in the board.

    Returns:
        int | None: Zero-based row index or ``None`` when the column is full.

    """

    if column < 0 or column >= len(board[0]):
        return None
    for row in range(row_count):
        if board[row][column] == EMPTY:
            return row
    return None


def drop_piece(board: Board, row: int, column: int, piece: int) -> None:
    """Place ``piece`` at the specified ``row`` and ``column``.

    Args:
        board: Board to mutate.
        row: Row index where the piece should land.
        column: Column index where the piece should be placed.
        piece: Player identifier to insert.

    Returns:
        None

    """

    board[row][column] = piece


def get_valid_locations(board: Board, row_count: int, column_count: int) -> list[int]:
    """Return a list of all columns that currently accept moves.

    Args:
        board: Current game board.
        row_count: Number of rows in the board.
        column_count: Number of columns in the board.

    Returns:
        list[int]: Columns that are not yet full.

    """

    return [column for column in range(column_count) if is_valid_location(board, column, row_count)]


def opponent(piece: int) -> int:
    """Return the opposing player's identifier.

    Args:
        piece: Player identifier (:data:`PLAYER_ONE` or :data:`PLAYER_TWO`).

    Returns:
        int: Identifier of the opposing player.

    """

    if piece == PLAYER_ONE:
        return PLAYER_TWO
    if piece == PLAYER_TWO:
        return PLAYER_ONE
    raise ValueError(f"Unknown piece code {piece}")


def winning_move(
    board: Board,
    piece: int,
    row_count: int,
    column_count: int,
    window_length: int,
) -> bool:
    """Return whether ``piece`` has a winning alignment on the board.

    Args:
        board: Current game board.
        piece: Player identifier to check for.
        row_count: Number of rows in the board.
        column_count: Number of columns in the board.
        window_length: Required alignment length to win.

    Returns:
        bool: ``True`` when ``piece`` occupies a winning window.

    """

    # Horizontal
    for row in range(row_count):
        for column in range(column_count - window_length + 1):
            window = board[row][column : column + window_length]
            if all(cell == piece for cell in window):
                return True
    # Vertical
    for column in range(column_count):
        for row in range(row_count - window_length + 1):
            window = [board[row + offset][column] for offset in range(window_length)]
            if all(cell == piece for cell in window):
                return True
    # Positive diagonal
    for row in range(row_count - window_length + 1):
        for column in range(column_count - window_length + 1):
            if all(board[row + offset][column + offset] == piece for offset in range(window_length)):
                return True
    # Negative diagonal
    for row in range(window_length - 1, row_count):
        for column in range(column_count - window_length + 1):
            if all(board[row - offset][column + offset] == piece for offset in range(window_length)):
                return True
    return False


def detect_winner(
    board: Board,
    row_count: int,
    column_count: int,
    window_length: int,
) -> tuple[int, bool]:
    """Return the winner and draw status for ``board``.

    Args:
        board: Current game board.
        row_count: Number of rows in the board.
        column_count: Number of columns in the board.
        window_length: Alignment length required to win.

    Returns:
        tuple[int, bool]: Two-tuple where the first item is the winning player
        identifier (``0`` when no winner exists) and the second item is ``True``
        when the position is a draw.

    """

    if winning_move(board, PLAYER_ONE, row_count, column_count, window_length):
        return PLAYER_ONE, False
    if winning_move(board, PLAYER_TWO, row_count, column_count, window_length):
        return PLAYER_TWO, False
    is_draw = not any(cell == EMPTY for row in board for cell in row)
    return 0, is_draw


def is_terminal(board: Board, row_count: int, column_count: int, window_length: int) -> bool:
    """Return whether the position is terminal (win or draw).

    Args:
        board: Current game board.
        row_count: Number of rows in the board.
        column_count: Number of columns in the board.
        window_length: Alignment length required for a win.

    Returns:
        bool: ``True`` when the game has been won or the board is full.

    """

    winner, is_draw = detect_winner(board, row_count, column_count, window_length)
    return winner != 0 or is_draw


def count_cells(cells: Iterable[int], value: int) -> int:
    """Return how many times ``value`` appears in ``cells``.

    Args:
        cells: Iterable of integers describing a window of board cells.
        value: Cell value to count.

    Returns:
        int: Number of occurrences of ``value`` in ``cells``.

    """

    return sum(1 for cell in cells if cell == value)
