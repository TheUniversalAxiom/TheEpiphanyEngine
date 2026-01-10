"""Elements (B) component."""

from __future__ import annotations

from dataclasses import dataclass

from .base import Component


@dataclass(frozen=True)
class Elements(Component):
    """Elements component (B) in [0, 1]."""

    name: str = "B"
    minimum: float = 0.0
    maximum: float = 1.0
