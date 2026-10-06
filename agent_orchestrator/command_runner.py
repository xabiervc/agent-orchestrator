from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path
import shlex
import subprocess
from typing import Any

from .commands import ProjectCommandPlan


@dataclass(frozen=True)
class CommandExecution:
    passed: bool
    return_code: int | None
    timed_out: bool
    command_hash: str
    stdout_hash: str
    stderr_hash: str
    working_directory: str


def _hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _safe_working_directory(root: Path, working_directory: str) -> Path:
    project_root = root.resolve()
    candidate = (project_root / working_directory).resolve()
    if candidate != project_root and project_root not in candidate.parents:
        raise ValueError("Working directory must remain inside the project root.")
    if not candidate.exists() or not candidate.is_dir():
        raise ValueError("Working directory must exist and be a directory.")
    return candidate


def execute_command(plan: ProjectCommandPlan, *, project_root: Path | None = None) -> dict[str, Any]:
    root = (project_root or Path.cwd()).resolve()
    try:
        argv = shlex.split(plan.command, posix=True)
    except ValueError as exc:
        raise ValueError("Command has malformed quoting.") from exc
    if not argv:
        raise ValueError("Command must contain an executable.")
    working_directory = _safe_working_directory(root, plan.working_directory)
    try:
        completed = subprocess.run(
            argv,
            shell=False,
            cwd=working_directory,
            capture_output=True,
            text=True,
            timeout=plan.timeout_seconds,
            check=False,
        )
        stdout = completed.stdout or ""
        stderr = completed.stderr or ""
        return {
            "gate": plan.name,
            "command_hash": _hash(plan.command),
            "working_directory": str(working_directory),
            "return_code": completed.returncode,
            "timed_out": False,
            "passed": completed.returncode == 0,
            "stdout_hash": _hash(stdout),
            "stderr_hash": _hash(stderr),
        }
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""
        if isinstance(stdout, bytes):
            stdout = stdout.decode("utf-8", errors="replace")
        if isinstance(stderr, bytes):
            stderr = stderr.decode("utf-8", errors="replace")
        return {
            "gate": plan.name,
            "command_hash": _hash(plan.command),
            "working_directory": str(working_directory),
            "return_code": None,
            "timed_out": True,
            "passed": False,
            "stdout_hash": _hash(stdout),
            "stderr_hash": _hash(stderr),
        }
