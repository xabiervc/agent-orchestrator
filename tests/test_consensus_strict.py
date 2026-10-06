import json
from pathlib import Path

from agent_orchestrator.consensus import calculate_consensus


def _write(path: Path, kind: str, **extra):
    path.write_text(json.dumps({"schema_version": 1, "type": kind, "run_id": "run", "status": "completed", **extra}))


def test_consensus_stays_pending_without_review(tmp_path: Path):
    run = tmp_path / "run"
    (run / "proposals").mkdir(parents=True)
    (run / "reviews").mkdir()
    _write(run / "proposals" / "planner.json", "proposal")
    result = calculate_consensus(run)
    assert result["decision"] == "pending"
    assert result["approved"] is False


def test_consensus_approves_valid_proposal_and_review(tmp_path: Path):
    run = tmp_path / "run"
    (run / "proposals").mkdir(parents=True)
    (run / "reviews").mkdir()
    _write(run / "proposals" / "planner.json", "proposal", verdict="approve")
    _write(run / "reviews" / "reviewer.json", "review", verdict="approve")
    result = calculate_consensus(run)
    assert result["decision"] == "approve"
    assert result["approved"] is True


def test_consensus_rejects_explicit_rejection(tmp_path: Path):
    run = tmp_path / "run"
    (run / "proposals").mkdir(parents=True)
    (run / "reviews").mkdir()
    _write(run / "proposals" / "planner.json", "proposal", verdict="approve")
    _write(run / "reviews" / "reviewer.json", "review", verdict="reject")
    result = calculate_consensus(run)
    assert result["decision"] == "reject"
    assert result["approved"] is False


def test_consensus_does_not_implicitly_approve_missing_verdict(tmp_path: Path):
    run = tmp_path / "run"
    (run / "proposals").mkdir(parents=True)
    (run / "reviews").mkdir()
    _write(run / "proposals" / "planner.json", "proposal", verdict="approve")
    _write(run / "reviews" / "reviewer.json", "review")
    result = calculate_consensus(run)
    assert result["decision"] == "pending"
    assert result["missing_verdict_count"] == 1
