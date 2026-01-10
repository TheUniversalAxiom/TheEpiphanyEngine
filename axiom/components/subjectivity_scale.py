"""Axiomatic Subjectivity Scale (X) component."""

from __future__ import annotations

from dataclasses import dataclass

from .base import Component


@dataclass(frozen=True)
class SubjectivityScale(Component):
    """Axiomatic Subjectivity Scale component (X) in [0, 1]."""

    name: str = "X"
    minimum: float = 0.0
    maximum: float = 1.0
