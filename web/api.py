import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from engine.state import AxiomInputs
from engine.timesphere import TimeSphere, UpdateRules
from web.auth import AuthConfig, verify_api_key
from web.logging_config import LogContext, get_logger, setup_logging

# Setup structured logging
setup_logging()
logger = get_logger(__name__)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address, default_limits=["100/hour"])

# CORS configuration from environment
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "").strip()
if CORS_ORIGINS:
    # Split comma-separated origins and remove whitespace
    ALLOWED_ORIGINS = [origin.strip() for origin in CORS_ORIGINS.split(",") if origin.strip()]
else:
    # Default to localhost for development
    ALLOWED_ORIGINS = ["http://localhost:8000", "http://localhost:3000"]
    logger.warning(
        "CORS_ORIGINS not set, using default localhost origins. "
        "Set CORS_ORIGINS environment variable for production."
    )


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
    preset: Optional[str] = Field(None, description="Update-rule preset identifier")


class SimulationResponse(BaseModel):
    steps: List[Dict[str, Any]]
    summary: Dict[str, Any]
    intelligence_history: List[float]
    selected_preset: str
    preset_fallback: bool


app = FastAPI(
    title="Epiphany Engine API",
    version="0.1.0",
    description="Universal Axiom Organic Intelligence Model - REST API",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Add rate limiter to app state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-API-Key"],
)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all HTTP requests with timing information."""
    request_id = str(time.time())
    start_time = time.time()

    with LogContext(request_id=request_id):
        logger.info(
            f"Request started: {request.method} {request.url.path}",
            extra={
                "extra_fields": {
                    "method": request.method,
                    "path": request.url.path,
                    "client": request.client.host if request.client else None,
                }
            },
        )

        try:
            response = await call_next(request)
            duration = time.time() - start_time

            logger.info(
                f"Request completed: {request.method} {request.url.path}",
                extra={
                    "extra_fields": {
                        "method": request.method,
                        "path": request.url.path,
                        "status_code": response.status_code,
                        "duration_ms": round(duration * 1000, 2),
                    }
                },
            )

            return response

        except Exception as e:
            duration = time.time() - start_time
            logger.error(
                f"Request failed: {request.method} {request.url.path}",
                extra={
                    "extra_fields": {
                        "method": request.method,
                        "path": request.url.path,
                        "duration_ms": round(duration * 1000, 2),
                        "error": str(e),
                    }
                },
                exc_info=True,
            )
            raise

PRESET_DEFAULT = "baseline"


@app.get("/")
def root():
    """Root endpoint - redirect to docs."""
    return {
        "message": "Epiphany Engine API",
        "version": "0.1.0",
        "docs": "/api/docs",
        "health": "/api/health",
    }


@app.get("/api/health")
def health_check():
    """
    Health check endpoint for monitoring.

    Returns API status and configuration info.
    """
    return {
        "status": "healthy",
        "service": "epiphany-engine",
        "version": "0.1.0",
        "auth_enabled": AuthConfig.is_enabled(),
    }


@app.get("/api/info")
def get_info():
    """
    Get API information and available presets.

    Returns configuration details and preset options.
    """
    return {
        "name": "Epiphany Engine API",
        "version": "0.1.0",
        "description": "Universal Axiom Organic Intelligence Model",
        "presets": [
            "baseline",
            "basic-growth",
            "corruption-decay",
            "divergent-paths",
            "ai-alignment",
        ],
        "default_preset": PRESET_DEFAULT,
        "rate_limits": {
            "default": "100 requests per hour per IP",
            "simulate": "20 requests per minute per IP",
        },
        "authentication": {
            "enabled": AuthConfig.is_enabled(),
            "method": "API Key (X-API-Key header)" if AuthConfig.is_enabled() else "None",
        },
    }


def apply_preset_rules(
    sphere: TimeSphere,
    preset: str,
    request: SimulationRequest,
) -> Tuple[str, bool]:
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
@limiter.limit("20/minute")
def simulate(
    request: SimulationRequest,
    http_request: Request,
    authenticated: bool = Depends(verify_api_key),
) -> SimulationResponse:
    """
    Run intelligence simulation with given parameters.

    Args:
        request: Simulation parameters (A, B, C, X, Y, Z, E_n, F_n, steps, preset)
        http_request: FastAPI request object (for rate limiting)
        authenticated: Authentication status (from dependency)

    Returns:
        Simulation results with intelligence trajectory

    Raises:
        HTTPException: If parameters are invalid or simulation fails
    """
    try:
        logger.info(
            "Starting simulation",
            extra={
                "extra_fields": {
                    "preset": request.preset or PRESET_DEFAULT,
                    "steps": request.steps,
                }
            },
        )

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

        logger.info(
            "Simulation completed",
            extra={
                "extra_fields": {
                    "preset": selected_preset,
                    "final_intelligence": result.intelligence_history()[-1],
                }
            },
        )

        return SimulationResponse(
            steps=payload["steps"],
            summary=payload["summary"],
            intelligence_history=result.intelligence_history(),
            selected_preset=selected_preset,
            preset_fallback=preset_fallback,
        )

    except ValueError as e:
        logger.error(f"Invalid simulation parameters: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid parameters: {str(e)}",
        )
    except Exception as e:
        logger.error(f"Simulation failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Simulation error: {str(e)}",
        )


static_dir = Path(__file__).resolve().parent / "static"
if static_dir.exists():
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
