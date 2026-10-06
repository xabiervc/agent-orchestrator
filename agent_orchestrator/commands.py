from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


_MAX_TIMEOUT_SECONDS = 3600
_UNSAFE_SHELL_PATTERNS = ("&&", "||", ";", "|", ">", "<", "`", "$(',")


@dataclass(frozen=True)
class ProjectCommandPlan:
    name: str
    command: str
    timeout_seconds: int
    working_directory: str = "."


def build_project_command(name: str, command: str, timeout_seconds: int = 300, working_directory: str = ".") -> ProjectCommandPlan:
    if not name.strip() or not command.strip():
        raise ValueError("Command name and command are required.")
    if timeout_seconds <= 0 or timeout_seconds > _MAX_TIMEOUT_SECONDS:
        raise ValueError(f"Command timeout must be between 1 and {_MAX_TIMEOUT_SECONDS} seconds.")
    if not working_directory.strip():
        raise ValueError("Working directory is required.")
    if any(pattern in command for pattern in _UNSAFE_SHELL_PATTERNS):
        raise ValueError("Command contains unsupported shell control syntax.")
    return ProjectCommandPlan(name.strip(), command.strip(), timeout_seconds, str(Path(working_directory)))
