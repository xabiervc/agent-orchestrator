import json
from pathlib import Path

from agent_orchestrator.cli import main


def test_cli_can_create_and_advance_run(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    assert main(["init", "--profile", "generic"]) == 0
    assert main(["start", "--task", "Test lifecycle"]) == 0
    for state in ("planning", "reviewing", "consensus"):
        assert main(["transition", "--to", state]) == 0
    run_dirs = list((tmp_path / ".agent" / "runs").iterdir())
    data = json.loads((run_dirs[0] / "run.json").read_text())
    assert data["state"] == "consensus"


def test_cli_quality_returns_failure_code():
    assert main(["quality", "--result", "tests=false"]) == 1
