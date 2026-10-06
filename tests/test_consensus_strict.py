import json
from pathlib import Path

from agent_orchestrator.consensus import calculate_consensus


def _write(path: Path, kind: str, **extra):
    path.write_text(json.dumps({"schema_version": 1, "type": kind, "run_id": "run", "status": "completed", **extra}))


def _run(tmp_path: Path) -> Path:
    run = tmp_path / "run"
    (run / "proposals").mkdir(parents=True)
    (run / "reviews").mkdir()
    return run


def test_consensus_stays_pending_without_review(tmp_path: Path):
    run = _run(tmp_path)
    _write(run / "proposals" / "planner.json", "proposal")
    result = calculate_consensus(run)
    assert result["decision"] == "pending"
    assert result["approved"] is False


def test_consensus_approves_valid_proposal_and_review(tmp_path: Path):
    run = _run(tmp_path)
    _write(run / "proposals" / "planner.json", "proposal", verdict="approve")
    _write(run / "reviews" / "reviewer.json", "review", verdict="approve")
    result = calculate_consensus(run)
    assert result["decision"] == "approve"
    assert result["approved"] is True


def test_consensus_rejects_explicit_rejection(tmp_path: Path):
    run = _run(tmp_path)
    _write(run / "proposals" / "planner.json", "proposal", verdict="approve")
    _write(run / "reviews" / "reviewer.json", "review", verdict="reject")
    result = calculate_consensus(run)
    assert result["decision"] == "reject"


def test_changes_requested_is_not_approval(tmp_path: Path):
    run = _run(tmp_path)
    _write(run / "proposals" / "planner.json", "proposal", verdict="approve")
    _write(run / "reviews" / "reviewer.json", "review", verdict="changes_requested")
    result = calculate_consensus(run)
    assert result["decision"] == "pending"
    assert result["approved"] is False


def test_mixed_verdicts_are_not_approved(tmp_path: Path):
    run = _run(tmp_path)
    _write(run / "proposals" / "planner.json", "proposal", verdict="approve")
    _write(run / "reviews" / "rejecting.json", "review", verdict="reject")
    _write(run / "reviews" / "approving.json", "review", verdict="approve")
    result = calculate_consensus(run)
    assert result["decision"] == "reject"
    assert result["approved"] is False


def test_invalid_status_blocks_consensus(tmp_path: Path):
    run = _run(tmp_path)
    _write(run / "proposals" / "planner.json", "proposal", verdict="approve")
    _write(run / "reviews" / "reviewer.json", "review", status="blocked", verdict="approve")
    result = calculate_consensus(run)
    assert result["decision"] == "pending"
    assert result["invalid_artifacts"] == ["reviewer.json"]
