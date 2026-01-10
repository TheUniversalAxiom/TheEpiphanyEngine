"""Fibonacci Sequence (F_n) component."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .base import Component


@dataclass(frozen=True)
class FibonacciSequence(Component):
    """Fibonacci Sequence component (F_n) with lower bound at -1."""

    name: str = "F_n"
    minimum: float = -1.0
    maximum: Optional[float] = None
