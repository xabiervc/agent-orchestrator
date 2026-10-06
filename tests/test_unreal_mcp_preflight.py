from pathlib import Path

from plugins.unreal_mcp.preflight import discover_project, run_preflight


def test_preflight_blocks_without_editor_and_probe(tmp_path: Path):
    (tmp_path / "Demo.uproject").write_text("{}")
    project = discover_project(tmp_path)
    result = run_preflight(project)
    assert result.ready is False
    assert result.blocking_checks


def test_preflight_requires_read_only_probe(tmp_path: Path):
    (tmp_path / "Demo.uproject").write_text("{}")
    (tmp_path / ".mcp.json").write_text('{"mcpServers":{"unreal":{"url":"http://127.0.0.1:8000/mcp"}}}')
    project = discover_project(tmp_path)
    result = run_preflight(project, editor_open=True, read_only_probe=False)
    assert result.ready is False
    assert any(check["status"] == "required" for check in result.checks)


def test_preflight_can_be_ready(tmp_path: Path):
    (tmp_path / "Demo.uproject").write_text("{}")
    (tmp_path / ".mcp.json").write_text('{"mcpServers":{"unreal":{"url":"http://127.0.0.1:8000/mcp"}}}')
    project = discover_project(tmp_path)
    result = run_preflight(project, editor_open=True, read_only_probe=True)
    assert result.ready is True
