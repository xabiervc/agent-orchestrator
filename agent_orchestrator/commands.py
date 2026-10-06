from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProjectCommandPlan:
    name: str
    command: str
    timeout_seconds: int
    working_directory: str = "."


def build_project_command(name: str, command: str, timeout_seconds: int = 300, working_directory: str = ".") -> ProjectCommandPlan:
    if not name.strip() or not command.strip():
        raise ValueError("Command name and command are required.")
    if timeout_seconds <= 0:
        raise ValueError("Command timeout must be positive.")
    return ProjectCommandPlan(name, command, timeout_seconds, working_directory)
