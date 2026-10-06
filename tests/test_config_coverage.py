from __future__ import annotations

import json
from pathlib import Path

from agent_orchestrator.config import ProjectConfig, load_project_config, write_project_config


def test_project_config_round_trip(tmp_path: Path) -> None:
    path = tmp_path / "project.json"
    config = ProjectConfig(
        project_name="demo",
        project_root=tmp_path,
        config_path=path,
        environment="test",
        command_timeout_seconds=42,
        required_checks=("ruff", "mypy"),
        protected_paths=("src",),
        metadata={"owner": "qa"},
    )

    write_project_config(config)
    loaded = load_project_config(path)

    assert loaded == config
    assert json.loads(path.read_text(encoding="utf-8"))["project_name"] == "demo"


def test_project_config_can_write_to_explicit_path(tmp_path: Path) -> None:
    source = tmp_path / "source.json"
    target = tmp_path / "target.json"
    config = ProjectConfig("demo", tmp_path, source)

    write_project_config(config, target)

    assert load_project_config(target).project_name == "demo"
