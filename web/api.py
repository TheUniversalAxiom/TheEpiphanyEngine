from pathlib import Path
from typing import List, Dict, Any

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from engine.state import AxiomInputs
from engine.timesphere import TimeSphere, UpdateRules


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
    preset: str | None = Field(None, description="Update-rule preset identifier")


class SimulationResponse(BaseModel):
    steps: List[Dict[str, Any]]
    summary: Dict[str, Any]
    intelligence_history: List[float]
    selected_preset: str
    preset_fallback: bool


app = FastAPI(title="Epiphany Engine API")

PRESET_DEFAULT = "baseline"


def apply_preset_rules(
    sphere: TimeSphere,
    preset: str,
    request: SimulationRequest,
) -> tuple[str, bool]:
    presets = {
        "baseline": lambda: [
            sphere.add_update_rule(var, UpdateRules.constant(getattr(request, var)))
            for var in ("A", "B", "C", "X", "Y", "Z", "E_n", "F_n")
        ],
        "basic-growth": lambda: [
            sphere.add_update_rule("A", UpdateRules.linear_growth(0.02, max_val=1.0, variable="A")),
            sphere.add_update_rule("B", UpdateRules.linear_growth(0.015, max_val=1.0, variable="B")),
            sphere.add_update_rule("C", UpdateRules.linear_growth(0.02, max_val=1.0, variable="C")),
            sphere.add_update_rule("X", UpdateRules.linear_growth(0.015, max_val=1.0, variable="X")),
            sphere.add_update_rule("Y", UpdateRules.oscillate(amplitude=0.1, period=8, baseline=request.Y)),
            sphere.add_update_rule("Z", UpdateRules.linear_growth(0.015, max_val=1.0, variable="Z")),
            sphere.add_update_rule("E_n", UpdateRules.linear_growth(0.25, max_val=10.0, variable="E_n")),
            sphere.add_update_rule("F_n", UpdateRules.fibonacci_rule()),
        ],
        "corruption-decay": lambda: [
            sphere.add_update_rule("A", UpdateRules.decay(0.05, min_val=0.0, variable="A")),
            sphere.add_update_rule("B", UpdateRules.decay(0.05, min_val=0.0, variable="B")),
            sphere.add_update_rule("C", UpdateRules.decay(0.04, min_val=0.0, variable="C")),
            sphere.add_update_rule("X", UpdateRules.decay(0.04, min_val=0.0, variable="X")),
            sphere.add_update_rule("Y", UpdateRules.decay(0.03, min_val=0.0, variable="Y")),
            sphere.add_update_rule("Z", UpdateRules.decay(0.04, min_val=0.0, variable="Z")),
            sphere.add_update_rule("E_n", UpdateRules.decay(0.08, min_val=0.0, variable="E_n")),
            sphere.add_update_rule("F_n", UpdateRules.decay(0.06, min_val=0.0, variable="F_n")),
        ],
        "divergent-paths": lambda: [
            sphere.add_update_rule("A", UpdateRules.linear_growth(0.01, max_val=1.0, variable="A")),
            sphere.add_update_rule("B", UpdateRules.decay(0.01, min_val=0.0, variable="B")),
            sphere.add_update_rule("X", UpdateRules.oscillate(amplitude=0.25, period=6, baseline=request.X)),
            sphere.add_update_rule("Y", UpdateRules.oscillate(amplitude=0.2, period=9, baseline=request.Y)),
            sphere.add_update_rule("Z", UpdateRules.decay(0.015, min_val=0.0, variable="Z")),
            sphere.add_update_rule("E_n", UpdateRules.linear_growth(0.2, max_val=12.0, variable="E_n")),
            sphere.add_update_rule("F_n", UpdateRules.fibonacci_rule()),
        ],
        "ai-alignment": lambda: [
            sphere.add_update_rule("A", UpdateRules.oscillate(amplitude=0.08, period=7, baseline=request.A)),
            sphere.add_update_rule("C", UpdateRules.linear_growth(0.025, max_val=1.0, variable="C")),
            sphere.add_update_rule("X", UpdateRules.linear_growth(0.03, max_val=1.0, variable="X")),
            sphere.add_update_rule("Y", UpdateRules.decay(0.02, min_val=0.0, variable="Y")),
            sphere.add_update_rule("E_n", UpdateRules.e_sequence_rule(a=1.05, b=0.4)),
            sphere.add_update_rule("F_n", UpdateRules.fibonacci_rule()),
        ],
    }

    selected_preset = preset if preset in presets else PRESET_DEFAULT
    preset_fallback = selected_preset != preset
    presets[selected_preset]()
    return selected_preset, preset_fallback


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
    selected_preset, preset_fallback = apply_preset_rules(
        sphere,
        request.preset or PRESET_DEFAULT,
        request,
    )
    result = sphere.simulate(steps=request.steps)
    payload = result.to_dict()
    return SimulationResponse(
        steps=payload["steps"],
        summary=payload["summary"],
        intelligence_history=result.intelligence_history(),
        selected_preset=selected_preset,
        preset_fallback=preset_fallback,
    )


static_dir = Path(__file__).resolve().parent / "static"
if static_dir.exists():
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
