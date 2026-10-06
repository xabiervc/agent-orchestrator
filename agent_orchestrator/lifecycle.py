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

    def __new__(cls, value: str = "created"):
        obj = str.__new__(cls, value)
        obj._value_ = value
        return obj

    def transition(self, target: str) -> "RunState":
        allowed = {
            "created": {"planning", "failed"},
            "planning": {"reviewing", "failed"},
            "reviewing": {"consensus", "failed"},
            "consensus": {"advanced", "completed", "failed"},
            "advanced": {"completed", "failed"},
            "completed": set(),
            "failed": set(),
        }
        if target not in {member.value for member in RunState}:
            raise ValueError(f"Unknown run state: {target}")
        if target != self.value and target not in allowed.get(self.value, set()):
            raise ValueError(f"Invalid transition: {self.value} -> {target}")
        return RunState(target)


def start_task(root: Path, task: str) -> Path:
    return create_run(root, task)


def advance_task(run: Path, state: str = "advanced") -> dict:
    return advance_run(run, state)


def transition_task(run: Path, state: str) -> dict:
    payload = load_run(run)
    current = RunState(payload.get("state", "created"))
    current.transition(state)
    return advance_run(run, state)


def current_state(run: Path) -> dict:
    return load_run(run)
