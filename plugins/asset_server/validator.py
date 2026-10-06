from __future__ import annotations

from io import BytesIO
from zipfile import BadZipFile, ZipFile


def validate_archive_members(payload: bytes) -> list[str]:
    try:
        archive = ZipFile(BytesIO(payload))
    except BadZipFile:
        return ["Downloaded ZIP is invalid."]
    errors: list[str] = []
    for member in archive.namelist():
        normalized = member.replace("\\", "/")
        if normalized.startswith("/") or any(part == ".." for part in normalized.split("/")):
            errors.append(f"Archive member escapes destination: {member}.")
    return errors
