from pathlib import Path

from agent_orchestrator.models import Route
from agent_orchestrator.prompts import render_prompt, write_prompt


def test_prompt_contains_run_contract(tmp_path: Path):
    route = Route("planning", "claude-code", "sonnet")
    text = render_prompt("run-1", "planning", route, ".agent/runs/run-1/task.json", ["AGENTS.md"])
    assert "run-1" in text
    assert "AGENTS.md" in text
    assert "Do not expand the task scope" in text
    path = write_prompt(tmp_path / "prompt.md", "run-1", "planning", route, "task.json", [])
    assert path.exists()
