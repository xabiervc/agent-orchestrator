import pytest

from agent_orchestrator.commands import build_project_command


def test_command_rejects_shell_control_syntax():
    with pytest.raises(ValueError):
        build_project_command("tests", "pytest -q && echo bypass")


def test_command_rejects_invalid_timeout():
    with pytest.raises(ValueError):
        build_project_command("tests", "pytest -q", timeout_seconds=0)
    with pytest.raises(ValueError):
        build_project_command("tests", "pytest -q", timeout_seconds=3601)


def test_command_requires_working_directory():
    with pytest.raises(ValueError):
        build_project_command("tests", "pytest -q", working_directory=" ")
