from plugins.godot_mcp.prompts import read_only_probe_prompt, safe_change_prompt


def test_probe_prompt_is_read_only():
    prompt = read_only_probe_prompt()
    assert "change nothing" in prompt.lower()
    assert "project.godot" in prompt


def test_change_prompt_preserves_uids_and_scope():
    prompt = safe_change_prompt("Add a pause menu")
    assert "resource uids" in prompt.lower()
    assert "do not expand scope" in prompt.lower()
