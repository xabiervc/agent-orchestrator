from pathlib import Path

from plugins.blender_mcp.export_policy import validate_export_request
from plugins.blender_mcp.models import VisualAssetContract


def contract(**overrides):
    data = {"name": "hero", "asset_type": "character", "target_engine": "godot", "export_format": "glb", "destination": "assets/hero/hero.glb"}
    data.update(overrides)
    return VisualAssetContract(**data)


def test_export_requires_approval(tmp_path: Path):
    errors = validate_export_request(contract(), project_root=tmp_path)
    assert any("approval" in error.lower() for error in errors)


def test_export_rejects_path_escape(tmp_path: Path):
    errors = validate_export_request(contract(destination="../hero.glb"), approved=True, project_root=tmp_path)
    assert any("escapes" in error.lower() for error in errors)


def test_export_accepts_supported_format(tmp_path: Path):
    assert validate_export_request(contract(), approved=True, project_root=tmp_path) == []
