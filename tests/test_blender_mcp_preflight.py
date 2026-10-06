from pathlib import Path

from plugins.blender_mcp.preflight import discover_project, run_preflight


def test_preflight_blocks_without_saved_blend_and_probe(tmp_path: Path):
    project = discover_project(tmp_path)
    result = run_preflight(project)
    assert result.ready is False
    assert result.blocking_checks


def test_preflight_can_be_ready(tmp_path: Path):
    (tmp_path / "scene.blend").write_bytes(b"blend")
    (tmp_path / ".mcp.json").write_text('{"mcpServers":{"blender":{"command":"blender-mcp"}}}')
    project = discover_project(tmp_path)
    result = run_preflight(project, blender_available=True, scene_saved=True, mcp_connected=True, read_only_probe=True)
    assert result.ready is True


def test_preflight_blocks_active_render(tmp_path: Path):
    (tmp_path / "scene.blend").write_bytes(b"blend")
    (tmp_path / ".mcp.json").write_text('{"mcpServers":{"blender":{"command":"blender-mcp"}}}')
    project = discover_project(tmp_path)
    result = run_preflight(project, blender_available=True, scene_saved=True, mcp_connected=True, read_only_probe=True, render_active=True)
    assert result.ready is False
