from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from .models import AssetCandidate, AssetDownloadRequest, AssetSearchRequest
from .policy import AssetPolicy
from .provenance import build_provenance
from .validator import validate_archive_members


@dataclass(frozen=True)
class AssetServerClient:
    search_transport: Callable[[dict[str, Any]], list[dict[str, Any]]]
    download_transport: Callable[[str], bytes]
    policy: AssetPolicy

    def search(self, request: AssetSearchRequest) -> list[AssetCandidate]:
        errors = self.policy.validate_search(request)
        if errors:
            raise ValueError(" ".join(errors))
        results = self.search_transport({"query": request.query, "types": list(request.asset_types), "free_only": request.free_only, "downloadable_only": request.downloadable_only})
        candidates = [AssetCandidate(**result) for result in results]
        if request.license_allowlist:
            candidates = [candidate for candidate in candidates if candidate.license_name in request.license_allowlist]
        return candidates

    def download(self, request: AssetDownloadRequest) -> dict[str, Any]:
        errors = self.policy.validate_download(request)
        if errors:
            raise ValueError(" ".join(errors))
        payload = self.download_transport(request.candidate.download_url or "")
        destination = (self.policy.asset_root / request.destination).resolve()
        if destination.suffix.lower() == ".zip":
            archive_errors = validate_archive_members(payload)
            if archive_errors:
                raise ValueError(" ".join(archive_errors))
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(payload)
        return build_provenance(request.candidate, request.destination, payload)
