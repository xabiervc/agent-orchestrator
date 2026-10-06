from game_production.ui import UIContract, UIControl, validate_ui_contract


def test_ui_contract_requires_unique_controls():
    control = UIControl("play", "button")
    assert validate_ui_contract(UIContract("main_menu", (control, control)))


def test_ui_contract_accepts_keyboard_and_gamepad_navigation():
    contract = UIContract("main_menu", (UIControl("play", "button"),))
    assert validate_ui_contract(contract) == []
