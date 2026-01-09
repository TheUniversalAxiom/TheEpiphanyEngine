from pathlib import Path
from typing import List, Dict, Any

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from engine.state import AxiomInputs
from engine.timesphere import TimeSphere


class SimulationRequest(BaseModel):
    A: float = Field(..., ge=0.0, le=1.0)
    B: float = Field(..., ge=0.0, le=1.0)
    C: float = Field(..., ge=0.0, le=1.0)
    X: float = Field(..., ge=0.0, le=1.0)
    Y: float = Field(..., ge=0.0, le=1.0)
    Z: float = Field(..., ge=0.0, le=1.0)
    E_n: float = Field(..., ge=0.0)
    F_n: float = Field(...)
    steps: int = Field(10, ge=1, le=250)


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
    sphere = TimeSphere(initial_inputs=inputs)
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
