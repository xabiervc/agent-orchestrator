from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TransitionContract:
    name: str
    source: str
    target: str
    duration_ms: int = 500
    audio_crossfade_ms: int = 0
    camera_blend_ms: int = 0
    blocks_input: bool = True
    cancelable: bool = False


def validate_transition_contract(contract: TransitionContract) -> list[str]:
    errors: list[str] = []
    if not contract.name.strip() or not contract.source.strip() or not contract.target.strip():
        errors.append("Transition name, source, and target are required.")
    for value, label in ((contract.duration_ms, "duration_ms"), (contract.audio_crossfade_ms, "audio_crossfade_ms"), (contract.camera_blend_ms, "camera_blend_ms")):
        if value < 0:
            errors.append(f"{label} cannot be negative.")
    if contract.audio_crossfade_ms > contract.duration_ms and contract.duration_ms >= 0:
        errors.append("Audio crossfade cannot exceed transition duration.")
    if contract.camera_blend_ms > contract.duration_ms and contract.duration_ms >= 0:
        errors.append("Camera blend cannot exceed transition duration.")
    return errors
