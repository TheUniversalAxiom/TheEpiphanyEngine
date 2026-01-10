"""
Basic state models for EPIPHANY.

Provides:
- SystemState (dataclass)
- AxiomInputs (dataclass)
- IntelligenceSnapshot (dataclass)

If pydantic is available it will also expose Pydantic equivalents for validation/serialization.
"""
import json
from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional

try:
    from pydantic import BaseModel  # type: ignore
except Exception:
    BaseModel = None  # pydantic optional


@dataclass
class AxiomInputs:
    """
    Inputs for the Universal Axiom.

    A: Impulses
    B: Elements
    C: Pressure
    X: Axiomatic Subjectivity Scale
    Y: Why Axis
    Z: TimeSphere
    E_n: Exponential Growth
    F_n: Fibonacci Sequence
    """

    A: float
    B: float
    C: float
    X: float
    Y: float
    Z: float
    E_n: float
    F_n: float

    def to_dict(self) -> Dict[str, float]:
        return asdict(self)


@dataclass
class IntelligenceSnapshot:
    step: int
    score: float
    components: Optional[Dict[str, float]] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SystemState:
    step: int
    inputs: AxiomInputs
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "step": self.step,
            "inputs": self.inputs.to_dict(),
            "metadata": self.metadata or {},
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


# Optional Pydantic models for stricter validation / nicer serialization if pydantic present
if BaseModel is not None:

    class AxiomInputsModel(BaseModel):
        A: float
        B: float
        C: float
        X: float
        Y: float
        Z: float
        E_n: float
        F_n: float

    class IntelligenceSnapshotModel(BaseModel):
        step: int
        score: float
        components: Optional[Dict[str, float]] = None

    class SystemStateModel(BaseModel):
        step: int
        inputs: AxiomInputsModel
        metadata: Optional[Dict[str, Any]] = None
