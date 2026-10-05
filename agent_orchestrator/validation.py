from __future__ import annotations

from pathlib import Path
from .artifacts import read_json, list_artifacts


def validate_run(run: Path) -> list[str]:
    errors: list[str] = []
    for filename in ("task.json", "consensus.json"):
        path = run / filename
        if not path.exists():
            errors.append(f"Missing {filename}.")
            continue
        try:
            read_json(path)
        except ValueError as exc:
            errors.append(f"Invalid JSON in {filename}: {exc}.")
    consensus_path = run / "consensus.json"
    if consensus_path.exists():
        consensus = read_json(consensus_path)
        if consensus.get("decision") == "approve":
            if not list_artifacts(run / "proposals"):
                errors.append("Approved consensus requires proposal artifacts.")
            if not list_artifacts(run / "reviews"):
                errors.append("Approved consensus requires review artifacts.")
    return errors
