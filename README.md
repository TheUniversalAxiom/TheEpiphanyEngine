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
  - Derives X from observation signals (noise, emotion, bias)
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

- **Tests** (`tests/`)
  - Comprehensive unit tests for core equation
  - TimeSphere simulation validation
  - All tests passing ✅

### 🚧 Planned

- Hooks for integrating with reasoning models (e.g., OpenAI o1-style flows)
- Jupyter notebooks for exploration and teaching
- Visualization tools for intelligence trajectories
- More real-world scenarios and case studies

## Status

🎯 **Active development** - Core functionality complete, examples working, tests passing.

Project Intelligence Score: **3.20** (increased 5453% through axiom-guided development!)

## Getting started

### Quick Start

```bash
# Run all examples
python examples/run_all.py

# Run all tests
python tests/run_all_tests.py

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
