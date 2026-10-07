from __future__ import annotations

from dataclasses import asdict, replace
from typing import Any

from .models import DEFAULT_ROUTES, Route
from .policy import RoutingPolicy


def route_for(role: str, *, risk: str = "normal", profiles: list[str] | None = None) -> Route:
    del profiles
    if role in {"planning", "review"} and risk in {"high", "critical"}:
        key = "architecture_review" if "architecture_review" in DEFAULT_ROUTES else role
    elif role in {"implementation", "implement"}:
        preferred = "complex_implementation" if risk in {"high", "critical"} else "normal_implementation"
        if risk == "low":
            preferred = "low_risk_implementation"
        key = preferred if preferred in DEFAULT_ROUTES else "complex_implementation"
    else:
        key = role if role in DEFAULT_ROUTES else "planning"
    selected = DEFAULT_ROUTES[key]
    return replace(selected, model=RoutingPolicy().model_for(risk))


def route_dict(route: Route) -> dict[str, Any]:
    return asdict(route)
