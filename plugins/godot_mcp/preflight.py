from __future__ import annotations

from pathlib import Path

from .models import GodotPreflight, GodotProject
from .policy import validate_mcp_config


def discover_project(root: Path) -> GodotProject:
    projects = sorted(root.glob("project.godot"))
    if not projects:
        raise FileNotFoundError(f"No project.godot file found in {root}")
    config_candidates = [root / ".mcp.json", root / ".godot-mcp.json"]
    config = next((path for path in config_candidates if path.exists()), None)
    return GodotProject(root=root, project_file=projects[0], mcp_config=config)


def run_preflight(project: GodotProject, *, editor_open: bool = False, game_running: bool = False, importing: bool = False, read_only_probe: bool = False) -> GodotPreflight:
    checks: list[dict[str, str]] = []
    checks.append({"name": "project_file_exists", "status": "passed" if project.project_file.exists() else "blocked"})
    checks.append({"name": "editor_open", "status": "passed" if editor_open else "blocked"})
    checks.append({"name": "game_inactive", "status": "blocked" if game_running else "passed"})
    checks.append({"name": "import_inactive", "status": "blocked" if importing else "passed"})
    if project.mcp_config is None:
        checks.append({"name": "mcp_config_exists", "status": "blocked"})
    else:
        errors = validate_mcp_config(project.mcp_config)
        checks.append({"name": "mcp_config_valid", "status": "passed" if not errors else "blocked", "details": "; ".join(errors)})
    checks.append({"name": "read_only_probe", "status": "passed" if read_only_probe else "required"})
    ready = not any(check["status"] == "blocked" for check in checks) and read_only_probe
    return GodotPreflight(ready=ready, checks=checks)
