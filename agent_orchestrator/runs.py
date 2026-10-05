from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import json
import uuid

from .config import ProjectConfig


def create_run(root: Path, config: ProjectConfig, task: str) -> Path:
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
    run = root / ".agent" / "runs" / run_id
    for child in ("proposals", "reviews", "prompts", "evidence"):
        (run / child).mkdir(parents=True, exist_ok=True)
    (run / "task.json").write_text(json.dumps({"run_id": run_id, "task": task, "project": config.raw}, indent=2) + "\n", encoding="utf-8")
    (run / "consensus.json").write_text(json.dumps({"decision": "pending", "run_id": run_id}, indent=2) + "\n", encoding="utf-8")
    return run


def latest_run(root: Path) -> Path | None:
    runs = root / ".agent" / "runs"
    if not runs.exists():
        return None
    candidates = sorted((p for p in runs.iterdir() if p.is_dir()), reverse=True)
    return candidates[0] if candidates else None
