from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4
from typing import Any

from .artifacts import read_json, write_json


def _write_run_payload(run: Path, payload: dict) -> None:
    write_json(run / "run.json", payload)
    write_json(run / "state.json", payload)


def create_run(root: Path, config_or_task: Any, task: str | None = None) -> Path:
    config = config_or_task if isinstance(config_or_task, dict) else None
    task_text = task if task is not None else str(config_or_task)
    if not task_text.strip():
        raise ValueError("Task is required.")
    run_id = f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{uuid4().hex[:8]}"
    run = root / ".agent" / "runs" / run_id
    payload = {"run_id": run_id, "task": task_text.strip(), "state": "created", "history": ["created"]}
    if config is not None:
        payload["config"] = config
        payload["proposal"] = {"task": task_text.strip(), "status": "pending"}
    _write_run_payload(run, payload)
    write_json(run / "evidence" / "manifest.json", {"entries": []})
    (run / "proposals").mkdir(parents=True, exist_ok=True)
    return run


def load_run(run: Path) -> dict:
    state_path = run / "state.json"
    if state_path.exists():
        return read_json(state_path)
    return read_json(run / "run.json")


def advance_run(run: Path, state: str = "advanced") -> dict:
    payload = load_run(run)
    payload["state"] = state
    payload.setdefault("history", []).append(state)
    _write_run_payload(run, payload)
    return payload


def latest_run(root: Path) -> Path | None:
    runs = root / ".agent" / "runs"
    if not runs.exists():
        return None
    candidates = sorted((path for path in runs.iterdir() if path.is_dir()), reverse=True)
    return candidates[0] if candidates else None
