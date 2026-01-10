"""Base definitions for Universal Axiom components."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Optional


def validate_numeric(value: float, name: str) -> float:
    """Validate numeric input is finite and coerce to float."""
    val = float(value)
    if not math.isfinite(val):
        raise ValueError(f"{name} must be finite, got {value}")
    return val


def clamp_value(value: float, minimum: Optional[float], maximum: Optional[float]) -> float:
    """Clamp numeric value to optional bounds."""
    val = value
    if minimum is not None:
        val = max(minimum, val)
    if maximum is not None:
        val = min(maximum, val)
    return val


@dataclass(frozen=True)
class Component:
    """Base component container with optional bounds."""

    value: float
    name: str
    minimum: Optional[float] = None
    maximum: Optional[float] = None

    def normalized(self, clamp: bool = True) -> float:
        """Return normalized component value, optionally clamped to bounds."""
        val = validate_numeric(self.value, self.name)
        if clamp:
            return clamp_value(val, self.minimum, self.maximum)
        return val
