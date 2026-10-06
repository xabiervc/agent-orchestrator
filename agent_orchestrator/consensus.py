from __future__ import annotations

import json
from pathlib import Path


VALID_VERDICTS = {"approve", "reject", "changes_requested"}


def _read_artifact(path: Path) -> dict | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def _valid_artifact(path: Path) -> bool:
    data = _read_artifact(path)
    return data is not None and data.get("status") not in {"failed", "unavailable", "blocked"}


def _artifact_verdict(path: Path) -> str | None:
    data = _read_artifact(path)
    verdict = data.get("verdict") if data else None
    return verdict if verdict in VALID_VERDICTS else None


def calculate_consensus(run: Path) -> dict:
    proposals = sorted((run / "proposals").glob("*.json"))
    reviews = sorted((run / "reviews").glob("*.json"))
    artifacts = proposals + reviews
    invalid = [path.name for path in artifacts if not _valid_artifact(path)]
    approvals = [path.name for path in artifacts if _valid_artifact(path) and _artifact_verdict(path) == "approve"]
    non_approvals = [path.name for path in artifacts if _valid_artifact(path) and _artifact_verdict(path) in {"reject", "changes_requested"}]
    missing_verdict = [path.name for path in artifacts if _valid_artifact(path) and _artifact_verdict(path) is None]
    reasons = []
    if invalid:
        reasons.append("invalid_artifacts")
    if non_approvals:
        reasons.append("non_approval_verdicts")
    if missing_verdict:
        reasons.append("missing_or_invalid_verdicts")
    if invalid or non_approvals or missing_verdict:
        decision = "reject" if non_approvals else "pending"
    elif approvals:
        decision = "approve"
    else:
        decision = "pending"
    return {
        "decision": decision,
        "approved": decision == "approve",
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
