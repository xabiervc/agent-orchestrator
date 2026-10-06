from __future__ import annotations

from typing import Iterable

from .animation import AnimationContract, validate_animation_contract
from .audio import AudioContract, validate_audio_contract
from .events import EventContract, validate_event_contract
from .presentation import TransitionContract, validate_transition_contract
from .ui import UIContract, validate_ui_contract


def validate_game_production_contracts(*, events: Iterable[EventContract] = (), audio: Iterable[AudioContract] = (), animations: Iterable[AnimationContract] = (), ui: Iterable[UIContract] = (), transitions: Iterable[TransitionContract] = ()) -> list[str]:
    errors: list[str] = []
    for contract in events:
        errors.extend(validate_event_contract(contract))
    for contract in audio:
        errors.extend(validate_audio_contract(contract))
    for contract in animations:
        errors.extend(validate_animation_contract(contract))
    for contract in ui:
        errors.extend(validate_ui_contract(contract))
    for contract in transitions:
        errors.extend(validate_transition_contract(contract))
    return errors
