from __future__ import annotations

from dataclasses import asdict
from typing import Any

from .models import DEFAULT_ROUTES, Route


def route_for(role: str, *, risk: str = "normal", profiles: list[str] | None = None) -> Route:
    profiles = profiles or []
    if role in {"planning", "review"} and risk in {"high", "critical"}:
        return DEFAULT_ROUTES["architecture_review"]
    if role in {"implementation", "implement"}:
        key = "complex_implementation" if risk in {"high", "critical"} else "normal_implementation"
        if risk == "low":
            key = "low_risk_implementation"
        return DEFAULT_ROUTES[key]
    return DEFAULT_ROUTES.get(role, DEFAULT_ROUTES["planning"])


def route_dict(route: Route) -> dict[str, Any]:
    return asdict(route)
