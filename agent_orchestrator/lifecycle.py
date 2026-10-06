from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .runs import advance_run, create_run, load_run


@dataclass(frozen=True)
class _StateValue:
    value: str

    def transition(self, target: str) -> "_StateValue":
        allowed = {
            "created": {"planning", "failed"},
            "planning": {"reviewing", "failed"},
            "reviewing": {"consensus", "failed"},
            "consensus": {"advanced", "completed", "failed"},
            "advanced": {"completed", "failed"},
            "completed": set(),
            "failed": set(),
        }
        if target not in allowed:
            raise ValueError(f"Unknown run state: {target}")
        if target != self.value and target not in allowed[self.value]:
            raise ValueError(f"Invalid transition: {self.value} -> {target}")
        return _StateValue(target)

    def __str__(self) -> str:
        return self.value


class RunState:
    CREATED = _StateValue("created")
    PLANNING = _StateValue("planning")
    REVIEWING = _StateValue("reviewing")
    CONSENSUS = _StateValue("consensus")
    ADVANCED = _StateValue("advanced")
    COMPLETED = _StateValue("completed")
    FAILED = _StateValue("failed")

    def __init__(self, value: str = "created") -> None:
        if value not in {state.value for state in (self.CREATED, self.PLANNING, self.REVIEWING, self.CONSENSUS, self.ADVANCED, self.COMPLETED, self.FAILED)}:
            raise ValueError(f"Unknown run state: {value}")
        self.value = value

    def transition(self, target: str) -> "RunState":
        _StateValue(self.value).transition(target)
        return RunState(target)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, RunState) and self.value == other.value

    def __repr__(self) -> str:
        return f"RunState({self.value!r})"


def start_task(root: Path, task: str) -> Path:
    return create_run(root, task)


def advance_task(run: Path, state: str = "advanced") -> dict:
    return advance_run(run, state)


def transition_task(run: Path, state: str) -> dict:
    payload = load_run(run)
    RunState(payload.get("state", "created")).transition(state)
    return advance_run(run, state)


def current_state(run: Path) -> dict:
    return load_run(run)
