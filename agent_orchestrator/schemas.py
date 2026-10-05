from __future__ import annotations

from typing import Any

SCHEMA_VERSION = 1


def task_artifact(run_id: str, task: str, project: dict[str, Any]) -> dict[str, Any]:
    return {"schema_version": SCHEMA_VERSION, "type": "task", "run_id": run_id, "task": task, "project": project}


def consensus_artifact(run_id: str) -> dict[str, Any]:
    return {"schema_version": SCHEMA_VERSION, "type": "consensus", "run_id": run_id, "decision": "pending", "blocking_reasons": []}


def provider_artifact(run_id: str, provider: str, role: str, status: str = "completed") -> dict[str, Any]:
    return {"schema_version": SCHEMA_VERSION, "type": "provider_result", "run_id": run_id, "provider": provider, "role": role, "status": status, "model_requested": None, "model_reported": None, "files_changed": [], "verification": []}
