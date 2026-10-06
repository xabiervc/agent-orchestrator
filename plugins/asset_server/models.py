from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class AssetSearchRequest:
    query: str
    asset_types: tuple[str, ...] = ("model",)
    free_only: bool = True
    downloadable_only: bool = True
    license_allowlist: tuple[str, ...] = ()


@dataclass(frozen=True)
class AssetCandidate:
    asset_id: str
    name: str
    provider: str
    source_url: str
    download_url: str | None = None
    license_name: str | None = None
    attribution_required: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class AssetDownloadRequest:
    candidate: AssetCandidate
    destination: str
    approved: bool = False
    overwrite: bool = False
