from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse
import ipaddress
import socket

from .models import AssetDownloadRequest, AssetSearchRequest


@dataclass(frozen=True)
class AssetPolicy:
    asset_root: Path
    allowed_licenses: tuple[str, ...] = ("CC0", "CC BY", "CC BY 4.0")
    allow_unknown_license: bool = False
    allow_overwrite: bool = False

    def validate_search(self, request: AssetSearchRequest) -> list[str]:
        errors: list[str] = []
        if not request.query.strip():
            errors.append("Search query must not be empty.")
        if not request.asset_types:
            errors.append("At least one asset type is required.")
        return errors

    def validate_download(self, request: AssetDownloadRequest) -> list[str]:
        errors: list[str] = []
        if not request.approved:
            errors.append("Asset download requires explicit approval.")
        url = request.candidate.download_url
        if not url:
            errors.append("Candidate has no download URL.")
        else:
            errors.extend(validate_public_url(url))
        license_name = request.candidate.license_name
        if not license_name and not self.allow_unknown_license:
            errors.append("Asset license is unknown.")
        elif license_name and license_name not in self.allowed_licenses:
            errors.append(f"License is not allowed: {license_name}.")
        destination = (self.asset_root / request.destination).resolve()
        root = self.asset_root.resolve()
        if destination != root and root not in destination.parents:
            errors.append("Destination escapes the configured asset root.")
        if destination.exists() and not (request.overwrite and self.allow_overwrite):
            errors.append("Destination exists and overwrite is disabled.")
        return errors


def validate_public_url(url: str) -> list[str]:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        return ["Only HTTP(S) URLs are allowed."]
    if not parsed.hostname:
        return ["URL must include a hostname."]
    host = parsed.hostname.lower()
    if host == "localhost" or host.endswith(".localhost"):
        return ["Loopback hostnames are not allowed."]
    try:
        addresses = socket.getaddrinfo(host, None)
    except OSError:
        addresses = []
    for address in addresses:
        ip = ipaddress.ip_address(address[4][0])
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved:
            return ["Private or non-public address is not allowed."]
    return []
