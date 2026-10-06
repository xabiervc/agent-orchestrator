from plugins.asset_server.models import AssetCandidate
from plugins.asset_server.provenance import build_provenance


def test_provenance_contains_hash_and_license():
    data = build_provenance(AssetCandidate("a", "Tree", "test", "https://example.com", license_name="CC0"), "tree.glb", b"asset")
    assert data["license"] == "CC0"
    assert len(data["sha256"]) == 64
    assert data["destination"] == "tree.glb"
