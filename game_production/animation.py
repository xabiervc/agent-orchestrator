from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AnimationTransition:
    source: str
    target: str
    crossfade_ms: int = 150


@dataclass(frozen=True)
class AnimationContract:
    character: str
    states: tuple[str, ...]
    transitions: tuple[AnimationTransition, ...] = ()
    required_actions: tuple[str, ...] = ()
    blend_parameter: str | None = None


def validate_animation_contract(contract: AnimationContract) -> list[str]:
    errors: list[str] = []
    if not contract.character.strip():
        errors.append("Animation character must not be empty.")
    if not contract.states:
        errors.append("Animation contract needs at least one state.")
    known = set(contract.states)
    for transition in contract.transitions:
        if transition.source not in known or transition.target not in known:
            errors.append(f"Unknown animation transition: {transition.source}->{transition.target}.")
        if transition.crossfade_ms < 0:
            errors.append("Animation crossfade cannot be negative.")
    missing = set(contract.required_actions) - known
    if missing:
        errors.append(f"Required animation actions are not states: {sorted(missing)}.")
    return errors
