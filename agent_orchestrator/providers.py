from __future__ import annotations

from dataclasses import dataclass
import shutil

from .models import Route


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
    return CommandPlan(route.provider, command, {}, [f"Run from {working_directory}.", "Credentials must be provided by the provider CLI.", "This is a command plan; the core does not execute it."])


def detect_provider(provider: str) -> ProviderStatus:
    executable = {"claude-code": "claude", "codex": "codex", "copilot": "copilot"}.get(provider, provider)
    path = shutil.which(executable)
    return ProviderStatus(provider, executable, path is not None, "found on PATH" if path else "executable not found on PATH")
