from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .command_runner import execute_command
from .commands import ProjectCommandPlan, build_project_command


@dataclass(frozen=True)
class QualityResult:
    passed: bool
    gates: dict[str, bool]
    failures: list[str]
    evidence: list[dict[str, Any]] | None = None

    def as_dict(self) -> dict[str, Any]:
        return {"passed": self.passed, "gates": self.gates, "failures": self.failures, "evidence": self.evidence}


@dataclass(frozen=True)
class QualityGate:
    name: str
    command: str
    timeout_seconds: int = 300
    working_directory: str = "."
    passed: bool = False
    details: str = ""


@dataclass(frozen=True)
class QualityGateReport:
    passed: bool
    gates: list[QualityGate]


def _quality_evidence(plan: ProjectCommandPlan, project_root: Path | None = None) -> dict[str, Any]:
    result = execute_command(plan, project_root=project_root)
    result["command"] = plan.command
    result["timeout_seconds"] = plan.timeout_seconds
    return result


def _report_from_result(result: dict[str, Any]) -> QualityGateReport:
    details = str(result)
    gate = QualityGate(name=result["gate"], command=result.get("command", ""), timeout_seconds=int(result.get("timeout_seconds", 300)), passed=bool(result.get("passed")), details=details)
    return QualityGateReport(gate.passed, [gate])


def run_quality_command(name: str, command: str, timeout_seconds: int = 300, *, project_root: Path | None = None) -> QualityGateReport:
    plan = build_project_command(name, command, timeout_seconds)
    return _report_from_result(_quality_evidence(plan, project_root))


def execute_quality_command(plan_or_name: ProjectCommandPlan | str, command: str | None = None, *, timeout_seconds: int = 300, project_root: Path | None = None) -> QualityGateReport | dict[str, Any]:
    if isinstance(plan_or_name, ProjectCommandPlan):
        return _quality_evidence(plan_or_name, project_root)
    if command is None:
        raise TypeError("command is required when the first argument is a gate name")
    return run_quality_command(plan_or_name, command, timeout_seconds, project_root=project_root)


def evaluate_quality(results: dict[str, Any], required_gates: tuple[str, ...] = ("tests", "validation", "evidence")) -> QualityResult:
    gates = {gate: bool(results.get(gate, False)) for gate in required_gates}
    failures = [gate for gate, passed in gates.items() if not passed]
    evidence = results.get("_evidence")
    return QualityResult(not failures, gates, failures, evidence if isinstance(evidence, list) else None)


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
