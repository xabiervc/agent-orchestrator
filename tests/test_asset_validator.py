from io import BytesIO
from zipfile import ZipFile

from plugins.asset_server.validator import validate_archive_members


def zip_payload(name: str) -> bytes:
    buffer = BytesIO()
    with ZipFile(buffer, "w") as archive:
        archive.writestr(name, b"data")
    return buffer.getvalue()


def test_rejects_zip_slip_member():
    assert validate_archive_members(zip_payload("../../outside.txt"))


def test_accepts_safe_archive():
    assert validate_archive_members(zip_payload("models/tree.glb")) == []
