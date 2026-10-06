import json

import pytest

from agent_orchestrator.cli import main
from agent_orchestrator.routing import route_dict, route_for


@pytest.mark.parametrize("role", ["exploration", "planning", "review", "implementation"])
@pytest.mark.parametrize("risk", ["mechanical", "low", "normal", "high", "critical"])
def test_cli_route_uses_routing_api(role, risk, monkeypatch, capsys):
    monkeypatch.chdir("/")
    assert main(["route", "--role", role, "--risk", risk]) == 0
    cli_result = json.loads(capsys.readouterr().out)
    expected = {"role": role, "risk": risk, **route_dict(route_for(role, risk=risk))}
    assert cli_result == expected
