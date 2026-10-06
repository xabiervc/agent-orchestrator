from agent_orchestrator.quality import evaluate_quality


def test_quality_requires_all_default_gates():
    result = evaluate_quality({"tests": True, "validation": True, "evidence": False})
    assert result.passed is False
    assert result.failures == ["evidence"]


def test_quality_passes_all_gates():
    assert evaluate_quality({"tests": True, "validation": True, "evidence": True}).passed is True
