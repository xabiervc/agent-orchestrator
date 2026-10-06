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


@dataclass(frozen=True, init=False)
class ProjectConfig:
    project_name: str
    project_root: Path
    config_path: Path | None
    profiles: tuple[str, ...]
    environment: str
    command_timeout_seconds: int
    required_checks: tuple[str, ...]
    protected_paths: tuple[str, ...]
    metadata: dict[str, Any]
    raw: dict[str, Any]

    def __init__(self, project_name: str, project_root: Path | None = None, config_path: Path | None = None, profiles: tuple[str, ...] = (), environment: str = "development", command_timeout_seconds: int = 300, required_checks: tuple[str, ...] = (), protected_paths: tuple[str, ...] = (), metadata: dict[str, Any] | None = None, raw: dict[str, Any] | None = None) -> None:
        payload = dict(raw or {})
        project = dict(payload.get("project", {}))
        resolved_name = str(project.get("name", project_name))
        resolved_root = Path(project_root or payload.get("project_root", "."))
        self.project_name = resolved_name
        self.project_root = resolved_root
        self.config_path = config_path
        self.profiles = tuple(profiles or payload.get("profiles", ()))
        self.environment = environment
        self.command_timeout_seconds = command_timeout_seconds
        self.required_checks = tuple(required_checks)
        self.protected_paths = tuple(protected_paths)
        self.metadata = dict(metadata or {})
        self.raw = payload


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
        raw=data,
    )


def write_project_config(config_or_root: ProjectConfig | Path, data_or_path: dict[str, Any] | Path | None = None) -> None:
    if isinstance(config_or_root, ProjectConfig):
        config = config_or_root
        target = Path(data_or_path) if isinstance(data_or_path, Path) else config.config_path
        if target is None:
            raise ValueError("A configuration path is required.")
        data: dict[str, Any] = dict(config.raw)
        data.setdefault("project", {"name": config.project_name})
        data.setdefault("profiles", list(config.profiles))
        data.setdefault("project_root", str(config.project_root))
    else:
        root = Path(config_or_root)
        target = _config_path(root)
        data = dict(data_or_path or {})
        root.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
