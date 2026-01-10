# The EPIPHANY Engine ⚡️ Quantum AI

> An open-source implementation of **The Universal Axiom Organic Intelligence Model** (“The Axiom”) – a physics-style framework for modeling and evolving intelligence over time.

## What is this?

The EPIPHANY Engine treats intelligence as a dynamic process governed by a core equation:

Intelligence_n = E_n * (1 + F_n) * X * Y * Z * (A * B * C)

This repo turns that conceptual model into:

- A **Python library** for modeling systems using A, B, C, X, Y, Z, Eₙ, Fₙ
- An **engine** for running time-based simulations (“TimeSphere”)
- Tools to **analyze corruption vs coherence** (subjectivity vs alignment)
- Examples and scenarios for humans, organizations, and AI models

## Features

### ✅ Implemented

- **Core Axiom Math** (`axiom/core_equation.py`)
  - Intelligence computation with all variables (A, B, C, X, Y, Z, E_n, F_n)
  - E_n recurrence sequences (linear growth)
  - F_n Fibonacci sequences
  - Component analysis and validation

- **Subjectivity Scale** (`axiom/subjectivity_scale.py`)
  - 7-tier objectivity/subjectivity measurement
  - Derives X from observation signals (linear, shallow, bias)
  - Configurable thresholds and labels

- **TimeSphere Simulation Engine** (`engine/timesphere.py`)
  - Time-based evolution of intelligence over discrete steps
  - Customizable update rules for all variables
  - Event detection and milestone tracking
  - Trend analysis (growth, decay, inflection points)
  - Pre-built update rules (growth, decay, oscillation, etc.)

- **State Management** (`engine/state.py`)
  - Structured data models for system states
  - Intelligence snapshots with component tracking
  - JSON serialization support

- **Example Scenarios** (`examples/`)
  - Basic growth: Learner's journey
  - Corruption & decay: Intelligence collapse
  - Divergent paths: Comparing different strategies
  - AI alignment: Capability vs. values balance
  - Resilience & recovery: Shock response and comeback
  - Innovation cycles: Experimentation leading to breakthroughs

- **Interactive Jupyter Notebooks** (`notebooks/`) 🆕
  - Interactive intelligence exploration with visualizations
  - AI alignment deep dive with scenario comparisons
  - Sensitivity analysis and parameter exploration

- **Advanced Visualization** (`viz/`) 🆕
  - Intelligence trajectory plotting
  - Component evolution tracking
  - Multi-scenario comparisons
  - 2D parameter heatmaps
  - Comprehensive dashboards
  - Professional export capabilities (PNG, PDF)

- **Export & Reporting** (`viz/exporters.py`) 🆕
  - JSON export for data interchange
  - CSV export for spreadsheet analysis
  - Markdown reports with summaries
  - Multi-scenario comparison reports

- **Performance Benchmarks** (`benchmarks/`) 🆕
  - Core computation benchmarking
  - Simulation performance metrics
  - Update rule comparison
  - Comprehensive benchmark suite

- **Extension System** (`extensions/`) 🆕
  - Plugin architecture for custom functionality
  - Custom update rules
  - Domain-specific models
  - Event handler extensions
  - Integration adapters
  - Extension registry and loader

- **Comprehensive Testing** (`tests/`) 🆕
  - Unit tests for core equation
  - TimeSphere simulation validation
  - Edge case and boundary testing
  - Input validation tests
  - All 30+ tests passing ✅

- **Documentation** (`docs/`) 🆕
  - Complete API reference
  - Contributing guidelines
  - Code examples and best practices

- **Web API** (`web/`)
  - FastAPI REST endpoint with OpenAPI docs
  - Interactive web UI
  - Preset scenarios (baseline, growth, decay, alignment, etc.)
  - Real-time visualization
  - **NEW**: Rate limiting (20 req/min per IP)
  - **NEW**: Optional API key authentication
  - **NEW**: Structured JSON logging
  - **NEW**: Health check endpoints
  - **NEW**: CORS and security middleware

- **MCP Integration** (`mcp/`)
  - Model Context Protocol server
  - Tool and resource endpoints

- **Production Ready** 🆕
  - **Docker support** with multi-stage builds
  - **Docker Compose** for easy deployment
  - **GitHub Actions CI/CD** pipeline
  - **Pre-commit hooks** for code quality
  - **Security scanning** with pip-audit
  - **Type checking** with mypy
  - **Linting** with ruff
  - **Code formatting** with black
  - **Comprehensive deployment guide**

