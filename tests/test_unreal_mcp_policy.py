import json
from pathlib import Path

from plugins.unreal_mcp.policy import validate_mcp_config, validate_local_mcp_url


def test_accepts_local_mcp_config(tmp_path: Path):
    config = tmp_path / ".mcp.json"
    config.write_text(json.dumps({"mcpServers": {"unreal-mcp": {"type": "http", "url": "http://127.0.0.1:8000/mcp"}}}))
    assert validate_mcp_config(config) == []


def test_rejects_non_local_mcp_config(tmp_path: Path):
    config = tmp_path / ".mcp.json"
    config.write_text(json.dumps({"mcpServers": {"unreal-mcp": {"url": "https://example.com/mcp"}}}))
    assert validate_mcp_config(config)


def test_rejects_non_http_url():
    assert validate_local_mcp_url("file:///tmp/mcp")
