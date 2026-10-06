import json
from pathlib import Path

from agent_orchestrator.config import load_project_config, write_project_config
from agent_orchestrator.consensus import calculate_consensus
from agent_orchestrator.runs import create_run


def test_approved_run_requires_proposal(tmp_path: Path):
    write_project_config(tmp_path, {"project": {"name": "demo"}, "profiles": ["generic"]})
    config = load_project_config(tmp_path)
    run = create_run(tmp_path, config, "Task")
    (run / "proposals" / "planner.json").write_text(json.dumps({"schema_version": 1, "type": "proposal", "run_id": run.name, "status": "completed", "verdict": "approve"}))
    (run / "reviews" / "reviewer.json").write_text(json.dumps({"schema_version": 1, "type": "review", "run_id": run.name, "status": "completed", "verdict": "approve"}))
    assert calculate_consensus(run)["decision"] == "approve"
