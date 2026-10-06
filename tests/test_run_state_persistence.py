import json
from pathlib import Path

from agent_orchestrator.config import ProjectConfig
from agent_orchestrator.runs import create_run


def test_run_json_persists_created_state(tmp_path: Path):
    run = create_run(tmp_path, ProjectConfig("demo", raw={"project": {"name": "demo"}}), "Task")
    data = json.loads((run / "run.json").read_text())
    assert data["state"] == "created"
    assert data["run_id"] == run.name
