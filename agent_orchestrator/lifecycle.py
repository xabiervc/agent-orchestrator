from __future__ import annotations

from enum import Enum
from pathlib import Path

from .runs import advance_run, create_run, load_run


class RunState(str, Enum):
    CREATED = "created"
    PLANNING = "planning"
    ADVANCED = "advanced"
    COMPLETED = "completed"
    FAILED = "failed"


def start_task(root: Path, task: str) -> Path:
    return create_run(root, task)


def advance_task(run: Path, state: str = "advanced") -> dict:
    return advance_run(run, state)


def transition_task(run: Path, state: str) -> dict:
    allowed = {member.value for member in RunState}
    if state not in allowed:
        raise ValueError(f"Unknown run state: {state}")
    return advance_run(run, state)


def current_state(run: Path) -> dict:
    return load_run(run)
