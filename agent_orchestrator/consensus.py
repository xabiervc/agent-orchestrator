from __future__ import annotations

from pathlib import Path

from .artifacts import list_artifacts, read_json, write_json


def _valid_artifact(path: Path, expected_type: str | None = None) -> bool:
    try:
        data = read_json(path)
    except (OSError, ValueError):
        return False
    if expected_type is not None and data.get("type") not in {expected_type, None}:
        return False
    return isinstance(data, dict) and data.get("status", "completed") not in {"failed", "unavailable", "blocked"}


def calculate_consensus(run: Path, *, require_review: bool = True) -> dict:
    proposals = [p for p in list_artifacts(run / "proposals") if _valid_artifact(p, "proposal")]
    reviews = [p for p in list_artifacts(run / "reviews") if _valid_artifact(p, "review")]
    blocking: list[str] = []
    if not proposals:
        blocking.append("No valid proposal artifacts found.")
    if require_review and not reviews:
        blocking.append("No valid review artifacts found.")
    for directory in (run / "proposals", run / "reviews"):
        for path in list_artifacts(directory):
            if not _valid_artifact(path):
                blocking.append(f"Invalid or blocked artifact: {path.name}.")
    result = {"schema_version": 1, "type": "consensus", "run_id": run.name, "decision": "approve" if not blocking else "pending", "proposal_count": len(proposals), "review_count": len(reviews), "blocking_reasons": blocking}
    write_json(run / "consensus.json", result)
    return result
