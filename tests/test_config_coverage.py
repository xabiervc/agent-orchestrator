from pathlib import Path

import pytest

from agent_orchestrator.config import load_project_config, write_project_config


def test_project_config_round_trip(tmp_path: Path) -> None:
    path = write_project_config(tmp_path, {"project": {"name": "demo"}, "profiles": ["generic"]})
    config = load_project_config(tmp_path)
    assert path == tmp_path / ".agent" / "project.json"
    assert config.name == "demo"
    assert config.profiles == ["generic"]


def test_missing_project_config_raises(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_project_config(tmp_path)
