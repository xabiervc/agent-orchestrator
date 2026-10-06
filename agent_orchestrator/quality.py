from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class QualityResult:
    passed: bool
    gates: dict[str, bool]
    failures: list[str]


def evaluate_quality(results: dict[str, Any], required_gates: tuple[str, ...] = ("tests", "validation", "evidence")) -> QualityResult:
    gates = {gate: bool(results.get(gate, False)) for gate in required_gates}
    failures = [gate for gate, passed in gates.items() if not passed]
    return QualityResult(not failures, gates, failures)
