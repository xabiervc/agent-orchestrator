from __future__ import annotations

from dataclasses import dataclass

STATES = ("created", "planning", "reviewing", "consensus", "approved", "implementing", "verifying", "completed", "blocked", "failed")
ALLOWED = {
    "created": {"planning", "blocked", "failed"},
    "planning": {"reviewing", "blocked", "failed"},
    "reviewing": {"consensus", "blocked", "failed"},
    "consensus": {"approved", "blocked", "failed"},
    "approved": {"implementing", "blocked", "failed"},
    "implementing": {"verifying", "blocked", "failed"},
    "verifying": {"completed", "blocked", "failed"},
    "completed": set(),
    "blocked": {"planning", "failed"},
    "failed": {"planning"},
}


@dataclass(frozen=True)
class RunState:
    state: str = "created"

    def transition(self, target: str) -> "RunState":
        if target not in STATES:
            raise ValueError(f"Unknown run state: {target}")
        if target not in ALLOWED[self.state]:
            raise ValueError(f"Invalid transition: {self.state} -> {target}")
        return RunState(target)
