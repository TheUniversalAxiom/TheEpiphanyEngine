from pathlib import Path
from typing import List, Dict, Any

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from engine.state import AxiomInputs
from engine.timesphere import TimeSphere


class SimulationRequest(BaseModel):
    A: float = Field(...)
    B: float = Field(...)
    C: float = Field(...)
    X: float = Field(...)
    Y: float = Field(...)
    Z: float = Field(...)
    E_n: float = Field(...)
    F_n: float = Field(...)
    steps: int = Field(10, ge=1, le=250)
    strict: bool = Field(False, description="Reject out-of-bounds inputs instead of clamping.")


class SimulationResponse(BaseModel):
    steps: List[Dict[str, Any]]
    summary: Dict[str, Any]
    intelligence_history: List[float]


app = FastAPI(title="Epiphany Engine API")


@app.post("/api/simulate", response_model=SimulationResponse)
def simulate(request: SimulationRequest) -> SimulationResponse:
    inputs = AxiomInputs(
        A=request.A,
        B=request.B,
        C=request.C,
        X=request.X,
        Y=request.Y,
        Z=request.Z,
        E_n=request.E_n,
        F_n=request.F_n,
    )
    if request.strict:
        errors = []
        for key in ("A", "B", "C", "X", "Y"):
            value = getattr(inputs, key)
            if not 0.0 <= value <= 1.0:
                errors.append(f"{key}={value} not in [0, 1]")
        if inputs.Z < 0.0:
            errors.append(f"Z={inputs.Z} must be >= 0")
        if inputs.E_n < 0.0:
            errors.append(f"E_n={inputs.E_n} must be >= 0")
        if inputs.F_n < -1.0:
            errors.append(f"F_n={inputs.F_n} must be >= -1")
        if errors:
            raise HTTPException(
                status_code=422,
                detail={"message": "Strict mode rejected out-of-bounds inputs.", "errors": errors},
            )
    sphere = TimeSphere(initial_inputs=inputs, clamp_to_unit=not request.strict)
    result = sphere.simulate(steps=request.steps)
    payload = result.to_dict()
    return SimulationResponse(
        steps=payload["steps"],
        summary=payload["summary"],
        intelligence_history=result.intelligence_history(),
    )


static_dir = Path(__file__).resolve().parent / "static"
if static_dir.exists():
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
