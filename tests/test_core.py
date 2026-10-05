from pathlib import Path
import json

from agent_orchestrator.config import load_project_config, write_project_config
from agent_orchestrator.consensus import calculate_consensus
from agent_orchestrator.runs import create_run, latest_run
from agent_orchestrator.validation import validate_run


def test_run_starts_and_blocks_without_artifacts(tmp_path: Path):
    write_project_config(tmp_path, {"project": {"name": "demo"}, "profiles": ["generic"]})
    config = load_project_config(tmp_path)
    run = create_run(tmp_path, config, "Inspect the project")
    result = calculate_consensus(run)
    assert result["decision"] == "pending"
    assert validate_run(run) == []


def test_approved_run_requires_proposal(tmp_path: Path):
    write_project_config(tmp_path, {"project": {"name": "demo"}, "profiles": ["generic"]})
    config = load_project_config(tmp_path)
    run = create_run(tmp_path, config, "Task")
    (run / "proposals" / "planner.json").write_text(json.dumps({"schema_version": 1, "type": "proposal", "run_id": run.name, "status": "completed"}))
    (run / "reviews" / "reviewer.json").write_text(json.dumps({"schema_version": 1, "type": "review", "run_id": run.name, "status": "completed"}))
    assert calculate_consensus(run)["decision"] == "approve"
    assert validate_run(run) == []


def test_latest_run_ignores_files(tmp_path: Path):
    runs = tmp_path / ".agent" / "runs"
    (runs / "20260101T000000Z-old").mkdir(parents=True)
    (runs / "README.md").write_text("not a run")
    (runs / "20260102T000000Z-new").mkdir()
    assert latest_run(tmp_path).name == "20260102T000000Z-new"
