from pathlib import Path

from plugins.godot_mcp.preflight import discover_project, run_preflight


def test_preflight_blocks_without_editor_and_probe(tmp_path: Path):
    (tmp_path / "project.godot").write_text("[application]\nconfig/name=Demo\n")
    project = discover_project(tmp_path)
    result = run_preflight(project)
    assert result.ready is False
    assert result.blocking_checks


def test_preflight_can_be_ready_with_local_config(tmp_path: Path):
    (tmp_path / "project.godot").write_text("[application]\nconfig/name=Demo\n")
    (tmp_path / ".mcp.json").write_text('{"mcpServers":{"godot":{"command":"godot-mcp"}}}')
    project = discover_project(tmp_path)
    result = run_preflight(project, editor_open=True, read_only_probe=True)
    assert result.ready is True


def test_preflight_blocks_while_game_runs(tmp_path: Path):
    (tmp_path / "project.godot").write_text("{}")
    (tmp_path / ".mcp.json").write_text('{"mcpServers":{"godot":{"command":"godot-mcp"}}}')
    project = discover_project(tmp_path)
    result = run_preflight(project, editor_open=True, game_running=True, read_only_probe=True)
    assert result.ready is False
