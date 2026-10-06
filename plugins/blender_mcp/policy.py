from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse
import json

HIGH_RISK_OPERATIONS = {"python_execute", "run_external_command", "delete_object", "overwrite_blend", "overwrite_asset", "apply_destructive_modifier", "change_scene_settings", "change_render_settings", "export_asset"}


def validate_mcp_config(path: Path) -> list[str]:
    if not path.exists():
        return ["MCP configuration does not exist."]
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return [f"MCP configuration is invalid JSON: {exc}"]
    if not isinstance(data, dict):
        return ["MCP configuration must be an object."]
    if "mcpServers" in data:
        servers = data["mcpServers"]
        if not isinstance(servers, dict) or not servers:
            return ["MCP configuration has no mcpServers."]
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
    return ["MCP configuration needs mcpServers."]


def validate_local_url(url: str) -> list[str]:
    if not isinstance(url, str):
        return ["MCP URL must be a string."]
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https", "ws", "wss"}:
        return ["MCP URL must use a supported local transport."]
    if not parsed.hostname:
        return ["MCP URL must include a hostname."]
    if parsed.hostname.lower() in {"localhost", "127.0.0.1", "::1"}:
        return []
    return ["Remote MCP endpoints are disabled by default."]


def validate_operation(operation: str, *, approved: bool = False) -> list[str]:
    if operation in HIGH_RISK_OPERATIONS and not approved:
        return [f"High-risk Blender operation requires explicit approval: {operation}."]
    return []
