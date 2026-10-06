from game_production.animation import AnimationContract, AnimationTransition, validate_animation_contract


def test_animation_contract_validates_transitions():
    contract = AnimationContract("hero", ("idle", "walk"), (AnimationTransition("idle", "walk"),), ("idle",))
    assert validate_animation_contract(contract) == []


def test_animation_contract_rejects_unknown_state():
    contract = AnimationContract("hero", ("idle",), (AnimationTransition("idle", "run"),))
    assert validate_animation_contract(contract)
