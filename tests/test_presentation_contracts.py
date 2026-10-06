from game_production.presentation import TransitionContract, validate_transition_contract


def test_transition_contract_accepts_coordinated_transition():
    contract = TransitionContract("to_combat", "exploration", "combat", 1000, 700, 500)
    assert validate_transition_contract(contract) == []


def test_transition_contract_rejects_long_crossfade():
    contract = TransitionContract("bad", "a", "b", 100, 200)
    assert validate_transition_contract(contract)
