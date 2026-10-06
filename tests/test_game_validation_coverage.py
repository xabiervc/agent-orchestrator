from __future__ import annotations

import pytest

from game_production.validation import validate_game_event


def test_validate_game_event_accepts_valid_event() -> None:
    assert validate_game_event({"event": "spawn", "entity_id": "player"}) is True


@pytest.mark.parametrize("payload", [{}, {"event": ""}, {"entity_id": "player"}])
def test_validate_game_event_rejects_invalid_event(payload: dict[str, str]) -> None:
    assert validate_game_event(payload) is False
