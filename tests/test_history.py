"""Test parsing of history strings into validated game states.

The tests ensure that legal histories yield consistent state reconstructions and
that invalid sequences raise informative errors.

"""

from __future__ import annotations

import pytest

from connect4_engine import board
from connect4_engine.history import GameState, parse_history


def test_parse_history_builds_expected_state() -> None:
    """Verify that a simple history creates the correct game state.

    Returns:
        None: This test does not return a value.

    """

    state = parse_history(starter=1, moves="303030", row_count=6, column_count=7, window_length=4)
    assert isinstance(state, GameState)
    assert state.moves_played == 6
    assert state.winner == 0
    assert state.next_player == board.PLAYER_ONE
    assert not state.is_draw


def test_parse_history_rejects_illegal_token() -> None:
    """Ensure that non-digit tokens cause ``ValueError`` to be raised.

    Returns:
        None: This test does not return a value.

    """

    with pytest.raises(ValueError) as error:
        parse_history(starter=1, moves="0x3", row_count=6, column_count=7, window_length=4)
    assert "Illegal move token" in str(error.value)


def test_parse_history_rejects_moves_after_win() -> None:
    """Ensure histories that continue after a win are rejected.

    Returns:
        None: This test does not return a value.

    """

    winning_sequence = "01010102"
    with pytest.raises(ValueError) as error:
        parse_history(starter=1, moves=winning_sequence, row_count=6, column_count=7, window_length=4)
    assert "already been won" in str(error.value)


def test_parse_history_marks_draw() -> None:
    """Ensure histories that fill the board without a win are marked as draws.

    Returns:
        None: This test does not return a value.

    """

    draw_history = "0213203102132031"
    state = parse_history(starter=1, moves=draw_history, row_count=4, column_count=4, window_length=4)
    assert state.winner == 0
    assert state.is_draw
    assert state.next_player == 0
