from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from .artifacts import read_json, write_json


def _run_path(root: Path, run_id: str) -> Path:
    return root / ".agent" / "runs" / run_id


def create_run(root: Path, task: str) -> Path:
    run_id = f"run-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{uuid4().hex[:8]}"
    run = _run_path(root, run_id)
    for directory in ("proposals", "reviews", "evidence", "exports"):
        (run / directory).mkdir(parents=True, exist_ok=True)
    write_json(run / "run.json", {"schema_version": 1, "run_id": run_id, "task": task, "state": "created"})
    return run


def load_run(run: Path) -> dict[str, Any]:
    return read_json(run / "run.json")


def save_run(run: Path, payload: dict[str, Any]) -> None:
    write_json(run / "run.json", payload)


def advance_run(run: Path, state: str) -> dict[str, Any]:
    payload = load_run(run)
    payload["state"] = state
    save_run(run, payload)
    return payload
