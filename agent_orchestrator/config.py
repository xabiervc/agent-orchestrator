from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class AppConfig:
    project_root: Path
    config_path: Path
    environment: str = "development"
    command_timeout_seconds: int = 300
    required_checks: tuple[str, ...] = ()
    protected_paths: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ProjectConfig:
    project_name: str
    project_root: Path
    config_path: Path
    profiles: tuple[str, ...] = ()
    environment: str = "development"
    command_timeout_seconds: int = 300
    required_checks: tuple[str, ...] = ()
    protected_paths: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)


def _config_path(project_root: Path) -> Path:
    return project_root / "project.json"


def load_config(path: Path) -> AppConfig:
    data = json.loads(path.read_text(encoding="utf-8"))
    return AppConfig(
        project_root=Path(data["project_root"]),
        config_path=path,
        environment=data.get("environment", "development"),
        command_timeout_seconds=int(data.get("command_timeout_seconds", 300)),
        required_checks=tuple(data.get("required_checks", ())),
        protected_paths=tuple(data.get("protected_paths", ())),
        metadata=dict(data.get("metadata", {})),
    )


def load_project_config(project_root: Path) -> ProjectConfig:
    root = Path(project_root)
    path = _config_path(root)
    data = json.loads(path.read_text(encoding="utf-8"))
    project = dict(data.get("project", {}))
    return ProjectConfig(
        project_name=str(project.get("name", root.name)),
        project_root=root,
        config_path=path,
        profiles=tuple(data.get("profiles", ())),
        environment=data.get("environment", "development"),
        command_timeout_seconds=int(data.get("command_timeout_seconds", 300)),
        required_checks=tuple(data.get("required_checks", ())),
        protected_paths=tuple(data.get("protected_paths", ())),
        metadata=dict(data.get("metadata", {})),
    )


def write_project_config(project_root: Path, data: dict[str, Any]) -> None:
    root = Path(project_root)
    root.mkdir(parents=True, exist_ok=True)
    _config_path(root).write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
