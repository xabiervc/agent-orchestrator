from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class GodotProject:
    root: Path
    project_file: Path
    mcp_config: Path | None = None


@dataclass(frozen=True)
class GodotPreflight:
    ready: bool
    checks: list[dict[str, str]] = field(default_factory=list)

    @property
    def blocking_checks(self) -> list[dict[str, str]]:
        return [check for check in self.checks if check["status"] == "blocked"]
