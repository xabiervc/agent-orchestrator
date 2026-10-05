from __future__ import annotations

from pathlib import Path
from typing import Any
import json


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def list_artifacts(directory: Path) -> list[Path]:
    return sorted(directory.glob("*.json")) if directory.exists() else []
