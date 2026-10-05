from __future__ import annotations

from pathlib import Path
import re
from typing import Any

from .artifacts import list_artifacts, read_json

SCHEMA_VERSION = 1
VALID_STATUSES = {"completed", "pending"}
BLOCKED_STATUSES = {"failed", "unavailable", "blocked"}
SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|token|secret|password)\s*[:=]\s*['\"]?[^\s'\"]{8,}"),
    re.compile(r"(?i)bearer\s+[a-z0-9._-]{12,}"),
]


def _secret_text(value: Any) -> str:
    if isinstance(value, dict):
        return " ".join(f"{key} {value}" for key, value in value.items())
    if isinstance(value, list):
        return " ".join(_secret_text(item) for item in value)
    return str(value)


def contains_secret_like_value(data: Any) -> bool:
    text = _secret_text(data)
    return any(pattern.search(text) for pattern in SECRET_PATTERNS)


def validate_artifact(path: Path, expected_type: str | None = None, run_id: str | None = None) -> list[str]:
    errors: list[str] = []
    try:
        data = read_json(path)
    except (OSError, ValueError) as exc:
        return [f"{path.name}: invalid JSON: {exc}"]
    if not isinstance(data, dict):
        return [f"{path.name}: artifact must be an object."]
    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"{path.name}: unsupported schema_version.")
    if expected_type and data.get("type") != expected_type:
        errors.append(f"{path.name}: expected type {expected_type!r}.")
    if run_id and data.get("run_id") != run_id:
        errors.append(f"{path.name}: run_id does not match {run_id!r}.")
    status = data.get("status")
    if status in BLOCKED_STATUSES:
        errors.append(f"{path.name}: blocked status {status!r}.")
    if status is not None and status not in VALID_STATUSES and status not in BLOCKED_STATUSES:
        errors.append(f"{path.name}: unsupported status {status!r}.")
    if contains_secret_like_value(data):
        errors.append(f"{path.name}: secret-like value detected.")
    return errors


def validate_run(run: Path) -> list[str]:
    errors: list[str] = []
    task = run / "task.json"
    consensus = run / "consensus.json"
    errors.extend(validate_artifact(task, "task", run.name) if task.exists() else ["Missing task.json."])
    errors.extend(validate_artifact(consensus, "consensus", run.name) if consensus.exists() else ["Missing consensus.json."])
    for directory, expected in (("proposals", "proposal"), ("reviews", "review"), ("evidence", "evidence")):
        for path in list_artifacts(run / directory):
            errors.extend(validate_artifact(path, expected, run.name))
    if consensus.exists():
        data = read_json(consensus)
        if data.get("decision") == "approve":
            proposals = list_artifacts(run / "proposals")
            reviews = list_artifacts(run / "reviews")
            if not proposals:
                errors.append("Approved consensus requires proposals.")
            if not reviews:
                errors.append("Approved consensus requires reviews.")
            if data.get("conflicts"):
                errors.append("Approved consensus cannot contain unresolved conflicts.")
    return errors
