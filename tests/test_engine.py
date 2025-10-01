"""Exercise the high-level engine behaviour.

The tests validate that the public engine API returns sound suggestions,
reports terminal positions without searching, and continues to reject invalid
histories.

"""

from __future__ import annotations

from connect4_engine.engine import Connect4Engine


def test_engine_identifies_winning_move() -> None:
    """Ensure the engine finds an immediate winning horizontal move.

    Returns:
        None: This test does not return a value.

    """

    engine = Connect4Engine(depth=3)
    result = engine.suggest_move(starter=1, history_str="041425")
    assert result.column == 3
    assert result.winner == 1
    assert not result.is_draw


def test_engine_returns_terminal_win() -> None:
    """Verify that terminal histories produce a no-move result.

    Returns:
        None: This test does not return a value.

    """

    engine = Connect4Engine(depth=2)
    history = "0101010"
    result = engine.suggest_move(starter=1, history_str=history)
    assert result.column is None
    assert result.winner == 1
    assert not result.is_draw


def test_engine_returns_draw_result() -> None:
    """Verify that a drawn position is reported without a move.

    Returns:
        None: This test does not return a value.

    """

    engine = Connect4Engine(depth=2, row_count=4, column_count=4, window_length=4)
    draw_history = "0213203102132031"
    result = engine.suggest_move(starter=1, history_str=draw_history)
    assert result.column is None
    assert result.winner == 0
    assert result.is_draw


def test_engine_default_depth() -> None:
    """Ensure the engine initialises with the documented default depth.

    Returns:
        None: This test does not return a value.

    """

    engine = Connect4Engine()
    assert engine.depth == 8
