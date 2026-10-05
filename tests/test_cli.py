from agent_orchestrator.cli import main


def test_route_command(capsys):
    assert main(["route", "--risk", "mechanical", "--role", "planning"]) == 0
    output = capsys.readouterr().out
    assert '"model": "haiku"' in output


def test_provider_command(capsys):
    assert main(["provider", "codex"]) == 0
    assert "codex" in capsys.readouterr().out
