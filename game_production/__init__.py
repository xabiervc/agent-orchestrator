"""Engine-neutral contracts for game audio, animation, UI, and presentation."""

from .events import EventContract, EventResponse, validate_event_contract
from .audio import AudioContract, validate_audio_contract
from .animation import AnimationContract, validate_animation_contract
from .ui import UIContract, validate_ui_contract
from .presentation import TransitionContract, validate_transition_contract

__all__ = ["EventContract", "EventResponse", "AudioContract", "AnimationContract", "UIContract", "TransitionContract", "validate_event_contract", "validate_audio_contract", "validate_animation_contract", "validate_ui_contract", "validate_transition_contract"]
