from plugins.unreal_mcp.prompts import read_only_probe_prompt, safe_change_prompt


def test_probe_prompt_is_read_only():
    prompt = read_only_probe_prompt()
    assert "change nothing" in prompt.lower()
    assert "Player Start" in prompt


def test_change_prompt_requires_compile_and_scope():
    prompt = safe_change_prompt("Add one enemy")
    assert "compile" in prompt.lower()
    assert "do not expand scope" in prompt.lower()
