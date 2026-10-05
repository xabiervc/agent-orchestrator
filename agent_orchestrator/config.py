from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
import json


@dataclass
class ProjectConfig:
    name: str
    kind: str = "software"
    engine: str | None = None
    stack: dict[str, Any] = field(default_factory=dict)
    targets: list[str] = field(default_factory=list)
    profiles: list[str] = field(default_factory=lambda: ["generic"])
    commands: dict[str, Any] = field(default_factory=dict)
    context_required: list[str] = field(default_factory=list)
    risks: dict[str, str] = field(default_factory=dict)
    raw: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ProjectConfig":
        project = data.get("project", {})
        context = data.get("context", {})
        return cls(
            name=project.get("name", "unnamed-project"),
            kind=project.get("kind", "software"),
            engine=project.get("engine"),
            stack=project.get("stack", {}),
            targets=project.get("targets", []),
            profiles=data.get("profiles", ["generic"]),
            commands=data.get("commands", {}),
            context_required=context.get("required", []),
            risks=data.get("risks", {}),
            raw=data,
        )


def load_project_config(root: Path) -> ProjectConfig:
    path = root / ".agent" / "project.json"
    if not path.exists():
        raise FileNotFoundError(f"Missing project configuration: {path}")
    return ProjectConfig.from_dict(json.loads(path.read_text(encoding="utf-8")))


def write_project_config(root: Path, config: dict[str, Any]) -> Path:
    directory = root / ".agent"
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "project.json"
    path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    return path
