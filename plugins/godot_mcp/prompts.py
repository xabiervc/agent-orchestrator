from __future__ import annotations


def read_only_probe_prompt() -> str:
    return """# Godot MCP Read-Only Probe\n\nInspect the open Godot project. Read only; change nothing.\n\nReport:\n- project name and Godot version;\n- current scene and root node;\n- autoloads;\n- input actions;\n- enabled plugins;\n- available MCP capabilities.\n\nDo not modify project.godot, scenes, scripts, assets, input actions, autoloads, UIDs, export presets, or editor state.\n"""


def safe_change_prompt(task: str) -> str:
    return f"""# Godot MCP Change Request\n\nTask: {task}\n\nBefore editing:\n- confirm that the read-only probe passed;\n- confirm that the game is stopped;\n- confirm that importing is not active;\n- list exact scenes, scripts, resources, and project files to change.\n\nDuring editing:\n- change one system only;\n- preserve scene ownership and resource UIDs;\n- run the declared project checks;\n- stop instead of silently using a workaround.\n\nAfter editing:\n- report every changed file and resource;\n- report new debugger errors;\n- provide a Play checklist;\n- do not expand scope.\n"""
