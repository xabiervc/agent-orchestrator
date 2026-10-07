from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RoutingPolicy:
    exploration: str = "haiku"
    normal: str = "sonnet"
    complex: str = "opus"
    extended: str = "fable"
    allow_extended: bool = False
    require_consensus: bool = True
    max_parallel_implementers: int = 1

    @classmethod
    def from_config(cls, data: dict[str, Any]) -> RoutingPolicy:
        routing = data.get("routing", {})
        policy = data.get("policy", {})
        return cls(
            exploration=routing.get("exploration", "haiku"),
            normal=routing.get("normal", "sonnet"),
            complex=routing.get("complex", "opus"),
            extended=routing.get("extended", "fable"),
            allow_extended=policy.get("allow_extended", False),
            require_consensus=policy.get("require_consensus", True),
            max_parallel_implementers=policy.get("max_parallel_implementers", 1),
        )

    def model_for(self, risk: str) -> str:
        if risk in {"critical", "high"}:
            return self.complex
        if risk in {"low", "mechanical"}:
            return self.exploration
        return self.normal
