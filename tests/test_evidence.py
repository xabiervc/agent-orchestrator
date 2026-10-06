from pathlib import Path

from agent_orchestrator.evidence import create_evidence_manifest, validate_evidence_manifest


def test_evidence_manifest_round_trip(tmp_path: Path):
    run = tmp_path / "run"
    (run / "evidence").mkdir(parents=True)
    manifest = create_evidence_manifest(run, [{"path": "screenshot.png", "kind": "screenshot"}])
    assert validate_evidence_manifest(manifest, "run") == []
