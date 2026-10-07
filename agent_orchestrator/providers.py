from __future__ import annotations

import shutil
from dataclasses import dataclass

from .models import Route

FORBIDDEN_ARGUMENTS = {"--api-key", "--token", "--password", "--secret"}


@dataclass(frozen=True)
class CommandPlan:
    provider: str
    command: list[str]
    environment: dict[str, str]
    notes: list[str]


@dataclass(frozen=True)
class ProviderStatus:
    provider: str
    executable: str
    available: bool
    reason: str


def build_command(route: Route, prompt_path: str, working_directory: str = ".") -> CommandPlan:
    if route.provider == "claude-code":
        command = ["claude", "--model", route.model, "--permission-mode", "plan", "--prompt-file", prompt_path]
    elif route.provider == "codex":
        command = ["codex", "--prompt-file", prompt_path]
    elif route.provider == "copilot":
        command = ["copilot", "--prompt-file", prompt_path]
    else:
        command = [route.provider, "--prompt-file", prompt_path]
    if any(argument in FORBIDDEN_ARGUMENTS for argument in command):
        raise ValueError("Command plan contains a forbidden credential argument.")
    return CommandPlan(route.provider, command, {}, [f"Run from {working_directory}.", "Credentials must be provided by the provider CLI.", "This is a command plan; the core does not execute it."])


def detect_provider(provider: str) -> ProviderStatus:
    executable = {"claude-code": "claude", "codex": "codex", "copilot": "copilot"}.get(provider, provider)
    path = shutil.which(executable)
    return ProviderStatus(provider, executable, path is not None, "found on PATH" if path else "executable not found on PATH")
