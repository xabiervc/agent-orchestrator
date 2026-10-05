from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import uuid

from .artifacts import write_json
from .config import ProjectConfig
from .schemas import consensus_artifact, task_artifact


def create_run(root: Path, config: ProjectConfig, task: str) -> Path:
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
    run = root / ".agent" / "runs" / run_id
    for child in ("proposals", "reviews", "prompts", "evidence"):
        (run / child).mkdir(parents=True, exist_ok=True)
    write_json(run / "task.json", task_artifact(run_id, task, config.raw))
    write_json(run / "consensus.json", consensus_artifact(run_id))
    return run


def latest_run(root: Path) -> Path | None:
    runs = root / ".agent" / "runs"
    if not runs.exists():
        return None
    candidates = sorted((path for path in runs.iterdir() if path.is_dir()), key=lambda path: path.name, reverse=True)
    return candidates[0] if candidates else None
