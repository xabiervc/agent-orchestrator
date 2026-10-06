from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from .command_runner import execute_command
from .commands import build_project_command


@dataclass(frozen=True)
class QualityGate:
    name: str
    passed: bool
    required: bool = True
    details: str = ""


@dataclass(frozen=True)
class QualityReport:
    gates: tuple[QualityGate, ...]

    @property
    def passed(self) -> bool:
        return all(gate.passed for gate in self.gates if gate.required)

    def as_dict(self) -> dict[str, Any]:
        return {"passed": self.passed, "gates": [{"name": gate.name, "passed": gate.passed, "required": gate.required, "details": gate.details} for gate in self.gates]}


@dataclass(frozen=True)
class QualityResult:
    passed: bool
    failures: list[str]
    gates: tuple[QualityGate, ...] = ()

    @property
    def failed(self) -> bool:
        return not self.passed

    def as_dict(self) -> dict[str, Any]:
        return {"passed": self.passed, "failures": self.failures, "gates": [{"name": gate.name, "passed": gate.passed, "required": gate.required, "details": gate.details} for gate in self.gates]}


def evaluate_quality(results: Mapping[str, bool]) -> QualityResult:
    failures = [name for name, passed in results.items() if not passed]
    return QualityResult(not failures, failures, tuple(QualityGate(name, passed) for name, passed in results.items()))


def run_quality_command(name: str, command: str, *, timeout_seconds: int = 300, working_directory: str = ".", project_root: Path | None = None) -> QualityReport:
    plan = build_project_command(name, command, timeout_seconds, working_directory)
    execution = execute_command(plan, project_root=project_root)
    details = {"command_hash": execution["command_hash"], "return_code": execution["return_code"], "timed_out": execution["timed_out"], "working_directory": execution["working_directory"], "stdout_hash": execution["stdout_hash"], "stderr_hash": execution["stderr_hash"]}
    return QualityReport((QualityGate(name, execution["passed"], True, str(details)),))


def execute_quality_command(name: str, command: str, *, timeout_seconds: int = 300, working_directory: str = ".", project_root: Path | None = None) -> QualityReport:
    return run_quality_command(name, command, timeout_seconds=timeout_seconds, working_directory=working_directory, project_root=project_root)
