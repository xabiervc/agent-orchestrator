from pathlib import Path

from plugins.asset_server.models import AssetCandidate, AssetDownloadRequest, AssetSearchRequest
from plugins.asset_server.policy import AssetPolicy, validate_public_url


def candidate(**overrides):
    data = {"asset_id": "a1", "name": "Tree", "provider": "test", "source_url": "https://example.com/a", "download_url": "https://example.com/a.zip", "license_name": "CC0"}
    data.update(overrides)
    return AssetCandidate(**data)


def test_search_requires_query(tmp_path: Path):
    policy = AssetPolicy(tmp_path)
    assert policy.validate_search(AssetSearchRequest(""))


def test_download_requires_approval(tmp_path: Path):
    policy = AssetPolicy(tmp_path)
    errors = policy.validate_download(AssetDownloadRequest(candidate(), "tree.zip"))
    assert any("approval" in error.lower() for error in errors)


def test_rejects_private_and_non_http_urls():
    assert validate_public_url("file:///tmp/tree.zip")
    assert validate_public_url("http://127.0.0.1/tree.zip")
    assert validate_public_url("http://localhost/tree.zip")


def test_rejects_path_escape(tmp_path: Path):
    policy = AssetPolicy(tmp_path)
    errors = policy.validate_download(AssetDownloadRequest(candidate(), "../outside.zip", approved=True))
    assert any("escapes" in error.lower() for error in errors)
