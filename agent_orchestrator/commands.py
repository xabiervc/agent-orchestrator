from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

_MAX_TIMEOUT_SECONDS = 3600
_UNSAFE_SHELL_OPERATORS = ("&&", "||", ";", "|", ">", "<", "`", "$(")


@dataclass(frozen=True)
class ProjectCommandPlan:
    name: str
    command: str
    timeout_seconds: int = 300
    working_directory: str = "."


def _has_unsafe_shell_operator(command: str) -> bool:
    quote: str | None = None
    escaped = False
    index = 0
    while index < len(command):
        char = command[index]
        if escaped:
            escaped = False
            index += 1
            continue
        if char == "\\" and quote != "'":
            escaped = True
            index += 1
            continue
        if quote:
            if char == quote:
                quote = None
            index += 1
            continue
        if char in {"'", '"'}:
            quote = char
            index += 1
            continue
        if command.startswith("$(", index):
            return True
        if command.startswith("&&", index) or command.startswith("||", index):
            return True
        if char in {";", "|", ">", "<", "`"}:
            return True
        index += 1
    return False


def build_project_command(name: str, command: str, timeout_seconds: int = 300, working_directory: str = ".") -> ProjectCommandPlan:
    if not name.strip() or not command.strip():
        raise ValueError("Command name and command are required.")
    if timeout_seconds <= 0 or timeout_seconds > _MAX_TIMEOUT_SECONDS:
        raise ValueError(f"Command timeout must be between 1 and {_MAX_TIMEOUT_SECONDS} seconds.")
    if not working_directory.strip():
        raise ValueError("Working directory is required.")
    if _has_unsafe_shell_operator(command):
        raise ValueError("Command contains unsupported shell control syntax.")
    return ProjectCommandPlan(name.strip(), command.strip(), timeout_seconds, str(Path(working_directory)))
