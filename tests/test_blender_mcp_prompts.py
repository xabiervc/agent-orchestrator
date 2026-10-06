import pytest

from plugins.blender_mcp.prompts import read_only_probe_prompt, safe_visual_prompt


def test_probe_prompt_is_read_only():
    prompt = read_only_probe_prompt()
    assert "change nothing" in prompt.lower()
    assert "execute python" in prompt.lower()


def test_visual_prompt_requires_known_skill():
    assert "characters" in safe_visual_prompt("Create a hero", "characters")
    with pytest.raises(ValueError):
        safe_visual_prompt("Create a thing", "unknown")