- **Example Extensions** (`extensions/examples/`) 🆕
  - Momentum-based update rule
  - Threshold alert event handler
  - Extension development guide

### 🚧 Future Enhancements

- Hooks for integrating with reasoning models (e.g., OpenAI o1-style flows)
- Real-time monitoring dashboards
- Cloud deployment templates
- More domain-specific extensions

## Status

🎯 **Active development** - Core functionality complete, examples working, tests passing.

Project Intelligence Score: **3.20** (increased 5453% through axiom-guided development!)

## Getting started

### Quick Start

```bash
# Run all examples
python examples/run_all.py

# Run all tests
pytest tests/ -v

# Analyze project intelligence
python axiom_analysis.py
```

### Basic Usage

```python
from engine.timesphere import TimeSphere, UpdateRules
from engine.state import AxiomInputs

# Define initial state
initial = AxiomInputs(
    A=0.7,  # Alignment
    B=0.5,  # Behavior
    C=0.6,  # Capacity
    X=0.8,  # Objectivity
    Y=0.4,  # Yield
    Z=0.6,  # Zero-error
    E_n=3.0,  # Energy
    F_n=1.0,  # Feedback
)

# Create simulation
sphere = TimeSphere(initial_inputs=initial)

# Add evolution rules
sphere.add_update_rule("A", lambda s, step: min(1.0, s.inputs.A + 0.05))
sphere.add_update_rule("B", lambda s, step: min(1.0, s.inputs.B + 0.08))
sphere.add_update_rule("E_n", UpdateRules.e_sequence_rule(a=1.2, b=0.5))
sphere.add_update_rule("F_n", lambda s, step: float(step))

# Run simulation
result = sphere.simulate(steps=10)

# Analyze results
print(f"Initial Intelligence: {result.summary['initial_intelligence']:.4f}")
print(f"Final Intelligence: {result.summary['final_intelligence']:.4f}")
print(f"Growth Rate: {result.summary['growth_rate']:.1%}")
```

## MCP Server

Run the Universal Axiom MCP server over stdio:

```bash
python -m mcp.server
```

The server exposes:

- `compute_universal_axiom` tool for computing intelligence scores.
- `axiom://universal/formula` resource for the core equation.

## Deployment

### Docker (Recommended)

**Quick start with Docker Compose:**
```bash
# Build and run
docker-compose up -d

# Access at http://localhost:8000
# API docs at http://localhost:8000/api/docs
```

**Manual Docker build:**
```bash
# Build image
docker build -t epiphany-engine:latest .

# Run container
docker run -p 8000:8000 epiphany-engine:latest
```

### Production Deployment

**With authentication:**
```bash
# Set environment variables
export API_KEY_ENABLED=true
export API_KEY=$(openssl rand -hex 32)
export LOG_LEVEL=INFO

# Run with Gunicorn
gunicorn web.api:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

**Development mode:**
```bash
# Install dependencies
pip install -r requirements.txt

# Run with auto-reload
uvicorn web.api:app --reload
```

### Pre-commit Hooks

Install pre-commit hooks for automatic code quality checks:

```bash
pip install pre-commit
pre-commit install

# Run manually
pre-commit run --all-files
```

**For complete deployment instructions**, see [DEPLOYMENT.md](DEPLOYMENT.md) covering:
- Production setup with Nginx/Gunicorn
- Systemd service configuration
- SSL/TLS setup
- Security hardening
- Monitoring and logging
- Cloud deployment (AWS, GCP, Azure)
- Kubernetes deployment

## The Axiom Explained

The core equation models intelligence as the product of three dimensions:

- **ABC (Foundation)**: A·B·C
  - **A**: Alignment with truth/values
  - **B**: Behaviors and capabilities
  - **C**: Capacity for growth and learning

- **XYZ (Context)**: X·Y·Z
  - **X**: Objectivity (inverse of subjectivity)
  - **Y**: Yield/output quality
  - **Z**: Zero-error (accuracy/correctness)

- **Evolution**: E_n·(1 + F_n)
  - **E_n**: Energy/momentum (grows over time)
  - **F_n**: Feedback loops and iteration

**Key Insight**: Intelligence is multiplicative. A system with high capability (B) but low alignment (A) will have low intelligence. Similarly, high objectivity (X) amplifies everything else.

Intelligence_n = E_n * (1 + F_n) * X * Y * Z * (A * B * C)
