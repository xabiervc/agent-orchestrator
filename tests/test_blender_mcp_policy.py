import json
from pathlib import Path

from plugins.blender_mcp.policy import validate_mcp_config, validate_local_url, validate_operation


def test_accepts_stdio_config(tmp_path: Path):
    path = tmp_path / ".mcp.json"
    path.write_text(json.dumps({"mcpServers": {"blender": {"command": "blender-mcp"}}}))
    assert validate_mcp_config(path) == []


def test_accepts_local_websocket_config(tmp_path: Path):
    path = tmp_path / ".mcp.json"
    path.write_text(json.dumps({"mcpServers": {"blender": {"url": "ws://127.0.0.1:9876"}}}))
    assert validate_mcp_config(path) == []


def test_rejects_remote_endpoint():
    assert validate_local_url("https://example.com/mcp")


def test_python_execution_requires_approval():
    assert validate_operation("python_execute")
    assert validate_operation("python_execute", approved=True) == []
