from __future__ import annotations

from pathlib import Path

from .artifacts import list_artifacts, read_json, write_json
from .validation import validate_artifact


def calculate_consensus(run: Path, *, require_review: bool = True) -> dict:
    proposals = list_artifacts(run / "proposals")
    reviews = list_artifacts(run / "reviews")
    blocking: list[str] = []
    for path in proposals:
        blocking.extend(validate_artifact(path, "proposal", run.name))
    for path in reviews:
        blocking.extend(validate_artifact(path, "review", run.name))
    if not proposals:
        blocking.append("No proposal artifacts found.")
    if require_review and not reviews:
        blocking.append("No review artifacts found.")
    for path in proposals + reviews:
        try:
            data = read_json(path)
        except (OSError, ValueError):
            continue
        if data.get("conflicts"):
            blocking.append(f"Unresolved conflicts in {path.name}.")
    result = {"schema_version": 1, "type": "consensus", "run_id": run.name, "decision": "approve" if not blocking else "pending", "proposal_count": len(proposals), "review_count": len(reviews), "blocking_reasons": sorted(set(blocking)), "conflicts": []}
    write_json(run / "consensus.json", result)
    return result
