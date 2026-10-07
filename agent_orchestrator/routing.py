from __future__ import annotations

from dataclasses import asdict, replace
from typing import Any

from .models import DEFAULT_ROUTES, Route
from .policy import RoutingPolicy


def route_for(role: str, *, risk: str = "normal", profiles: list[str] | None = None) -> Route:
    del profiles
    normalized_risk = "normal" if risk == "mechanical" else risk
    if role in {"planning", "review"} and normalized_risk in {"high", "critical"}:
        key = "architecture_review" if "architecture_review" in DEFAULT_ROUTES else role
    elif role in {"implementation", "implement"}:
        preferred = "complex_implementation" if normalized_risk in {"high", "critical"} else "normal_implementation"
        if normalized_risk == "low":
            preferred = "low_risk_implementation"
        key = preferred if preferred in DEFAULT_ROUTES else "complex_implementation"
    else:
        key = role if role in DEFAULT_ROUTES else "planning"
    selected = DEFAULT_ROUTES[key]
    return replace(selected, model=RoutingPolicy().model_for(normalized_risk))


def route_dict(route: Route) -> dict[str, Any]:
    return asdict(route)
