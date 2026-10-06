from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class BlenderProject:
    root: Path
    blend_file: Path | None = None
    mcp_config: Path | None = None


@dataclass(frozen=True)
class BlenderPreflight:
    ready: bool
    checks: list[dict[str, str]] = field(default_factory=list)

    @property
    def blocking_checks(self) -> list[dict[str, str]]:
        return [check for check in self.checks if check["status"] == "blocked"]


@dataclass(frozen=True)
class VisualAssetContract:
    name: str
    asset_type: str
    target_engine: str
    export_format: str
    destination: str
    max_triangles: int | None = None
    max_material_slots: int | None = None
    scale_unit: str = "meters"
    required_actions: tuple[str, ...] = ()
