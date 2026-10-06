from pathlib import Path

from agent_orchestrator.runs import latest_run


def test_latest_run_ignores_non_directories(tmp_path: Path):
    runs = tmp_path / ".agent" / "runs"
    (runs / "20260101T000000Z-old").mkdir(parents=True)
    (runs / "notes.txt").write_text("not a run")
    (runs / "20260102T000000Z-new").mkdir()
    assert latest_run(tmp_path).name == "20260102T000000Z-new"
