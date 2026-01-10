"""Pressure (C) component."""

from __future__ import annotations

from dataclasses import dataclass

from .base import Component


@dataclass(frozen=True)
class Pressure(Component):
    """Pressure component (C) in [0, 1]."""

    name: str = "C"
    minimum: float = 0.0
    maximum: float = 1.0
