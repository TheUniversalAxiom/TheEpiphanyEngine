"""
EPIPHANY Engine - The Universal Axiom Organic Intelligence Model

A physics-style framework for modeling and evolving intelligence over time.

Intelligence_n = E_n · (1 + F_n) · X · Y · Z · (A · B · C)
"""

__version__ = "0.1.0"

from epiphany_engine.axiom.core_equation import compute_intelligence, e_recurrence, fibonacci
from epiphany_engine.axiom.subjectivity_scale import x_from_observations, label_x
from epiphany_engine.engine.timesphere import TimeSphere, UpdateRules
from epiphany_engine.engine.state import AxiomInputs, SystemState, IntelligenceSnapshot

__all__ = [
    # Core functions
    "compute_intelligence",
    "e_recurrence",
    "fibonacci",
    # Subjectivity
    "x_from_observations",
    "label_x",
    # Simulation
    "TimeSphere",
    "UpdateRules",
    # Data models
    "AxiomInputs",
    "SystemState",
    "IntelligenceSnapshot",
]
