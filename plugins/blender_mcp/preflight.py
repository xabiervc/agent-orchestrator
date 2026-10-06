from __future__ import annotations

from pathlib import Path

from .models import BlenderPreflight, BlenderProject
from .policy import validate_mcp_config


def discover_project(root: Path) -> BlenderProject:
    blend_files = sorted(root.glob("*.blend"))
    blend_file = blend_files[0] if len(blend_files) == 1 else None
    config_candidates = [root / ".mcp.json", root / ".blender-mcp.json"]
    config = next((path for path in config_candidates if path.exists()), None)
    return BlenderProject(root=root, blend_file=blend_file, mcp_config=config)


def run_preflight(project: BlenderProject, *, blender_available: bool = False, scene_saved: bool = False, mcp_connected: bool = False, read_only_probe: bool = False, render_active: bool = False) -> BlenderPreflight:
    checks: list[dict[str, str]] = []
    checks.append({"name": "blender_available", "status": "passed" if blender_available else "blocked"})
    checks.append({"name": "blend_file_discovered", "status": "passed" if project.blend_file else "blocked"})
    checks.append({"name": "scene_saved", "status": "passed" if scene_saved else "blocked"})
    checks.append({"name": "render_inactive", "status": "blocked" if render_active else "passed"})
    checks.append({"name": "mcp_connected", "status": "passed" if mcp_connected else "blocked"})
    if project.mcp_config is None:
        checks.append({"name": "mcp_config_exists", "status": "blocked"})
    else:
        errors = validate_mcp_config(project.mcp_config)
        checks.append({"name": "mcp_config_valid", "status": "passed" if not errors else "blocked", "details": "; ".join(errors)})
    checks.append({"name": "read_only_probe", "status": "passed" if read_only_probe else "required"})
    ready = not any(check["status"] == "blocked" for check in checks) and read_only_probe
    return BlenderPreflight(ready=ready, checks=checks)
