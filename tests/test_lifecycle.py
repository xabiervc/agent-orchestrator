import pytest

from agent_orchestrator.lifecycle import RunState


def test_valid_lifecycle_transition():
    state = RunState().transition("planning").transition("reviewing")
    assert state.state == "reviewing"


def test_invalid_lifecycle_transition():
    with pytest.raises(ValueError):
        RunState().transition("approved")
