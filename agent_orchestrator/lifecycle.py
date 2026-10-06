from __future__ import annotations

from pathlib import Path

from .runs import advance_run, create_run, load_run


def start_task(root: Path, task: str) -> Path:
    return create_run(root, task)


def advance_task(run: Path, state: str = "advanced") -> dict:
    return advance_run(run, state)


def current_state(run: Path) -> dict:
    return load_run(run)
