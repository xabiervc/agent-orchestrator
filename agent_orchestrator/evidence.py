from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .artifacts import read_json, write_json


def create_evidence_manifest(run: Path, entries: list[dict[str, Any]]) -> dict[str, Any]:
    manifest = {"schema_version": 1, "type": "evidence_manifest", "run_id": run.name, "created_at": datetime.now(timezone.utc).isoformat(), "entries": entries}
    write_json(run / "evidence" / "manifest.json", manifest)
    return manifest


def append_evidence_entries(run: Path, entries: list[dict[str, Any]]) -> dict[str, Any]:
    manifest_path = run / "evidence" / "manifest.json"
    if manifest_path.exists():
        manifest = read_json(manifest_path)
        if not isinstance(manifest.get("entries"), list):
            manifest["entries"] = []
    else:
        manifest = {"schema_version": 1, "type": "evidence_manifest", "run_id": run.name, "created_at": datetime.now(timezone.utc).isoformat(), "entries": []}
    manifest["entries"].extend(entries)
    write_json(manifest_path, manifest)
    return manifest


def load_evidence_manifest(run: Path) -> dict[str, Any]:
    return read_json(run / "evidence" / "manifest.json")


def validate_evidence_manifest(manifest: dict[str, Any], run_id: str) -> list[str]:
    errors: list[str] = []
    if manifest.get("type") != "evidence_manifest":
        errors.append("Invalid evidence manifest type.")
    if manifest.get("run_id") != run_id:
        errors.append("Evidence manifest run_id does not match.")
    if not isinstance(manifest.get("entries"), list) or not manifest["entries"]:
        errors.append("Evidence manifest must contain entries.")
    return errors
