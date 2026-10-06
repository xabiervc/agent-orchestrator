from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping


def write_project_config(root: Path, config: Mapping[str, Any]) -> Path:
    path = root / ".agent" / "project.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(dict(config), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def latest_run(root: Path) -> Path | None:
    runs = root / ".agent" / "runs"
    if not runs.exists():
        return None
    candidates = sorted((path for path in runs.iterdir() if path.is_dir()), reverse=True)
    return candidates[0] if candidates else None


def append_evidence_entries(run: Path, entries: list[Mapping[str, Any]]) -> Path:
    """Append evidence entries to a run manifest without changing its shape."""
    manifest = run / "evidence" / "manifest.json"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    if manifest.exists():
        payload = json.loads(manifest.read_text(encoding="utf-8"))
    else:
        payload = {"entries": []}
    if isinstance(payload, list):
        payload = {"entries": payload}
    if not isinstance(payload, dict):
        raise ValueError("Evidence manifest must be a JSON object or list.")
    existing = payload.setdefault("entries", [])
    if not isinstance(existing, list):
        raise ValueError("Evidence manifest entries must be a list.")
    existing.extend(dict(entry) for entry in entries)
    manifest.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest
