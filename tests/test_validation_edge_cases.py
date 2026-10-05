import json
from pathlib import Path

from agent_orchestrator.validation import contains_secret_like_value, validate_artifact, validate_run


def test_rejects_wrong_run_id(tmp_path: Path):
    path = tmp_path / "proposal.json"
    path.write_text(json.dumps({"schema_version": 1, "type": "proposal", "run_id": "other", "status": "completed"}))
    assert validate_artifact(path, "proposal", "expected")


def test_rejects_secret_like_value(tmp_path: Path):
    path = tmp_path / "proposal.json"
    path.write_text(json.dumps({"schema_version": 1, "type": "proposal", "run_id": "run", "status": "completed", "api_key": "abcdefghijklmnop"}))
    assert validate_artifact(path, "proposal", "run")
    assert contains_secret_like_value({"token": "abcdefghijklmnop"})


def test_accepts_safe_metadata(tmp_path: Path):
    path = tmp_path / "proposal.json"
    path.write_text(json.dumps({"schema_version": 1, "type": "proposal", "run_id": "run", "status": "completed", "token_count": 12, "description": "Review the token budget."}))
    assert validate_artifact(path, "proposal", "run") == []


def test_rejects_nested_secret_like_value():
    assert contains_secret_like_value({"provider": {"authorization": "Bearer abcdefghijklmnop"}})


def test_rejects_approved_consensus_with_conflicts(tmp_path: Path):
    run = tmp_path / "run"
    (run / "proposals").mkdir(parents=True)
    (run / "reviews").mkdir()
    (run / "evidence").mkdir()
    base = {"schema_version": 1, "run_id": "run", "status": "completed"}
    (run / "task.json").write_text(json.dumps({**base, "type": "task"}))
    (run / "consensus.json").write_text(json.dumps({**base, "type": "consensus", "decision": "approve", "conflicts": ["scope"]}))
    (run / "proposals" / "proposal.json").write_text(json.dumps({**base, "type": "proposal"}))
    (run / "reviews" / "review.json").write_text(json.dumps({**base, "type": "review"}))
    assert validate_run(run)
