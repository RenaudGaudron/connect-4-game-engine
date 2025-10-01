"""Provide the command-line interface for the Connect 4 engine package.

The CLI accepts the starting player, historical moves, and minimax depth, then
prints the recommended column index. This module is registered as the entry
point ``connect4-engine`` in :mod:`pyproject.toml`.

"""

from __future__ import annotations

import argparse
import sys

from .engine import Connect4Engine


def build_parser() -> argparse.ArgumentParser:
    """Return the argument parser used by the CLI.

    Returns:
        argparse.ArgumentParser: Configured parser with all CLI options.

    """

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--starter",
        type=int,
        required=True,
        help="Identifier of the starting player (1 or 2).",
    )
    parser.add_argument(
        "--history",
        type=str,
        default="",
        help="History of moves encoded as column digits (e.g. 334221).",
    )
    parser.add_argument(
        "--depth",
        type=int,
        default=8,
        help="Minimax depth to use when computing the move (default 8).",
    )
    parser.add_argument(
        "--rows",
        type=int,
        default=6,
        help="Number of rows in the board (default 6).",
    )
    parser.add_argument(
        "--columns",
        type=int,
        default=7,
        help="Number of columns in the board (default 7).",
    )
    parser.add_argument(
        "--window",
        type=int,
        default=4,
        help="Alignment length required to win (default 4).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the CLI and return an exit code compatible with ``sys.exit``.

    Args:
        argv: Optional list of arguments for testing. When ``None`` the
            arguments are read from :data:`sys.argv`.

    Returns:
        int: ``0`` when successful, ``2`` when input validation fails.

    """

    parser = build_parser()
    args = parser.parse_args(argv)

    engine = Connect4Engine(
        depth=args.depth,
        row_count=args.rows,
        column_count=args.columns,
        window_length=args.window,
    )

    try:
        result = engine.suggest_move(starter=args.starter, history_str=args.history)
    except ValueError as error:
        parser.error(str(error))
        return 2

    if result.column is not None:
        print(result.column)
    if result.is_draw:
        print("Draw!")
    elif result.winner in {1, 2}:
        print(f"Player {result.winner} won!")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
