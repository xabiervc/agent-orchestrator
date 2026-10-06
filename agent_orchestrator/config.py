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
    environment: str = "development"
    command_timeout_seconds: int = 300
    required_checks: tuple[str, ...] = ()
    protected_paths: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)


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


def load_project_config(path: Path) -> ProjectConfig:
    data = json.loads(path.read_text(encoding="utf-8"))
    return ProjectConfig(
        project_name=str(data["project_name"]),
        project_root=Path(data["project_root"]),
        config_path=path,
        environment=data.get("environment", "development"),
        command_timeout_seconds=int(data.get("command_timeout_seconds", 300)),
        required_checks=tuple(data.get("required_checks", ())),
        protected_paths=tuple(data.get("protected_paths", ())),
        metadata=dict(data.get("metadata", {})),
    )


def write_project_config(config: ProjectConfig, path: Path | None = None) -> None:
    target = path or config.config_path
    data = {
        "project_name": config.project_name,
        "project_root": str(config.project_root),
        "environment": config.environment,
        "command_timeout_seconds": config.command_timeout_seconds,
        "required_checks": list(config.required_checks),
        "protected_paths": list(config.protected_paths),
        "metadata": config.metadata,
    }
    target.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
