from __future__ import annotations

from dataclasses import dataclass
import hashlib
import subprocess
from typing import Any

from .commands import ProjectCommandPlan


@dataclass(frozen=True)
class QualityResult:
    passed: bool
    gates: dict[str, bool]
    failures: list[str]
    evidence: list[dict[str, Any]] | None = None


def _sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def execute_quality_command(plan: ProjectCommandPlan) -> dict[str, Any]:
    command_hash = _sha256(plan.command)
    try:
        completed = subprocess.run(
            plan.command,
            shell=True,
            cwd=plan.working_directory,
            capture_output=True,
            text=True,
            timeout=plan.timeout_seconds,
            check=False,
        )
        stdout = completed.stdout or ""
        stderr = completed.stderr or ""
        return {
            "gate": plan.name,
            "command": plan.command,
            "command_hash": command_hash,
            "timeout_seconds": plan.timeout_seconds,
            "return_code": completed.returncode,
            "timed_out": False,
            "passed": completed.returncode == 0,
            "stdout_hash": _sha256(stdout),
            "stderr_hash": _sha256(stderr),
        }
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""
        if isinstance(stdout, bytes):
            stdout = stdout.decode("utf-8", errors="replace")
        if isinstance(stderr, bytes):
            stderr = stderr.decode("utf-8", errors="replace")
        return {
            "gate": plan.name,
            "command": plan.command,
            "command_hash": command_hash,
            "timeout_seconds": plan.timeout_seconds,
            "return_code": None,
            "timed_out": True,
            "passed": False,
            "stdout_hash": _sha256(stdout),
            "stderr_hash": _sha256(stderr),
        }


def evaluate_quality(results: dict[str, Any], required_gates: tuple[str, ...] = ("tests", "validation", "evidence")) -> QualityResult:
    gates = {gate: bool(results.get(gate, False)) for gate in required_gates}
    failures = [gate for gate, passed in gates.items() if not passed]
    evidence = results.get("_evidence")
    return QualityResult(not failures, gates, failures, evidence if isinstance(evidence, list) else None)
