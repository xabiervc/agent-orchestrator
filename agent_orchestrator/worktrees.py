from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WorktreePlan:
    required: bool
    branch: str
    path: str
    reason: str


def plan_worktree(run_id: str, risk: str, parallel_agents: int = 1) -> WorktreePlan:
    required = parallel_agents > 1 or risk in {"high", "critical"}
    return WorktreePlan(required, f"agent/{run_id}", f".agent/worktrees/{run_id}", "parallel or high-risk work" if required else "single low-risk working copy")
