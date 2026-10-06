from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
from typing import Any

from .models import AssetCandidate


def build_provenance(candidate: AssetCandidate, destination: str, payload: bytes) -> dict[str, Any]:
    return {
        "asset_id": candidate.asset_id,
        "name": candidate.name,
        "provider": candidate.provider,
        "source_url": candidate.source_url,
        "download_url": candidate.download_url,
        "license": candidate.license_name,
        "attribution_required": candidate.attribution_required,
        "destination": destination,
        "sha256": sha256(payload).hexdigest(),
        "downloaded_at": datetime.now(timezone.utc).isoformat(),
    }
