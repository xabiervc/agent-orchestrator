import sys
from pathlib import Path

import pytest

from agent_orchestrator.quality import execute_quality_command, run_quality_command


def test_quality_command_passes_and_returns_execution_evidence(tmp_path: Path):
    report = run_quality_command(
        "tests",
        f'{sys.executable} -c "print(\'ok\')"',
        project_root=tmp_path,
    )
    assert report.passed is True
    assert "command_hash" in report.gates[0].details
    assert "return_code\': 0" in report.gates[0].details


def test_quality_command_reports_failure(tmp_path: Path):
    report = run_quality_command(
        "tests",
        f'{sys.executable} -c "raise SystemExit(3)"',
        project_root=tmp_path,
    )
    assert report.passed is False
    assert "return_code\': 3" in report.gates[0].details


def test_quality_command_reports_timeout(tmp_path: Path):
    report = run_quality_command(
        "tests",
        f'{sys.executable} -c "import time; time.sleep(1)"',
        timeout_seconds=1,
        project_root=tmp_path,
    )
    assert report.passed is False
    assert "timed_out\': True" in report.gates[0].details


def test_quality_command_still_rejects_shell_control(tmp_path: Path):
    with pytest.raises(ValueError):
        run_quality_command("tests", "echo ok && echo bypass", project_root=tmp_path)


def test_legacy_execute_quality_command_api_delegates(tmp_path: Path):
    report = execute_quality_command(
        "tests",
        f'{sys.executable} -c "print(\'ok\')"',
        project_root=tmp_path,
    )
    assert report.passed is True
