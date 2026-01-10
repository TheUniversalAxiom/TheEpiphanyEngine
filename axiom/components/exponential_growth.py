"""Exponential Growth (E_n) component."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .base import Component


@dataclass(frozen=True)
class ExponentialGrowth(Component):
    """Exponential Growth component (E_n) with lower bound at 0."""

    name: str = "E_n"
    minimum: float = 0.0
    maximum: Optional[float] = None
