from __future__ import annotations

VISUAL_SKILLS = ("modeling", "characters", "rigging", "animation", "materials", "environment", "export")


def read_only_probe_prompt() -> str:
    return """# Blender MCP Read-Only Probe\n\nInspect the open Blender file. Read only; change nothing.\n\nReport:\n- Blender version;\n- current .blend file;\n- active scene and collections;\n- object counts by type;\n- selected objects;\n- materials;\n- armatures and animation actions;\n- cameras and lights;\n- available MCP capabilities.\n\nDo not create, delete, transform, export, execute Python, or change materials.\n"""


def safe_visual_prompt(task: str, skill: str) -> str:
    if skill not in VISUAL_SKILLS:
        raise ValueError(f"Unknown visual skill: {skill}")
    return f"""# Blender MCP Visual Task\n\nSkill: {skill}\nTask: {task}\n\nBefore editing:\n- confirm that the read-only probe passed;\n- confirm that the working .blend is saved;\n- list exact objects, collections, materials, actions, and files to change.\n\nDuring editing:\n- use only the selected skill;\n- do not execute Python or external commands unless explicitly approved;\n- do not overwrite source assets;\n- stop instead of silently using a workaround.\n\nAfter editing:\n- report every changed object and file;\n- provide a preview/render checklist;\n- provide an export checklist if applicable;\n- do not expand scope.\n"""
