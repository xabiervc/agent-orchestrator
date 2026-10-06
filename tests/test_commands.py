import pytest

from agent_orchestrator.commands import build_project_command


def test_command_plan_requires_positive_timeout():
    with pytest.raises(ValueError):
        build_project_command("tests", "pytest -q", 0)


def test_command_plan_is_declarative():
    plan = build_project_command("tests", "pytest -q", 60)
    assert plan.command == "pytest -q"
    assert plan.timeout_seconds == 60
