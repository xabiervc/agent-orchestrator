import sys
from pathlib import Path

import pytest

from agent_orchestrator.command_runner import execute_command
from agent_orchestrator.commands import build_project_command


def test_runner_executes_quoted_arguments_without_shell(tmp_path: Path):
    plan = build_project_command("tests", f'{sys.executable} -c "print(\'ok\')"')
    result = execute_command(plan, project_root=tmp_path)
    assert result["passed"] is True
    assert result["return_code"] == 0


def test_runner_rejects_shell_operators(tmp_path: Path):
    with pytest.raises(ValueError):
        build_project_command("tests", "echo ok && echo bypass")


def test_runner_rejects_path_traversal(tmp_path: Path):
    plan = build_project_command("tests", f'{sys.executable} -c "print(\'ok\')"', working_directory="..")
    with pytest.raises(ValueError):
        execute_command(plan, project_root=tmp_path)


def test_runner_rejects_malformed_quoting(tmp_path: Path):
    plan = build_project_command("tests", "echo 'unterminated")
    with pytest.raises(ValueError, match="malformed quoting"):
        execute_command(plan, project_root=tmp_path)
