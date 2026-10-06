from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from .artifacts import read_json, write_json


def create_run(root: Path, task: str) -> Path:
    if not task.strip():
        raise ValueError("Task is required.")
    run_id = f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{uuid4().hex[:8]}"
    run = root / ".agent" / "runs" / run_id
    write_json(run / "state.json", {"run_id": run_id, "task": task.strip(), "state": "created", "history": ["created"]})
    write_json(run / "evidence" / "manifest.json", {"entries": []})
    return run


def load_run(run: Path) -> dict:
    return read_json(run / "state.json")


def advance_run(run: Path, state: str = "advanced") -> dict:
    payload = load_run(run)
    payload["state"] = state
    payload.setdefault("history", []).append(state)
    write_json(run / "state.json", payload)
    return payload
