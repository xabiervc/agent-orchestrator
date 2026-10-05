from agent_orchestrator.models import Route
from agent_orchestrator.providers import build_command, detect_provider


def test_command_plan_never_contains_credentials():
    plan = build_command(Route("planning", "claude-code", "sonnet"), "prompt.md")
    assert plan.command[:2] == ["claude", "--model"]
    assert plan.environment == {}
    assert all("token" not in value.lower() for value in plan.command)


def test_missing_provider_is_reported_without_execution():
    status = detect_provider("provider-that-does-not-exist")
    assert status.available is False
