import json
from pathlib import Path

from agent_orchestrator.cli import main


def test_end_to_end_lifecycle_and_quality(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    assert main(["init", "--profile", "generic"]) == 0
    assert main(["start", "--task", "Release smoke test"]) == 0
    for state in ("planning", "reviewing", "consensus"):
        assert main(["transition", "--to", state]) == 0
    assert main(["quality", "--command", "tests=python -c \\\"print(1)\\\""]) == 0
    run = next((tmp_path / ".agent" / "runs").iterdir())
    run_data = json.loads((run / "run.json").read_text())
    state_data = json.loads((run / "state.json").read_text())
    evidence = json.loads((run / "evidence" / "manifest.json").read_text())
    assert run_data["state"] == "consensus"
    assert state_data["history"][-1] == "consensus"
    assert evidence["entries"]
    assert (tmp_path / ".agent" / "project.json").exists()
