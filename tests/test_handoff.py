import json
from pathlib import Path

import pytest

from agent_orchestrator.handoff import create_handoff


def test_handoff_requires_approval(tmp_path: Path):
    run = tmp_path / "run"
    run.mkdir()
    (run / "consensus.json").write_text(json.dumps({"decision": "pending", "run_id": "run"}))
    with pytest.raises(ValueError):
        create_handoff(run, "claude-code", "sonnet", [], [])


def test_handoff_is_scope_locked(tmp_path: Path):
    run = tmp_path / "run"
    run.mkdir()
    (run / "consensus.json").write_text(json.dumps({"decision": "approve", "run_id": "run"}))
    result = create_handoff(run, "claude-code", "sonnet", ["src/player.gd"], ["godot --headless"])
    assert result["scope_locked"] is True
