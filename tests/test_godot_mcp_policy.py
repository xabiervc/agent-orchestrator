import json
from pathlib import Path

from plugins.godot_mcp.policy import validate_mcp_config, validate_local_url, validate_operation


def test_accepts_stdio_config(tmp_path: Path):
    path = tmp_path / ".mcp.json"
    path.write_text(json.dumps({"mcpServers": {"godot": {"command": "godot-mcp"}}}))
    assert validate_mcp_config(path) == []


def test_accepts_local_websocket_config(tmp_path: Path):
    path = tmp_path / ".mcp.json"
    path.write_text(json.dumps({"mcpServers": {"godot": {"url": "ws://127.0.0.1:6505"}}}))
    assert validate_mcp_config(path) == []


def test_rejects_network_endpoint():
    assert validate_local_url("https://example.com/mcp")


def test_high_risk_operation_requires_approval():
    assert validate_operation("save_data_write")
    assert validate_operation("save_data_write", approved=True) == []
