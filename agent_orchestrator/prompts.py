from __future__ import annotations

from pathlib import Path

from .models import Route


def render_prompt(run_id: str, role: str, route: Route, task_path: str, context_paths: list[str]) -> str:
    context = "\n".join(f"- `{path}`" for path in context_paths) or "- No additional context files were declared."
    return f"""# Agent Run Prompt\n\nRun: `{run_id}`\nRole: `{role}`\nProvider: `{route.provider}`\nRequested model: `{route.model}`\nEffort: `{route.effort}`\n\n## Task artifact\n\nRead `{task_path}` before proposing or editing anything.\n\n## Shared context\n\n{context}\n\n## Safety contract\n\n- Do not expand the task scope.\n- Do not edit when the run has no approved consensus.\n- Report files changed, commands, exit codes, and unverified behavior.\n- Never write credentials, tokens, cookies, or secrets to artifacts.\n\nReturn a structured result suitable for saving under the run artifact directories.\n"""


def write_prompt(path: Path, run_id: str, role: str, route: Route, task_path: str, context_paths: list[str]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_prompt(run_id, role, route, task_path, context_paths), encoding="utf-8")
    return path
