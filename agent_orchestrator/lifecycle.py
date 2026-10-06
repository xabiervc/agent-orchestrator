from __future__ import annotations

from enum import Enum
from pathlib import Path

from .runs import advance_run, create_run, load_run


class RunState(str, Enum):
    CREATED = "created"
    PLANNING = "planning"
    REVIEWING = "reviewing"
    CONSENSUS = "consensus"
    ADVANCED = "advanced"
    COMPLETED = "completed"
    FAILED = "failed"


_ALLOWED_TRANSITIONS = {
    "created": {"planning", "failed"},
    "planning": {"reviewing", "failed"},
    "reviewing": {"consensus", "failed"},
    "consensus": {"advanced", "completed", "failed"},
    "advanced": {"completed", "failed"},
    "completed": set(),
    "failed": set(),
}


def start_task(root: Path, task: str) -> Path:
    return create_run(root, task)


def advance_task(run: Path, state: str = "advanced") -> dict:
    return advance_run(run, state)


def transition_task(run: Path, state: str) -> dict:
    payload = load_run(run)
    current = payload.get("state", "created")
    if state not in {member.value for member in RunState}:
        raise ValueError(f"Unknown run state: {state}")
    if state != current and state not in _ALLOWED_TRANSITIONS.get(current, set()):
        raise ValueError(f"Invalid transition: {current} -> {state}")
    return advance_run(run, state)


def current_state(run: Path) -> dict:
    return load_run(run)
