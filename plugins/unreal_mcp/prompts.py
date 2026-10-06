from __future__ import annotations


def read_only_probe_prompt() -> str:
    return """# Unreal MCP Read-Only Probe\n\nInspect the open Unreal Editor project. Read only; change nothing.\n\nReport:\n- active level name;\n- main actors;\n- whether a Player Start exists;\n- whether a third-person character exists;\n- enabled MCP-related plugins if visible.\n\nDo not modify actors, assets, Blueprints, project settings, source files, or editor state.\n"""


def safe_change_prompt(task: str) -> str:
    return f"""# Unreal MCP Change Request\n\nTask: {task}\n\nBefore editing:\n- confirm that the read-only probe passed;\n- confirm that Play mode is stopped;\n- confirm that compilation is not active;\n- list exact assets, Blueprints, actors, and files to change.\n\nDuring editing:\n- change one system only;\n- compile every changed Blueprint;\n- report compile results;\n- stop instead of silently using a workaround.\n\nAfter editing:\n- report every changed asset and file;\n- report new Output Log errors;\n- provide a Play checklist;\n- do not expand scope.\n"""
