from __future__ import annotations

from pathlib import Path
import json


def validate_run(run: Path) -> list[str]:
    errors: list[str] = []
    for filename in ("task.json", "consensus.json"):
        path = run / filename
        if not path.exists():
            errors.append(f"Missing {filename}.")
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid JSON in {filename}: {exc}.")
    consensus = run / "consensus.json"
    if consensus.exists():
        data = json.loads(consensus.read_text(encoding="utf-8"))
        if data.get("decision") == "approve" and not list((run / "proposals").glob("*.json")):
            errors.append("Approved consensus cannot exist without proposals.")
    return errors
