from __future__ import annotations

from pathlib import Path

from .models import VisualAssetContract

SUPPORTED_FORMATS = {"glb", "gltf", "fbx", "obj"}


def validate_export_request(contract: VisualAssetContract, *, approved: bool = False, overwrite: bool = False, project_root: Path | None = None) -> list[str]:
    errors: list[str] = []
    if not approved:
        errors.append("Asset export requires explicit approval.")
    if contract.export_format.lower() not in SUPPORTED_FORMATS:
        errors.append(f"Unsupported export format: {contract.export_format}.")
    if not contract.destination.strip():
        errors.append("Export destination must not be empty.")
    if project_root is not None:
        destination = (project_root / contract.destination).resolve()
        root = project_root.resolve()
        if root not in destination.parents and destination != root:
            errors.append("Export destination escapes the project root.")
        if destination.exists() and not overwrite:
            errors.append("Export destination exists and overwrite is disabled.")
    return errors
