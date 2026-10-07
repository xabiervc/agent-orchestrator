from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .command_runner import execute_command
from .commands import ProjectCommandPlan, build_project_command


@dataclass(frozen=True)
class QualityGate:
    name: str
    command: str
    timeout_seconds: int = 300
    working_directory: str = "."


def build_quality_gate(name: str, command: str, timeout_seconds: int = 300, working_directory: str = ".") -> QualityGate:
    plan = build_project_command(name, command, timeout_seconds, working_directory)
    return QualityGate(plan.name, plan.command, plan.timeout_seconds, plan.working_directory)


def run_quality_gate(gate: QualityGate, *, project_root: Path | None = None) -> dict[str, Any]:
    plan = ProjectCommandPlan(gate.name, gate.command, gate.timeout_seconds, gate.working_directory)
    return execute_command(plan, project_root=project_root)


def summarize_quality(results: list[Mapping[str, Any]]) -> dict[str, Any]:
    passed = [result for result in results if result.get("passed") is True]
    failed = [result for result in results if result.get("passed") is False]
    return {"passed": not failed and bool(results), "total": len(results), "passed_count": len(passed), "failed_count": len(failed)}
