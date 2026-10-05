from agent_orchestrator.policy import RoutingPolicy


def test_policy_routes_by_risk():
    policy = RoutingPolicy()
    assert policy.model_for("mechanical") == "haiku"
    assert policy.model_for("normal") == "sonnet"
    assert policy.model_for("high") == "opus"
