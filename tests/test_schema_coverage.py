from __future__ import annotations

import agent_orchestrator.schemas as schemas


def test_schemas_module_imports() -> None:
    assert schemas is not None
