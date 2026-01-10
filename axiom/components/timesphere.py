"""TimeSphere (Z) component."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .base import Component


@dataclass(frozen=True)
class TimeSphere(Component):
    """TimeSphere component (Z) with lower bound at 0."""

    name: str = "Z"
    minimum: float = 0.0
    maximum: Optional[float] = None
