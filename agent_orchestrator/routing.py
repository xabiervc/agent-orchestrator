from __future__ import annotations

from dataclasses import asdict, replace
from typing import Any

from .models import DEFAULT_ROUTES, Route
from .policy import RoutingPolicy


def route_for(role: str, *, risk: str = "normal", profiles: list[str] | None = None) -> Route:
    profiles = profiles or []
    if role in {"planning", "review"} and risk in {"high", "critical"}:
        selected = DEFAULT_ROUTES["architecture_review"]
    elif role in {"implementation", "implement"}:
        key = "complex_implementation" if risk in {"high", "critical"} else "normal_implementation"
        if risk == "low":
            key = "low_risk_implementation"
        selected = DEFAULT_ROUTES[key]
    else:
        selected = DEFAULT_ROUTES.get(role, DEFAULT_ROUTES["planning"])
    return replace(selected, model=RoutingPolicy().model_for(risk))


def route_dict(route: Route) -> dict[str, Any]:
    return asdict(route)
