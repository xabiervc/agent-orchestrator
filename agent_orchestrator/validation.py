from __future__ import annotations

from pathlib import Path
import re
from typing import Any

from .artifacts import list_artifacts, read_json

SCHEMA_VERSION = 1
VALID_STATUSES = {"completed", "pending"}
BLOCKED_STATUSES = {"failed", "unavailable", "blocked"}
SENSITIVE_KEYS = {"api_key", "apikey", "token", "secret", "password", "authorization", "access_token", "refresh_token"}
SECRET_PATTERNS = [
    re.compile(r"(?i)bearer\s+[a-z0-9._-]{12,}"),
    re.compile(r"(?i)sk-[a-z0-9_-]{12,}"),
]


def _looks_secret(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    stripped = value.strip()
    if len(stripped) < 8:
        return False
    return bool(re.search(r"[A-Za-z]", stripped) and re.search(r"[0-9]|[_./+=-]", stripped)) or bool(SECRET_PATTERNS[0].search(stripped)) or bool(SECRET_PATTERNS[1].search(stripped))


def contains_secret_like_value(data: Any) -> bool:
    if isinstance(data, dict):
        for key, value in data.items():
            normalized = str(key).lower().replace("-", "_")
            if normalized in SENSITIVE_KEYS and _looks_secret(value):
                return True
            if contains_secret_like_value(value):
                return True
        return False
    if isinstance(data, list):
        return any(contains_secret_like_value(item) for item in data)
    return bool(isinstance(data, str) and any(pattern.search(data) for pattern in SECRET_PATTERNS))


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
