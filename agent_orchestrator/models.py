from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

ModelAlias = Literal["haiku", "sonnet", "opus", "fable", "default", "auto"]


@dataclass(frozen=True)
class Route:
    role: str
    provider: str
    model: ModelAlias
    effort: str = "medium"
    reason: str = ""


DEFAULT_ROUTES = {
    "exploration": Route("exploration", "claude-code", "haiku", "low", "mechanical or read-only work"),
    "planning": Route("planning", "claude-code", "sonnet", "medium", "normal planning"),
    "review": Route("review", "codex", "default", "medium", "independent review when available"),
    "low_risk_implementation": Route("low_risk_implementation", "copilot", "auto", "medium", "localized implementation"),
    "normal_implementation": Route("normal_implementation", "codex", "default", "medium", "normal implementation"),
    "complex_implementation": Route("complex_implementation", "claude-code", "opus", "high", "architecture or high-risk implementation"),
    "architecture_review": Route("architecture_review", "claude-code", "opus", "high", "architecture and persistence review"),
}
