from __future__ import annotations

from agent_orchestrator.schemas import validate_payload


def test_validate_payload_accepts_mapping() -> None:
    assert validate_payload({"name": "demo"}) == {"name": "demo"}


def test_validate_payload_rejects_non_mapping() -> None:
    try:
        validate_payload(["invalid"])
    except (TypeError, ValueError):
        pass
    else:
        raise AssertionError("non-mapping payload should be rejected")
