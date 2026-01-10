"""Axiom components for The Epiphany Engine."""

from __future__ import annotations

from .core_equation import (
    compute_intelligence,
    e_recurrence,
    e_sequence,
    fibonacci,
    fibonacci_sequence,
)
from .components import (
    Component,
    Elements,
    ExponentialGrowth,
    FibonacciSequence,
    Impulses,
    Pressure,
    SubjectivityScale,
    TimeSphere,
    WhyAxis,
)

UNIVERSAL_AXIOM = "Intelligence_n = E_n * (1 + F_n) * X * Y * Z * (A * B * C)"

__all__ = [
    "UNIVERSAL_AXIOM",
    "compute_intelligence",
    "e_recurrence",
    "e_sequence",
    "fibonacci",
    "fibonacci_sequence",
    "Component",
    "Elements",
    "ExponentialGrowth",
    "FibonacciSequence",
    "Impulses",
    "Pressure",
    "SubjectivityScale",
    "TimeSphere",
    "WhyAxis",
]
