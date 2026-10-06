from __future__ import annotations

from pathlib import Path

from .models import UnrealPreflight, UnrealProject
from .policy import validate_mcp_config


def discover_project(root: Path) -> UnrealProject:
    projects = sorted(root.glob("*.uproject"))
    if not projects:
        raise FileNotFoundError(f"No .uproject file found in {root}")
    if len(projects) > 1:
        raise ValueError(f"Multiple .uproject files found in {root}")
    project_file = projects[0]
    config = project_file.with_name(".mcp.json")
    return UnrealProject(root=root, project_file=project_file, mcp_config=config if config.exists() else None)


def run_preflight(project: UnrealProject, *, editor_open: bool = False, play_active: bool = False, compiling: bool = False, read_only_probe: bool = False) -> UnrealPreflight:
    checks: list[dict[str, str]] = []
    checks.append({"name": "uproject_exists", "status": "passed" if project.project_file.exists() else "blocked"})
    checks.append({"name": "editor_open", "status": "passed" if editor_open else "blocked"})
    checks.append({"name": "play_inactive", "status": "blocked" if play_active else "passed"})
    checks.append({"name": "compile_inactive", "status": "blocked" if compiling else "passed"})
    if project.mcp_config is None:
        checks.append({"name": "mcp_config_exists", "status": "blocked"})
    else:
        errors = validate_mcp_config(project.mcp_config)
        checks.append({"name": "mcp_config_valid", "status": "passed" if not errors else "blocked", "details": "; ".join(errors)})
    checks.append({"name": "read_only_probe", "status": "passed" if read_only_probe else "required"})
    return UnrealPreflight(ready=not any(check["status"] == "blocked" for check in checks) and read_only_probe, checks=checks)
