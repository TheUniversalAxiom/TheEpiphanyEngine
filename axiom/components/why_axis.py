"""Why Axis (Y) component."""

from __future__ import annotations

from dataclasses import dataclass

from .base import Component


@dataclass(frozen=True)
class WhyAxis(Component):
    """Why Axis component (Y) in [0, 1]."""

    name: str = "Y"
    minimum: float = 0.0
    maximum: float = 1.0
