from agent_orchestrator.worktrees import plan_worktree


def test_high_risk_requires_worktree():
    plan = plan_worktree("run-1", "high")
    assert plan.required is True


def test_normal_single_agent_does_not_require_worktree():
    plan = plan_worktree("run-1", "normal")
    assert plan.required is False
