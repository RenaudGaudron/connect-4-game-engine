"""Expose the public interface for the Connect 4 minimax engine package.

This module provides the package version metadata and re-exports the
:class:`connect4_engine.engine.Connect4Engine` class together with the
:class:`connect4_engine.engine.SuggestionResult` dataclass so that users can
import them directly from :mod:`connect4_engine`. The package offers a reusable
Connect 4 engine powered by a minimax search with alpha-beta pruning and a
companion command-line interface.

"""

from __future__ import annotations

from .engine import Connect4Engine, SuggestionResult

__all__ = ["Connect4Engine", "SuggestionResult"]
