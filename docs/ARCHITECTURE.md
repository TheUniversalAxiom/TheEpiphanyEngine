# Architecture Documentation: The Epiphany Engine

**Version:** 0.1.0
**Last Updated:** 2026-01-10
**Status:** Production Ready

---

## Table of Contents

1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Core Components](#core-components)
4. [Design Patterns](#design-patterns)
5. [Data Flow](#data-flow)
6. [Extension System](#extension-system)
7. [Security Architecture](#security-architecture)
8. [Caching Strategy](#caching-strategy)
9. [Technology Stack](#technology-stack)
10. [Deployment Architecture](#deployment-architecture)

---

## Overview

The Epiphany Engine is a production-ready Python application implementing "The Universal Axiom Organic Intelligence Model" - a physics-style framework for modeling intelligence evolution over time.

### Core Equation

```
Intelligence_n = E_n × (1 + F_n) × X × Y × Z × (A × B × C)
```

Where:
- **A, B, C**: Core system parameters (0-1 normalized)
- **X, Y, Z**: Environmental/contextual factors (0-1 normalized)
- **E_n**: Energy/effort at step n (≥0, can grow)
- **F_n**: Feedback/adaptation at step n (≥-1, typically from Fibonacci)

### Key Principles

1. **Intelligence as Process**: Model intelligence as dynamic evolution over discrete time steps
2. **Composable Factors**: Break down intelligence into measurable, adjustable components
3. **Extensibility**: Plugin architecture for domain-specific customization
4. **Type Safety**: Comprehensive type hints and mypy enforcement
5. **Production Ready**: Security headers, rate limiting, authentication, caching

---

## System Architecture

### High-Level Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                     THE EPIPHANY ENGINE                       │
└──────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
              ┌─────▼──────┐      ┌────▼─────┐
              │  REST API  │      │   CLI    │
              │  (FastAPI) │      │  Tools   │
              └─────┬──────┘      └────┬─────┘
                    │                   │
                    └─────────┬─────────┘
                              │
         ┌────────────────────┼────────────────────┐
         │                    │                    │
    ┌────▼─────┐       ┌─────▼──────┐      ┌─────▼──────┐
    │  Axiom   │       │   Engine   │      │ Extensions │
    │  (Core)  │       │ (TimeSphere)│      │  (Plugins) │
    └──────────┘       └────────────┘      └────────────┘
         │                    │                    │
         │              ┌─────▼──────┐            │
         │              │   State    │            │
         │              │ Management │            │
         │              └────────────┘            │
         │                                        │
         └─────────┬──────────────────────────────┘
                   │
            ┌──────▼────────┐
            │  Visualization │
            │   (Optional)   │
            └────────────────┘
```

### Layer Architecture

```
┌───────────────────────────────────────────────────────────┐
│ PRESENTATION LAYER                                        │
│  - REST API Endpoints                                     │
│  - Request/Response Schemas (Pydantic)                    │
│  - Authentication & Rate Limiting                         │
└───────────────────────────────────────────────────────────┘
                          │
┌───────────────────────────────────────────────────────────┐
│ BUSINESS LOGIC LAYER                                      │
│  - TimeSphere Simulation Engine                           │
│  - Update Rules & Event Handlers                          │
│  - Extension Registry & Loader                            │
└───────────────────────────────────────────────────────────┘
                          │
┌───────────────────────────────────────────────────────────┐
│ DOMAIN LAYER                                              │
│  - Core Axiom Mathematics                                 │
│  - Subjectivity Scale Calculations                        │
│  - State Models (Immutable Dataclasses)                   │
└───────────────────────────────────────────────────────────┘
                          │
┌───────────────────────────────────────────────────────────┐
│ INFRASTRUCTURE LAYER                                      │
│  - Caching (LRU + Optional Redis)                         │
│  - Logging (JSON Structured)                              │
│  - Security Middleware                                    │
└───────────────────────────────────────────────────────────┘
```

---

## Core Components

### 1. Axiom Module (`axiom/`)

**Purpose:** Core mathematical framework for intelligence computation

#### core_equation.py

```python
def compute_intelligence(
    A, B, C, X, Y, Z, E_n, F_n,
    *,
    validate: bool = True,
    clamp_to_unit: bool = True,
    return_components: bool = False
) -> Union[float, Tuple[float, Dict[str, float]]]
```

**Features:**
- Validates numeric inputs and finite values
- Clamps values to safe ranges (A-F to [0,1], E_n/Z ≥ 0, F_n ≥ -1)
- Returns either score only or (score, components dict)
- Symbolic differentiation support (via sympy)
- E_n and F_n sequence generators

**Type Safety:**
- Comprehensive type hints
- Runtime validation for numeric types
- Proper handling of edge cases (infinity, NaN)

#### subjectivity_scale.py

```python
def subjectivity_from_signals(
    noise_level: float,
    emotional_bias: float,
    cognitive_bias: float,
    weights: Optional[dict] = None
) -> SubjectivityMeasurement
```

**Features:**
- 7-tier objectivity/subjectivity scale
- Weighted signal combination
- Configurable thresholds and labels
- Maps signals to X value (0-1 normalized)

---

### 2. Engine Module (`engine/`)

**Purpose:** Time-based simulation engine for intelligence evolution

#### timesphere.py

```python
class TimeSphere:
    def __init__(
        self,
        initial_inputs: AxiomInputs,
        update_rules: Optional[Dict[str, UpdateRule]] = None
    ):
        ...

    def step(self, step_num: int) -> TimeStep:
        """Execute single simulation step"""

    def simulate(self, steps: int) -> SimulationResult:
        """Run full simulation with history tracking"""
```

**Architecture:**

```
┌─────────────────────────────────────────────────────────┐
│                      TimeSphere                         │
├─────────────────────────────────────────────────────────┤
│  State:                                                 │
│   - initial_state: SystemState                          │
│   - update_rules: Dict[str, UpdateRule]                 │
│   - event_handlers: List[EventHandler]                  │
│                                                         │
│  Methods:                                               │
│   - step(n) → TimeStep                                  │
│   - simulate(steps) → SimulationResult                  │
│   - add_update_rule(var, rule)                          │
│   - detect_events(history) → List[Event]               │
│   - analyze_trends(history) → TrendAnalysis             │
└─────────────────────────────────────────────────────────┘
                        │
           ┌────────────┴────────────┐
           │                         │
    ┌──────▼──────┐          ┌──────▼──────┐
    │   State     │          │   Update    │
    │ Management  │          │    Rules    │
    └─────────────┘          └─────────────┘
```

**Features:**
- Discrete time-step simulation
- Pluggable update rules for all variables
- Event detection (thresholds, milestones)
- Trend analysis (acceleration, deceleration, inflection points)
- Pre-built update rules (growth, decay, oscillation, sigmoid)

**Design Decisions:**
- Immutable state objects (SystemState, IntelligenceSnapshot)
- Functional update rules (state → float)
- History tracking for analysis and visualization

#### state.py

```python
@dataclass(frozen=True)
class AxiomInputs:
    """Immutable axiom input values"""
    A: float
    B: float
    C: float
    X: float
    Y: float
    Z: float
    E_n: float
    F_n: float

@dataclass(frozen=True)
class SystemState:
    """Complete system state at a point in time"""
    step: int
    inputs: AxiomInputs
    metadata: Optional[Dict[str, Any]] = None

@dataclass(frozen=True)
class IntelligenceSnapshot:
    """Intelligence score and components at a step"""
    step: int
    score: float
    components: Dict[str, float]
```

**Design Rationale:**
- **Immutability**: `frozen=True` prevents accidental state mutation
- **Type Safety**: Enforced via dataclasses and type hints
- **Serialization**: Built-in `to_dict()` methods for JSON export

---

### 3. Web Module (`web/`)

**Purpose:** FastAPI REST API with security, caching, and logging

#### api.py

```python
app = FastAPI(
    title="Epiphany Engine API",
    version="0.1.0",
    description="Universal Axiom Intelligence Model API"
)

# Main endpoints:
POST   /api/v1/simulate         # Run simulation
GET    /api/v1/presets          # List preset scenarios
POST   /api/v1/presets/{name}   # Run preset scenario
GET    /health                  # Health check
GET    /info                    # API information
```

**Features:**
- Pydantic request/response validation
- Rate limiting (20 req/min for simulate)
- Optional authentication (API key + JWT)
- Comprehensive error handling
- OpenAPI/Swagger documentation

#### Architecture Diagram:

```
┌──────────────┐
│   Request    │
└──────┬───────┘
       │
       ▼
┌──────────────────────────────────────┐
│  Security Middleware                 │
│  - CORS                              │
│  - Security Headers (7 headers)      │
│  - Rate Limiting (slowapi)           │
└──────┬───────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│  Authentication (Optional)           │
│  - API Key Validation                │
│  - JWT Token Verification            │
└──────┬───────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│  Request Validation                  │
│  - Pydantic Models                   │
│  - Input Bounds Checking             │
└──────┬───────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│  Cache Check                         │
│  - SHA256 key generation             │
│  - LRU cache lookup                  │
└──────┬───────────────────────────────┘
       │
       ▼ (cache miss)
┌──────────────────────────────────────┐
│  Business Logic                      │
│  - TimeSphere simulation             │
│  - Result processing                 │
└──────┬───────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│  Cache Store                         │
│  - Store with TTL                    │
└──────┬───────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│  Response Serialization              │
│  - Pydantic Response Models          │
│  - JSON encoding                     │
└──────┬───────────────────────────────┘
       │
       ▼
┌──────────────┐
│   Response   │
└──────────────┘
```

#### security.py

**7 Security Headers Implemented:**

```python
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Content-Security-Policy: default-src 'self'; ...
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), microphone=(), ...
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

#### cache.py

```python
_simulation_cache: TTLCache = TTLCache(maxsize=1000, ttl=3600)

def cache_simulation(
    inputs: Dict,
    steps: int,
    result: Any,
    ttl: Optional[int] = None
) -> None:
    """Cache simulation result with SHA256 key"""
```

**Caching Strategy:**
- In-memory LRU cache with TTL (1 hour default)
- SHA256 hash of sorted parameters as cache key
- Cached Fibonacci and E_n sequences
- Production: Redis recommended for multi-worker deployments

---

### 4. Extensions Module (`extensions/`)

**Purpose:** Plugin architecture for domain-specific customization

#### Architecture:

```
┌────────────────────────────────────────────────────────┐
│                  BaseExtension (ABC)                   │
├────────────────────────────────────────────────────────┤
│  - name: str                                           │
│  - version: str                                        │
│  - enabled: bool                                       │
│                                                        │
│  Abstract Methods:                                     │
│  - initialize() → None                                 │
│  - get_metadata() → Dict[str, Any]                     │
└────────────────┬───────────────────────────────────────┘
                 │
        ┌────────┴─────────┬──────────────┬──────────────┐
        │                  │              │              │
┌───────▼────────┐  ┌──────▼──────┐ ┌────▼─────┐  ┌────▼─────┐
│ UpdateRule     │  │ EventHandler│ │Integration│  │  Domain  │
│   Extension    │  │  Extension  │ │ Extension │  │  Model   │
└────────────────┘  └─────────────┘ └───────────┘  └──────────┘
```

#### Extension Types:

1. **UpdateRuleExtension**: Custom state evolution logic
   - `get_update_rules() → Dict[str, Callable]`
   - `get_rule_descriptions() → Dict[str, str]`

2. **EventHandlerExtension**: React to simulation events
   - `get_event_handlers() → Dict[str, Callable]`
   - `get_event_types() → Dict[str, str]`

3. **IntegrationExtension**: External system connections
   - Custom integration methods

4. **DomainModelExtension**: Domain-specific models
   - Custom domain logic

#### Extension Registry:

```python
class ExtensionRegistry:
    def register(self, extension: BaseExtension) -> None:
        """Register extension"""

    def load(self, name: str) -> BaseExtension:
        """Load extension by name"""

    def discover(self, path: str) -> List[BaseExtension]:
        """Auto-discover extensions in path"""
```

**Design Pattern:** **Factory + Registry**
- Factory pattern for extension creation
- Registry pattern for discovery and management
- Lazy loading for performance

---

## Design Patterns

### 1. Strategy Pattern (Update Rules)

```python
# Define update strategy
def exponential_growth(state: SystemState, step: int) -> float:
    return state.inputs.A * 1.05  # 5% growth per step

# Inject strategy
sphere = TimeSphere(initial_inputs=inputs)
sphere.add_update_rule("A", exponential_growth)
```

**Benefits:**
- Interchangeable update logic
- Easy to test individual strategies
- Runtime configuration

### 2. Immutable Data Pattern (State)

```python
@dataclass(frozen=True)
class SystemState:
    step: int
    inputs: AxiomInputs
    metadata: Optional[Dict[str, Any]] = None
```

**Benefits:**
- Thread-safe
- Predictable behavior
- Cacheable
- Time-travel debugging (history tracking)

### 3. Middleware Pattern (Web Security)

```python
@app.middleware("http")
async def security_headers_middleware(request: Request, call_next):
    response = await call_next(request)
    # Add security headers
    return response
```

**Benefits:**
- Separation of concerns
- Reusable across endpoints
- Easy to test and configure

### 4. Factory Pattern (Extension Loading)

```python
class ExtensionLoader:
    @staticmethod
    def load_from_module(module_path: str) -> BaseExtension:
        """Factory method for extension creation"""
```

**Benefits:**
- Centralized object creation
- Flexible configuration
- Dependency injection

### 5. Repository Pattern (Extension Registry)

```python
class ExtensionRegistry:
    _extensions: Dict[str, BaseExtension] = {}

    def register(self, extension: BaseExtension) -> None:
        self._extensions[extension.name] = extension
```

**Benefits:**
- Abstraction over data storage
- Easy to swap implementations
- Testable

---

## Data Flow

### Simulation Request Flow

```
┌──────────┐
│  Client  │
└────┬─────┘
     │ POST /api/v1/simulate
     │ {inputs, steps, update_rules}
     ▼
┌──────────────────┐
│  FastAPI Handler │
└────┬─────────────┘
     │ 1. Validate request (Pydantic)
     ▼
┌──────────────────┐
│  Cache Lookup    │  Generate SHA256 key
└────┬─────────────┘  Check TTLCache
     │
     ├─ HIT → Return cached result
     │
     └─ MISS ▼
┌───────────────────────────────┐
│  TimeSphere Initialization    │
│  - Create initial SystemState │
│  - Setup update rules         │
└────┬──────────────────────────┘
     │
     ▼
┌───────────────────────────────┐
│  Simulation Loop (N steps)    │
│  for step in range(steps):    │
│    1. Apply update rules      │
│    2. Compute intelligence    │
│    3. Create new state        │
│    4. Detect events           │
│    5. Track history           │
└────┬──────────────────────────┘
     │
     ▼
┌───────────────────────────────┐
│  Post-Processing              │
│  - Trend analysis             │
│  - Event aggregation          │
│  - Statistics                 │
└────┬──────────────────────────┘
     │
     ▼
┌───────────────────────────────┐
│  Cache Store                  │
│  - Store with TTL             │
└────┬──────────────────────────┘
     │
     ▼
┌───────────────────────────────┐
│  Response Serialization       │
│  - Convert to JSON            │
│  - Add metadata               │
└────┬──────────────────────────┘
     │
     ▼
┌──────────┐
│  Client  │  Receives SimulationResponse
└──────────┘
```

### State Update Cycle

```
Current State (step n)
        │
        ▼
┌────────────────────┐
│  Apply Update      │
│  Rules             │
│  - For each var:   │
│    new_val =       │
│    rule(state, n)  │
└────────┬───────────┘
         │
         ▼
┌────────────────────┐
│  Create New        │
│  AxiomInputs       │
│  with updated      │
│  values            │
└────────┬───────────┘
         │
         ▼
┌────────────────────┐
│  Compute           │
│  Intelligence      │
│  score, components │
└────────┬───────────┘
         │
         ▼
┌────────────────────┐
│  Create New        │
│  SystemState       │
│  (step n+1)        │
└────────┬───────────┘
         │
         ▼
Next State (step n+1)
```

---

## Extension System

### Extension Lifecycle

```
1. DISCOVERY
   └─ Scan extension directories
   └─ Find Python modules with BaseExtension subclasses

2. REGISTRATION
   └─ Register extension in ExtensionRegistry
   └─ Validate required methods implemented

3. INITIALIZATION
   └─ Call extension.initialize()
   └─ Load configuration
   └─ Setup resources

4. USAGE
   └─ Application calls extension methods
   └─ Extension executes custom logic

5. CLEANUP (optional)
   └─ Release resources
   └─ Save state if needed
```

### Creating a Custom Extension

**Example: Economic Forecasting Extension**

```python
from extensions.base import UpdateRuleExtension
from typing import Callable, Dict

class EconomicForecastExtension(UpdateRuleExtension):
    def __init__(self, gdp_growth: float, inflation: float):
        super().__init__(name="economic_forecast")
        self.gdp_growth = gdp_growth
        self.inflation = inflation

    def initialize(self) -> None:
        # Load economic data, train models, etc.
        pass

    def get_update_rules(self) -> Dict[str, Callable]:
        return {
            "A": self._economic_capacity_update,
            "E_n": self._energy_investment_update
        }

    def get_rule_descriptions(self) -> Dict[str, str]:
        return {
            "A": f"Economic capacity with {self.gdp_growth}% GDP growth",
            "E_n": f"Energy investment adjusted for {self.inflation}% inflation"
        }

    def _economic_capacity_update(self, state: SystemState, step: int) -> float:
        # Custom economic model logic
        current_a = state.inputs.A
        adjusted_growth = self.gdp_growth / 100
        return current_a * (1 + adjusted_growth)

    def _energy_investment_update(self, state: SystemState, step: int) -> float:
        # Energy investment logic
        current_e = state.inputs.E_n
        inflation_adjustment = 1 - (self.inflation / 100)
        return current_e * inflation_adjustment + step * 0.1

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "name": "EconomicForecastExtension",
            "version": "1.0.0",
            "gdp_growth": self.gdp_growth,
            "inflation": self.inflation
        }
```

**Usage:**

```python
from engine.timesphere import TimeSphere
from extensions.economic_forecast import EconomicForecastExtension

# Create extension
econ_ext = EconomicForecastExtension(gdp_growth=2.5, inflation=3.0)

# Get update rules
update_rules = econ_ext.get_update_rules()

# Use in simulation
sphere = TimeSphere(initial_inputs=inputs, update_rules=update_rules)
result = sphere.simulate(steps=100)
```

---

## Security Architecture

### Defense in Depth

```
Layer 1: Network (Reverse Proxy)
├─ Rate limiting (Nginx/Cloudflare)
├─ DDoS protection
└─ SSL/TLS termination

Layer 2: HTTP Security Headers
├─ X-Content-Type-Options: nosniff
├─ X-Frame-Options: DENY
├─ X-XSS-Protection: 1; mode=block
├─ Content-Security-Policy
├─ Referrer-Policy
├─ Permissions-Policy
└─ Strict-Transport-Security

Layer 3: Application Rate Limiting
├─ slowapi: 100 req/hour globally
└─ Endpoint-specific: 20 req/min for /simulate

Layer 4: Authentication (Optional)
├─ API Key validation (X-API-Key header)
└─ JWT token verification (Bearer token)

Layer 5: Input Validation
├─ Pydantic schema validation
├─ Type checking
└─ Bounds validation (0-1 for normalized values)

Layer 6: Business Logic Security
├─ Immutable state objects
├─ No eval() or exec()
└─ Safe mathematical operations
```

### Authentication Flow (When Enabled)

```
┌──────────┐
│  Client  │
└────┬─────┘
     │ 1. POST /api/v1/auth/login
     │    {username, password}
     ▼
┌──────────────────┐
│  Auth Endpoint   │
└────┬─────────────┘
     │ 2. Verify credentials
     │    (bcrypt password check)
     ▼
┌──────────────────┐
│  JWT Generation  │  create_access_token()
└────┬─────────────┘
     │ 3. Return JWT
     │    {access_token, token_type}
     ▼
┌──────────┐
│  Client  │  Stores token
└────┬─────┘
     │ 4. Subsequent requests
     │    Authorization: Bearer <token>
     ▼
┌──────────────────┐
│  Verify Token    │  verify_token()
└────┬─────────────┘
     │ 5. Decode and validate
     │    - Check signature
     │    - Check expiration
     │    - Extract user data
     ▼
┌──────────────────┐
│  Request Handler │  Process with authenticated context
└──────────────────┘
```

---

## Caching Strategy

### Cache Hierarchy

```
Level 1: LRU Cache (functools.lru_cache)
├─ cached_fibonacci(n)  [1024 entries]
└─ cached_e_sequence(n) [64 entries]

Level 2: TTL Cache (cachetools.TTLCache)
├─ Simulation results   [1000 entries, 1 hour TTL]
└─ SHA256 key generation

Level 3: Redis (Production Multi-Worker)
├─ Shared across workers
├─ Configurable TTL
└─ Persistence support
```

### Cache Key Generation

```python
def generate_cache_key(inputs: Dict, steps: int) -> str:
    """
    Generate deterministic cache key from parameters.

    Process:
    1. Sort dictionary keys (for determinism)
    2. Serialize to JSON string
    3. Hash with SHA256
    4. Return hex digest
    """
    sorted_params = {k: inputs[k] for k in sorted(inputs.keys())}
    serialized = json.dumps(sorted_params, sort_keys=True)
    serialized += f"|steps={steps}"
    return hashlib.sha256(serialized.encode()).hexdigest()
```

### Cache Invalidation Strategy

**Current (Development):**
- TTL-based expiration (1 hour)
- LRU eviction when capacity reached

**Production Recommendations:**
- Redis with configurable TTL
- Explicit invalidation on data updates
- Cache warming for common scenarios
- Monitoring for hit/miss rates

---

## Technology Stack

### Core Dependencies

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.9+ | Core language |
| FastAPI | 0.104+ | REST API framework |
| Uvicorn | 0.24+ | ASGI server |
| Pydantic | 2.0+ | Data validation |
| NumPy | 1.24+ | Numerical computing (optional) |
| Matplotlib | 3.7+ | Visualization (optional) |

### Security & Performance

| Technology | Version | Purpose |
|------------|---------|---------|
| slowapi | 0.1.9+ | Rate limiting |
| python-jose | 3.3+ | JWT handling |
| passlib | 1.7.4+ | Password hashing (bcrypt) |
| cachetools | - | TTL caching |

### Development & Quality

| Technology | Version | Purpose |
|------------|---------|---------|
| pytest | 7.4+ | Testing framework |
| pytest-cov | 4.1+ | Coverage reporting |
| mypy | 1.5+ | Static type checking |
| black | 23.0+ | Code formatting |
| ruff | 0.1+ | Fast linting |
| pre-commit | 3.5+ | Git hooks |

---

## Deployment Architecture

### Development Environment

```
┌────────────────────────────────────┐
│  Developer Workstation             │
│                                    │
│  ┌──────────────────────────────┐ │
│  │  Docker Container            │ │
│  │  ┌────────────────────────┐  │ │
│  │  │  Epiphany Engine       │  │ │
│  │  │  - FastAPI             │  │ │
│  │  │  - Uvicorn (reload)    │  │ │
│  │  │  - Hot reload enabled  │  │ │
│  │  └────────────────────────┘  │ │
│  └──────────────────────────────┘ │
│                                    │
│  Volume mounts for live editing    │
└────────────────────────────────────┘
```

### Production (Single Server)

```
┌──────────────────────────────────────────────────────┐
│  Production Server (AWS EC2 / GCP Compute / Azure)   │
│                                                       │
│  ┌─────────────────────────────────────────────────┐ │
│  │  Nginx (Reverse Proxy)                          │ │
│  │  - SSL/TLS termination                          │ │
│  │  - Rate limiting                                │ │
│  │  - Static file serving                          │ │
│  └──────────────┬──────────────────────────────────┘ │
│                 │                                     │
│  ┌──────────────▼──────────────────────────────────┐ │
│  │  Gunicorn (Process Manager)                     │ │
│  │  - 4 worker processes                           │ │
│  │  - Graceful reload                              │ │
│  └──────────────┬──────────────────────────────────┘ │
│                 │                                     │
│  ┌──────────────▼──────────────────────────────────┐ │
│  │  Epiphany Engine (FastAPI + Uvicorn)           │ │
│  │  - Worker 1                                     │ │
│  │  - Worker 2                                     │ │
│  │  - Worker 3                                     │ │
│  │  - Worker 4                                     │ │
│  └──────────────┬──────────────────────────────────┘ │
│                 │                                     │
│  ┌──────────────▼──────────────────────────────────┐ │
│  │  Redis (Optional)                               │ │
│  │  - Shared cache across workers                  │ │
│  └─────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────┘
```

### Production (Kubernetes)

```
┌────────────────────────────────────────────────────────┐
│  Kubernetes Cluster                                    │
│                                                        │
│  ┌────────────────────────────────────────────────┐   │
│  │  Ingress (nginx-ingress)                       │   │
│  │  - SSL/TLS termination                         │   │
│  │  - Load balancing                              │   │
│  └──────────────┬─────────────────────────────────┘   │
│                 │                                      │
│  ┌──────────────▼─────────────────────────────────┐   │
│  │  Service (epiphany-engine-service)             │   │
│  │  - Type: ClusterIP                             │   │
│  │  - Port: 8000                                  │   │
│  └──────────────┬─────────────────────────────────┘   │
│                 │                                      │
│  ┌──────────────▼─────────────────────────────────┐   │
│  │  Deployment (epiphany-engine)                  │   │
│  │  - Replicas: 3                                 │   │
│  │  - Resource limits: CPU/Memory                 │   │
│  │  - Liveness/Readiness probes                   │   │
│  │  - Rolling update strategy                     │   │
│  │                                                │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐    │   │
│  │  │  Pod 1   │  │  Pod 2   │  │  Pod 3   │    │   │
│  │  │ Epiphany │  │ Epiphany │  │ Epiphany │    │   │
│  │  │  Engine  │  │  Engine  │  │  Engine  │    │   │
│  │  └──────────┘  └──────────┘  └──────────┘    │   │
│  └────────────┬───────────────────────────────────┘   │
│               │                                        │
│  ┌────────────▼───────────────────────────────────┐   │
│  │  StatefulSet (redis)                           │   │
│  │  - Persistent volume for cache                 │   │
│  │  - Single master (optional: Redis Cluster)     │   │
│  └────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────┘
```

### Scaling Considerations

1. **Horizontal Scaling**: Add more Kubernetes pods or server instances
2. **Vertical Scaling**: Increase CPU/memory per instance
3. **Caching**: Redis for shared cache across workers
4. **Database**: If persistence needed, add PostgreSQL/MongoDB
5. **Async Processing**: Celery + RabbitMQ for long-running simulations
6. **CDN**: CloudFlare/CloudFront for static assets
7. **Monitoring**: Prometheus + Grafana for metrics

---

## Appendix: File Structure

```
TheEpiphanyEngine/
├── axiom/                  # Core mathematics
│   ├── core_equation.py
│   └── subjectivity_scale.py
├── engine/                 # Simulation engine
│   ├── state.py
│   └── timesphere.py
├── web/                    # REST API
│   ├── api.py
│   ├── auth.py
│   ├── security.py
│   ├── cache.py
│   └── logging_config.py
├── extensions/             # Plugin system
│   ├── base.py
│   ├── registry.py
│   ├── loader.py
│   └── examples/
│       ├── momentum_update_rule.py
│       └── threshold_alert.py
├── mcp/                    # Model Context Protocol
│   └── server.py
├── tests/                  # Test suite (1,496 lines)
│   ├── test_core_equation.py
│   ├── test_timesphere.py
│   ├── test_api.py (27 tests)
│   ├── test_validation.py
│   ├── test_examples.py
│   └── run_all_tests.py
├── examples/               # Usage examples
│   ├── basic_simulation.py
│   ├── custom_update_rules.py
│   ├── event_handling.py
│   ├── subjectivity_analysis.py
│   ├── visualization_demo.py
│   └── extension_demo.py
├── docs/                   # Documentation
│   ├── API_REFERENCE.md
│   ├── ARCHITECTURE.md (this file)
│   └── ...
├── viz/                    # Visualization utilities
│   └── plotter.py
├── benchmarks/             # Performance benchmarks
├── notebooks/              # Jupyter notebooks
├── Dockerfile              # Multi-stage production build
├── docker-compose.yml      # Development environment
├── pyproject.toml          # Project configuration
├── requirements.txt        # Python dependencies
├── .github/workflows/ci.yml # CI/CD pipeline
└── .pre-commit-config.yaml # Pre-commit hooks
```

---

## Further Reading

- **[API_REFERENCE.md](API_REFERENCE.md)**: Complete API endpoint documentation
- **[DEPLOYMENT.md](DEPLOYMENT.md)**: Production deployment guide
- **[SECURITY.md](SECURITY.md)**: Security best practices and policies
- **[CONTRIBUTING.md](CONTRIBUTING.md)**: Contribution guidelines
- **README.md**: Quick start and feature overview

---

**Document Status:** Living document - updated as architecture evolves
**Next Review:** 2026-04-10 (quarterly)
**Maintainer:** TheUniversalAxiom Team
