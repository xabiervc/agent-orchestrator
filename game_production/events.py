from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EventResponse:
    channel: str
    action: str
    target: str | None = None


@dataclass(frozen=True)
class EventContract:
    name: str
    responses: tuple[EventResponse, ...] = ()
    payload: tuple[str, ...] = ()
    description: str = ""


def validate_event_contract(contract: EventContract) -> list[str]:
    errors: list[str] = []
    if not contract.name.strip():
        errors.append("Event name must not be empty.")
    if any(not response.channel.strip() or not response.action.strip() for response in contract.responses):
        errors.append("Every event response needs a channel and action.")
    if len({(response.channel, response.action, response.target) for response in contract.responses}) != len(contract.responses):
        errors.append("Event responses must be unique.")
    return errors
