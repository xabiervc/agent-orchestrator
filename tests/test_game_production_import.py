def test_game_production_package_is_importable():
    from game_production import AnimationContract, AudioContract, EventContract, TransitionContract, UIContract

    assert AudioContract is not None
    assert AnimationContract is not None
    assert EventContract is not None
    assert TransitionContract is not None
    assert UIContract is not None
