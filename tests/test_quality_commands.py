import hashlib
import sys
import time
from pathlib import Path

from agent_orchestrator.commands import build_project_command
from agent_orchestrator.quality import execute_quality_command


def test_command_gate_records_success_and_hashes():
    plan = build_project_command("tests", f"{sys.executable} -c \"print('ok')\"")
    result = execute_quality_command(plan)
    assert result["passed"] is True
    assert result["return_code"] == 0
    assert result["stdout_hash"] == hashlib.sha256(b"ok\n").hexdigest()
    assert len(result["command_hash"]) == 64


def test_command_gate_records_nonzero_exit():
    plan = build_project_command("tests", f"{sys.executable} -c \"raise SystemExit(3)\"")
    result = execute_quality_command(plan)
    assert result["passed"] is False
    assert result["return_code"] == 3


def test_command_gate_records_timeout():
    plan = build_project_command("tests", f"{sys.executable} -c \"import time; time.sleep(1)\"", timeout_seconds=1)
    result = execute_quality_command(plan)
    assert result["passed"] is False
    assert result["timed_out"] is True
