import json
from pathlib import Path

from agent_orchestrator.consensus import calculate_consensus


def test_consensus_stays_pending_without_review(tmp_path: Path):
    run = tmp_path / "run"
    (run / "proposals").mkdir(parents=True)
    (run / "reviews").mkdir()
    (run / "proposals" / "planner.json").write_text(json.dumps({"type": "proposal", "status": "completed"}))
    result = calculate_consensus(run)
    assert result["decision"] == "pending"


def test_consensus_approves_valid_proposal_and_review(tmp_path: Path):
    run = tmp_path / "run"
    (run / "proposals").mkdir(parents=True)
    (run / "reviews").mkdir()
    for directory, filename, kind in [("proposals", "planner.json", "proposal"), ("reviews", "reviewer.json", "review")]:
        (run / directory / filename).write_text(json.dumps({"type": kind, "status": "completed"}))
    assert calculate_consensus(run)["decision"] == "approve"
