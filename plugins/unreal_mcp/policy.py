from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse
import ipaddress
import json
import socket


def validate_mcp_config(path: Path) -> list[str]:
    if not path.exists():
        return ["MCP client configuration does not exist."]
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return [f"MCP client configuration is invalid JSON: {exc}"]
    servers = data.get("mcpServers")
    if not isinstance(servers, dict) or not servers:
        return ["MCP client configuration has no mcpServers."]
    errors: list[str] = []
    for name, server in servers.items():
        if not isinstance(server, dict):
            errors.append(f"MCP server {name!r} is not an object.")
            continue
        url = server.get("url")
        if not isinstance(url, str):
            errors.append(f"MCP server {name!r} has no URL.")
            continue
        errors.extend(f"{name}: {error}" for error in validate_local_mcp_url(url))
    return errors


def validate_local_mcp_url(url: str) -> list[str]:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        return ["MCP URL must use HTTP(S)."]
    if not parsed.hostname:
        return ["MCP URL must include a hostname."]
    host = parsed.hostname.lower()
    if host == "localhost" or host.endswith(".localhost"):
        return []
    try:
        addresses = socket.getaddrinfo(host, None)
    except OSError:
        return ["MCP hostname could not be resolved as a local address."]
    for address in addresses:
        ip = ipaddress.ip_address(address[4][0])
        if not (ip.is_loopback or ip.is_private):
            return ["MCP server must resolve to a local address."]
    return []
