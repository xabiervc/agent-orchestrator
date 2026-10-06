from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse
import json

HIGH_RISK_OPERATIONS = {"project_settings_write", "autoload_write", "input_actions_write", "save_data_write", "uid_write", "export_presets_write", "plugin_install"}


def validate_mcp_config(path: Path) -> list[str]:
    if not path.exists():
        return ["MCP client configuration does not exist."]
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return [f"MCP client configuration is invalid JSON: {exc}"]
    if not isinstance(data, dict):
        return ["MCP client configuration must be an object."]
    if "mcpServers" in data:
        servers = data["mcpServers"]
        if not isinstance(servers, dict) or not servers:
            return ["MCP client configuration has no mcpServers."]
        errors: list[str] = []
        for name, server in servers.items():
            if not isinstance(server, dict):
                errors.append(f"MCP server {name!r} is not an object.")
                continue
            if "command" in server:
                if not isinstance(server["command"], str) or not server["command"].strip():
                    errors.append(f"MCP server {name!r} has an invalid command.")
            elif "url" in server:
                errors.extend(f"{name}: {error}" for error in validate_local_url(server["url"]))
            else:
                errors.append(f"MCP server {name!r} needs command or URL.")
        return errors
    if "command" in data:
        return [] if isinstance(data["command"], str) and data["command"].strip() else ["MCP command is invalid."]
    if "url" in data:
        return validate_local_url(data["url"])
    return ["MCP configuration needs mcpServers, command, or URL."]


def validate_local_url(url: str) -> list[str]:
    if not isinstance(url, str):
        return ["MCP URL must be a string."]
    parsed = urlparse(url)
    if parsed.scheme not in {"ws", "wss", "http", "https"}:
        return ["MCP URL must use stdio configuration or local HTTP/WebSocket."]
    if not parsed.hostname:
        return ["MCP URL must include a hostname."]
    if parsed.hostname.lower() in {"localhost", "127.0.0.1", "::1"}:
        return []
    return ["Network MCP endpoints are disabled; use a local host."]


def validate_operation(operation: str, *, approved: bool = False) -> list[str]:
    if operation in HIGH_RISK_OPERATIONS and not approved:
        return [f"High-risk Godot operation requires explicit approval: {operation}."]
    return []
