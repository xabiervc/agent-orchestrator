from agent_orchestrator.quality import QualityResult, evaluate_quality


def test_quality_requires_all_default_gates():
    result = evaluate_quality({"tests": True, "validation": True, "evidence": False})
    assert isinstance(result, QualityResult)
    assert result.passed is False
    assert result.failures == ["evidence"]


def test_quality_passes_all_default_gates():
    result = evaluate_quality({"tests": True, "validation": True, "evidence": True})
    assert result.passed is True
    assert result.failures == []
