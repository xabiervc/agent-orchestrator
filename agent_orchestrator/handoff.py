from __future__ import annotations

from pathlib import Path
from typing import Any

from .artifacts import read_json, write_json


def create_handoff(run: Path, provider: str, model: str, allowed_files: list[str], verification_commands: list[str]) -> dict[str, Any]:
    consensus = read_json(run / "consensus.json")
    if consensus.get("decision") != "approve":
        raise ValueError("Handoff requires approved consensus.")
    if consensus.get("run_id") != run.name:
        raise ValueError("Consensus run_id does not match the run directory.")
    data = {"schema_version": 1, "type": "handoff", "run_id": run.name, "provider": provider, "model": model, "allowed_files": allowed_files, "verification_commands": verification_commands, "scope_locked": True}
    write_json(run / "handoff.json", data)
    return data
