import pytest

from agent_orchestrator.models import Route
from agent_orchestrator.providers import build_command


def test_provider_commands_are_credential_free():
    plan = build_command(Route("planning", "codex", "default"), "prompt.md")
    assert not any(argument.startswith("--api-key") for argument in plan.command)
    assert plan.environment == {}


def test_unknown_provider_remains_a_non_executing_plan():
    plan = build_command(Route("planning", "unknown-provider", "default"), "prompt.md")
    assert plan.command[0] == "unknown-provider"
