from __future__ import annotations

import json
from pathlib import Path


VALID_VERDICTS = {"approve", "reject", "changes_requested"}


def _valid_artifact(path: Path) -> bool:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    if data.get("status") in {"failed", "unavailable", "blocked"}:
        return False
    return True


def _artifact_verdict(path: Path) -> str | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    verdict = data.get("verdict")
    return verdict if verdict in VALID_VERDICTS else None


def calculate_consensus(run: Path) -> dict:
    proposals = sorted((run / "proposals").glob("*.json"))
    reviews = sorted((run / "reviews").glob("*.json"))
    invalid = [path.name for path in proposals + reviews if not _valid_artifact(path)]
    approvals = [path.name for path in proposals + reviews if _valid_artifact(path) and _artifact_verdict(path) == "approve"]
    non_approvals = [path.name for path in proposals + reviews if _valid_artifact(path) and _artifact_verdict(path) in {"reject", "changes_requested"}]
    missing_verdict = [path.name for path in proposals + reviews if _valid_artifact(path) and _artifact_verdict(path) is None]
    reasons = []
    if invalid:
        reasons.append("invalid_artifacts")
    if non_approvals:
        reasons.append("non_approval_verdicts")
    if missing_verdict:
        reasons.append("missing_or_invalid_verdicts")
    approved = bool(approvals) and not invalid and not non_approvals and not missing_verdict
    return {
        "approved": approved,
        "proposal_count": len(proposals),
        "review_count": len(reviews),
        "approval_count": len(approvals),
        "non_approval_count": len(non_approvals),
        "missing_verdict_count": len(missing_verdict),
        "invalid_artifacts": invalid,
        "approval_artifacts": approvals,
        "non_approval_artifacts": non_approvals,
        "missing_verdict_artifacts": missing_verdict,
        "reasons": reasons,
    }
