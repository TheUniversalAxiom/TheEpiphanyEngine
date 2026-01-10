"""Impulses (A) component."""

from __future__ import annotations

from dataclasses import dataclass

from .base import Component


@dataclass(frozen=True)
class Impulses(Component):
    """Impulses component (A) in [0, 1]."""

    name: str = "A"
    minimum: float = 0.0
    maximum: float = 1.0
