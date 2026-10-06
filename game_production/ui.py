from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class UIControl:
    control_id: str
    control_type: str
    focusable: bool = True
    action: str | None = None


@dataclass(frozen=True)
class UIContract:
    screen_id: str
    controls: tuple[UIControl, ...]
    supports_keyboard: bool = True
    supports_gamepad: bool = True
    accessible_labels_required: bool = True


def validate_ui_contract(contract: UIContract) -> list[str]:
    errors: list[str] = []
    if not contract.screen_id.strip():
        errors.append("UI screen_id must not be empty.")
    ids = [control.control_id for control in contract.controls]
    if len(ids) != len(set(ids)):
        errors.append("UI control IDs must be unique.")
    if not contract.controls:
        errors.append("UI screen needs at least one control.")
    if contract.supports_keyboard and not any(control.focusable for control in contract.controls):
        errors.append("Keyboard-enabled UI needs a focusable control.")
    if contract.supports_gamepad and not any(control.focusable for control in contract.controls):
        errors.append("Gamepad-enabled UI needs a focusable control.")
    if contract.accessible_labels_required and any(not control.control_id.strip() for control in contract.controls):
        errors.append("Accessible controls need non-empty IDs.")
    return errors
