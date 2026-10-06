import pytest

from agent_orchestrator.commands import build_project_command


def test_command_rejects_shell_control_syntax():
    for command in ("pytest -q && echo bypass", "pytest -q; echo bypass", "pytest -q | tee output"):
        with pytest.raises(ValueError):
            build_project_command("tests", command)


def test_command_allows_quoted_argument_syntax():
    plan = build_project_command("tests", 'python -c "import time; time.sleep(1)"')
    assert plan.command.endswith('time.sleep(1)"')


def test_command_rejects_invalid_timeout():
    with pytest.raises(ValueError):
        build_project_command("tests", "pytest -q", timeout_seconds=0)
    with pytest.raises(ValueError):
        build_project_command("tests", "pytest -q", timeout_seconds=3601)


def test_command_requires_working_directory():
    with pytest.raises(ValueError):
        build_project_command("tests", "pytest -q", working_directory=" ")
