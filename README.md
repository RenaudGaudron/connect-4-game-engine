# Connect 4 Engine

A lightweight Connect 4 engine implemented in pure Python using a minimax
search with alpha-beta pruning. The project provides a reusable package and
command line interface for analysing ongoing games or automating play against
other agents. Everything required to parse game histories and evaluate
positions ships within this repository, making the package self-contained.

## Installation

```bash
pip install .
```

## Usage

The package exposes both a programmatic API and a CLI. Game histories are
encoded as a string of column indices (0-based) representing each move played in
order. Provide the integer identifier of the starting player (``1`` for player
one, ``2`` for player two) alongside the history string to fully describe the
current position.

### CLI

The CLI prints the recommended move when the position is ongoing. If the game
is already over, the search is skipped and a terminal message is displayed
instead. Immediate wins triggered by the recommended move include both the move
and the winning announcement.

```bash
$ connect4-engine --starter 1 --history 0101010
Player 1 won!

$ connect4-engine --starter 1 --rows 4 --columns 4 --window 4 --history 0213203102132031
Draw!

$ connect4-engine --starter 1 --history 041425 --depth 3
3
Player 1 won!
```

When no immediate win follows the engine's recommendation, only the column
index is printed. Adjust `--depth` to control the minimax search depth (higher
values are stronger but slower). The default depth is ``8``, which offers a
strong baseline for tactical play on modern hardware.

### Python API

```python
from connect4_engine import Connect4Engine

engine = Connect4Engine(depth=8)
result = engine.suggest_move(starter=1, history_str="334221")

if result.column is not None:
    print(f"Engine recommends column {result.column}")
if result.is_draw:
    print("Draw!")
elif result.winner in {1, 2}:
    print(f"Player {result.winner} won!")
```

### Terminal detection helpers

Terminal detection is handled by :func:`connect4_engine.board.detect_winner`,
which returns a ``(winner, is_draw)`` tuple. ``winner`` is ``0`` for ongoing or
drawn positions, or the player identifier (:data:`1` or :data:`2`) when a win is
present. ``is_draw`` is ``True`` only when the board is full without a winner.
This helper covers horizontal, vertical, and both diagonal wins in addition to
full-board draws. The CLI and :class:`Connect4Engine` rely on this helper to
avoid searching terminal positions and to announce outcomes consistently.

### Package structure

```
src/connect4_engine/
    __init__.py        # Package exports and metadata
    board.py           # Board primitives and win detection
    engine.py          # High-level engine interface
    history.py         # Parsing logic for history strings
    minimax.py         # Minimax search with alpha-beta pruning
    cli.py             # Command-line interface entry point
```

## Development

Install the package in editable mode and run the test suite with `pytest` to
verify functionality.

```bash
pip install -e .
pytest
```

The repository includes comprehensive unit tests covering board logic, history
parsing, the minimax search, and the command-line interface.

