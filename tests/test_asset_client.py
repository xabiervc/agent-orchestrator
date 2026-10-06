from pathlib import Path

from plugins.asset_server.client import AssetServerClient
from plugins.asset_server.models import AssetDownloadRequest, AssetSearchRequest
from plugins.asset_server.policy import AssetPolicy


def test_client_uses_injected_transports_without_network(tmp_path: Path):
    calls = []

    def search(payload):
        calls.append(("search", payload))
        return [{"asset_id": "a", "name": "Tree", "provider": "test", "source_url": "https://example.com/a", "download_url": "https://example.com/a.glb", "license_name": "CC0"}]

    def download(url):
        calls.append(("download", url))
        return b"glb"

    client = AssetServerClient(search, download, AssetPolicy(tmp_path))
    candidates = client.search(AssetSearchRequest("tree"))
    assert candidates[0].name == "Tree"
    provenance = client.download(AssetDownloadRequest(candidates[0], "tree.glb", approved=True))
    assert (tmp_path / "tree.glb").read_bytes() == b"glb"
    assert [call[0] for call in calls] == ["search", "download"]
    assert provenance["sha256"]
