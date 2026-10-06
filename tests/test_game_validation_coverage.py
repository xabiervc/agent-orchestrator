from __future__ import annotations

import game_production.validation as validation


def test_game_validation_module_imports() -> None:
    assert validation is not None
