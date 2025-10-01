"""Expose a user-friendly interface around the minimax search engine.

The :class:`Connect4Engine` class wraps board parsing, heuristics, and the
minimax algorithm into a simple API suitable for both command-line and library
use. Histories are strings of zero-based column indices, and the starting
player is specified using ``1`` or ``2``. The module validates inputs, manages
search configuration, and produces high-quality move recommendations using
alpha-beta pruning.

"""

from __future__ import annotations

from dataclasses import dataclass

from . import board as board_lib
from . import history
from . import minimax


@dataclass(frozen=True)
class SuggestionResult:
    """Represent the outcome of :meth:`Connect4Engine.suggest_move`.

    Attributes:
        column: Recommended column index or ``None`` when the position is
            already terminal.
        winner: Winning player identifier (``0`` when no winner exists).
        is_draw: ``True`` when the position is a draw.

    """

    column: int | None
    winner: int
    is_draw: bool

@dataclass
class EngineConfig:
    """Configuration describing the board dimensions and search depth.

    Attributes:
        row_count: Number of rows in the board.
        column_count: Number of columns in the board.
        window_length: Alignment length required to win.
        depth: Default search depth for minimax.

    """

    row_count: int = 6
    column_count: int = 7
    window_length: int = 4
    depth: int = 8


class Connect4Engine:
    """Provide minimax-based move suggestions for Connect 4.

    The engine maintains board geometry information and offers helpers to adjust
    search depth. Each call to :meth:`suggest_move` parses the provided history,
    validates the position, and runs the minimax search with alpha-beta pruning
    to identify the best move for the side to play.

    """

    def __init__(
        self,
        depth: int = 8,
        row_count: int = 6,
        column_count: int = 7,
        window_length: int = 4,
    ) -> None:
        """Initialise the engine with the desired configuration.

        Args:
            depth: Default minimax depth for move suggestions. The default of
                ``8`` provides a strong tactical baseline.
            row_count: Number of rows in the board.
            column_count: Number of columns in the board.
            window_length: Alignment length required to win.

        Returns:
            None: This constructor does not return a value.

        Raises:
            ValueError: If any parameter is invalid.

        """

        self._config = EngineConfig(
            row_count=row_count,
            column_count=column_count,
            window_length=window_length,
            depth=depth,
        )
        self._validate_config()

    @property
    def depth(self) -> int:
        """Return the configured default search depth.

        Returns:
            int: Configured default search depth used when none is provided.

        """

        return self._config.depth

    def set_depth(self, depth: int) -> None:
        """Update the default minimax depth used by the engine.

        Args:
            depth: New depth value to apply. Must be a positive integer.

        Returns:
            None: This method does not return a value.

        Raises:
            ValueError: If ``depth`` is not a positive integer.

        """

        if depth <= 0:
            msg = "Depth must be a positive integer"
            raise ValueError(msg)
        self._config.depth = depth

    def suggest_move(
        self,
        starter: int,
        history_str: str,
        depth: int | None = None,
    ) -> SuggestionResult:
        """Return the next move selected by the minimax engine.

        Args:
            starter: Player identifier (1 or 2) that played the first move.
            history_str: String encoding the historical column choices.
            depth: Optional override for the minimax depth. When omitted the
                engine's default depth is used.

        Returns:
            SuggestionResult: Dataclass describing the chosen move and resulting
            outcome. When the history is already terminal ``column`` is ``None``
            and the appropriate winner or draw flag is set.

        Raises:
            ValueError: If the history is invalid or the depth is non-positive.

        """

        config = self._config
        state = history.parse_history(
            starter,
            history_str,
            config.row_count,
            config.column_count,
            config.window_length,
        )
        if state.winner or state.is_draw:
            return SuggestionResult(column=None, winner=state.winner, is_draw=state.is_draw)
        if state.next_player == 0:
            return SuggestionResult(column=None, winner=state.winner, is_draw=state.is_draw)

        search_depth = depth if depth is not None else config.depth
        if search_depth <= 0:
            msg = "Depth must be positive"
            raise ValueError(msg)

        valid_moves = board_lib.get_valid_locations(
            state.board,
            config.row_count,
            config.column_count,
        )
        if not valid_moves:
            return SuggestionResult(column=None, winner=state.winner, is_draw=True)

        best_column, _ = minimax.minimax(
            state.board,
            search_depth,
            float("-inf"),
            float("inf"),
            state.next_player,
            state.next_player,
            config.row_count,
            config.column_count,
            config.window_length,
        )

        chosen_column = valid_moves[0] if best_column is None else int(best_column)
        simulation_board = board_lib.copy_board(state.board)
        row = board_lib.get_next_open_row(simulation_board, chosen_column, config.row_count)
        if row is None:
            msg = f"Column {chosen_column} is unexpectedly full"
            raise ValueError(msg)
        board_lib.drop_piece(simulation_board, row, chosen_column, state.next_player)
        winner, is_draw = board_lib.detect_winner(
            simulation_board,
            config.row_count,
            config.column_count,
            config.window_length,
        )
        return SuggestionResult(column=chosen_column, winner=winner, is_draw=is_draw)

    def _validate_config(self) -> None:
        """Validate the engine configuration and raise on invalid values.

        Returns:
            None: This method does not return a value.

        Raises:
            ValueError: If the configuration values are out of range.

        """

        if self._config.depth <= 0:
            msg = "Depth must be positive"
            raise ValueError(msg)
        if self._config.row_count <= 0 or self._config.column_count <= 0:
            msg = "Board dimensions must be positive"
            raise ValueError(msg)
        if self._config.window_length <= 0:
            msg = "Window length must be positive"
            raise ValueError(msg)
