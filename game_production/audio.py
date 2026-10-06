from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AudioContract:
    asset_id: str
    audio_type: str
    event: str | None = None
    format: str = "wav"
    loop: bool = False
    variations: int = 1
    license_name: str | None = None
    attribution_required: bool = False
    duration_ms_max: int | None = None


def validate_audio_contract(contract: AudioContract) -> list[str]:
    errors: list[str] = []
    if not contract.asset_id.strip():
        errors.append("Audio asset_id must not be empty.")
    if contract.audio_type not in {"music", "sound_effect", "voice", "ambient", "stinger"}:
        errors.append(f"Unsupported audio type: {contract.audio_type}.")
    if contract.variations < 1:
        errors.append("Audio variations must be at least 1.")
    if contract.audio_type in {"sound_effect", "stinger"} and not contract.event:
        errors.append("Sound effects and stingers require an event.")
    if contract.duration_ms_max is not None and contract.duration_ms_max <= 0:
        errors.append("duration_ms_max must be positive.")
    if contract.license_name is None:
        errors.append("Audio license must be declared.")
    return errors
