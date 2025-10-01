"""Test the command-line interface wrapper.

The tests cover terminal detection messaging, standard move output, and error
handling paths for invalid histories.

"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from connect4_engine import cli

if TYPE_CHECKING:
    from pytest import CaptureFixture


def test_cli_reports_existing_win_player_one(capsys: CaptureFixture[str]) -> None:
    """Ensure the CLI reports an existing Player 1 victory.

    Args:
        capsys: Pytest fixture used to capture the CLI output.

    Returns:
        None: This test does not return a value.

    """

    exit_code = cli.main([
        "--starter",
        "1",
        "--history",
        "0101010",
    ])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out.strip() == "Player 1 won!"


def test_cli_reports_existing_win_player_two(capsys: CaptureFixture[str]) -> None:
    """Ensure the CLI reports an existing Player 2 victory.

    Args:
        capsys: Pytest fixture used to capture the CLI output.

    Returns:
        None: This test does not return a value.

    """

    exit_code = cli.main([
        "--starter",
        "2",
        "--history",
        "0101010",
    ])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out.strip() == "Player 2 won!"


def test_cli_reports_draw(capsys: CaptureFixture[str]) -> None:
    """Ensure the CLI prints the draw message for a full-board draw.

    Args:
        capsys: Pytest fixture used to capture the CLI output.

    Returns:
        None: This test does not return a value.

    """

    exit_code = cli.main([
        "--starter",
        "1",
        "--history",
        "0213203102132031",
        "--rows",
        "4",
        "--columns",
        "4",
        "--window",
        "4",
    ])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out.strip() == "Draw!"


def test_cli_reports_move_and_win(capsys: CaptureFixture[str]) -> None:
    """Ensure the CLI prints the move followed by the winning message.

    Args:
        capsys: Pytest fixture used to capture the CLI output.

    Returns:
        None: This test does not return a value.

    """

    exit_code = cli.main([
        "--starter",
        "1",
        "--history",
        "041425",
        "--depth",
        "3",
    ])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out.splitlines() == ["3", "Player 1 won!"]


def test_cli_reports_move_only_when_no_immediate_win(capsys: CaptureFixture[str]) -> None:
    """Ensure the CLI prints only the move when no win follows immediately.

    Args:
        capsys: Pytest fixture used to capture the CLI output.

    Returns:
        None: This test does not return a value.

    """

    exit_code = cli.main([
        "--starter",
        "1",
    ])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out.strip().isdigit()


def test_cli_rejects_invalid_history() -> None:
    """Ensure the CLI exits with an error for invalid history strings.

    Returns:
        None: This test does not return a value.

    """

    with pytest.raises(SystemExit) as exit_info:
        cli.main([
            "--starter",
            "1",
            "--history",
            "0x3",
        ])
    assert exit_info.value.code == 2
