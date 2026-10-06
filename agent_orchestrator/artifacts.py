from __future__ import annotations

import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any


def write_json(path: Path, payload: Any) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return target


def read_json(path: Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def list_artifacts(root: Path) -> list[Path]:
    base = Path(root)
    if not base.exists():
        return []
    return sorted((path for path in base.rglob("*") if path.is_file()), key=lambda path: path.as_posix())


def write_project_config(root: Path, config: Mapping[str, Any]) -> Path:
    return write_json(root / ".agent" / "project.json", dict(config))


def latest_run(root: Path) -> Path | None:
    runs = root / ".agent" / "runs"
    if not runs.exists():
        return None
    candidates = sorted((path for path in runs.iterdir() if path.is_dir()), reverse=True)
    return candidates[0] if candidates else None


def append_evidence_entries(run: Path, entries: list[Mapping[str, Any]]) -> Path:
    manifest = run / "evidence" / "manifest.json"
    payload = read_json(manifest) if manifest.exists() else {"entries": []}
    if isinstance(payload, list):
        payload = {"entries": payload}
    if not isinstance(payload, dict):
        raise TypeError("Evidence manifest must be a JSON object or list.")
    existing = payload.setdefault("entries", [])
    if not isinstance(existing, list):
        raise TypeError("Evidence manifest entries must be a list.")
    existing.extend(dict(entry) for entry in entries)
    return write_json(manifest, payload)
