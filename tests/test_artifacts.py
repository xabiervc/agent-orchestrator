from pathlib import Path
from agent_orchestrator.artifacts import write_json, read_json


def test_json_round_trip(tmp_path: Path):
    path = tmp_path / "artifact.json"
    write_json(path, {"ok": True})
    assert read_json(path) == {"ok": True}
