# Theoretical Framework - Universal Axiom Prism

## Overview

The EPIPHANY Engine is an implementation of **The Universal Axiom Prism**, a multidimensional framework for analyzing and improving cognitive processes, organizational intelligence, and AI systems.

This document maps the theoretical framework to the codebase implementation.

---

## Core Equation

```
Intelligence_n = E_n · (1 + F_n) · X · Y · Z · (A · B · C)
```

**Implementation:** `compute_intelligence()` in `src/epiphany_engine/axiom/core_equation.py`

---

## Framework Components

### 1. The Foundation (ABC)

#### A - Impulses
**Theory:** Driving forces behind thoughts and actions (positive/negative motivations, desires, fears)

**Implementation:**
- Variable: `A` in `AxiomInputs`
- Semantic: `impulses` in `PrismComponents`
- Helper: `IntrospectivePrism.assess_impulses()`

**Usage:**
```python
from epiphany_engine.prism import IntrospectivePrism

prism = IntrospectivePrism()
impulses_score, breakdown = prism.assess_impulses(
    positive_impulses={"passion": 0.9, "curiosity": 0.8},
    negative_impulses={"fear": 0.6, "anxiety": 0.4}
)
```

#### B - Elements
**Theory:** Resources including energy, matter, state (skills, knowledge, emotional capacity)

**Implementation:**
- Variable: `B` in `AxiomInputs`
- Semantic: `elements` in `PrismComponents`
- Helper: `IntrospectivePrism.assess_elements()`

**Usage:**
```python
elements_score, breakdown = prism.assess_elements(
    skills={"programming": 0.8, "communication": 0.7},
    knowledge={"domain_expertise": 0.9},
    emotional_state={"confidence": 0.7, "resilience": 0.8}
)
```

#### C - Pressure
**Theory:** Direction, momentum, and integrity (constructive/destructive forces)

**Implementation:**
- Variable: `C` in `AxiomInputs`
- Semantic: `pressure` in `PrismComponents`
- Helper: `IntrospectivePrism.assess_pressure()`

**Usage:**
```python
pressure_score, breakdown = prism.assess_pressure(
    constructive={"career_goals": 0.8, "mentorship": 0.7},
    destructive={"workload_stress": 0.6, "fear_of_failure": 0.5}
)
```

---

### 2. The Context (XYZ)

#### X - Axiomatic Subjectivity Scale (Objectivity)
**Theory:** Measures alignment with objective truth (inverse of subjectivity)

**Implementation:**
- Variable: `X` in `AxiomInputs`
- Semantic: `objectivity` in `PrismComponents`
- Function: `x_from_observations()` in `axiom/subjectivity_scale.py`
- Scale: 7-tier classification (apex-objective → apex-subjective)

**Usage:**
```python
from epiphany_engine import x_from_observations, label_x

x = x_from_observations(
    noise=0.3,
    emotional_volatility=0.4,
    bias_indicator=0.2
)
label = label_x(x)  # e.g., "objective", "mid-dynamic", etc.
```

#### Y - Why Axis
**Theory:** Alignment of motivations and reasons with long-term goals

**Formula:** `Y = Y_s / Y_max`

**Implementation:**
- Variable: `Y` in `AxiomInputs`
- Semantic: `why_alignment` in `PrismComponents`
- Helper: `IntrospectivePrism.calculate_why_alignment()`

**Usage:**
```python
why_score = prism.calculate_why_alignment(
    current_score=7.5,   # Current motivational alignment
    maximum_score=10.0   # Perfect alignment
)
# Returns: 0.75
```

#### Z - TimeSphere
**Theory:** Temporal evolution of intelligence (progress over time)

**Implementation:**
- Variable: `Z` in `AxiomInputs`
- Semantic: `time_progress` in `PrismComponents`
- Engine: `TimeSphere` class in `engine/timesphere.py`

**Usage:**
```python
from epiphany_engine import TimeSphere, AxiomInputs

initial = AxiomInputs(A=0.7, B=0.6, C=0.6, X=0.8, Y=0.7, Z=0.5, E_n=3.0, F_n=1.0)
sphere = TimeSphere(initial_inputs=initial)

# Define evolution rules
sphere.add_update_rule("Z", lambda s, step: min(1.0, s.inputs.Z + 0.05))

# Run simulation
result = sphere.simulate(steps=10)
```

---

### 3. Evolution Factors

#### E_n - Exponential Growth
**Theory:** Rapid, compounded expansion

**Formula:** `E_n = 3·E_{n-1} + 2`

**Implementation:**
- Variable: `E_n` in `AxiomInputs`
- Semantic: `energy` in `PrismComponents`
- Function: `e_recurrence(E_prev, a=3.0, b=2.0)` in `axiom/core_equation.py`
- Generator: `e_sequence(initial, steps)` for multiple values

**Usage:**
```python
from epiphany_engine import e_recurrence, e_sequence

# Single step
E_1 = e_recurrence(E_0=1.0, a=3.0, b=2.0)  # = 5.0

# Full sequence
energies = list(e_sequence(initial=1.0, steps=5, a=3.0, b=2.0))
# [1.0, 5.0, 17.0, 53.0, 161.0, 485.0]
```

**Pre-built Update Rule:**
```python
from epiphany_engine import UpdateRules

sphere.add_update_rule("E_n", UpdateRules.e_sequence_rule(a=3.0, b=2.0))
```

#### F_n - Fibonacci Sequence
**Theory:** Balanced, stable growth (natural harmony)

**Formula:** `F_n = F_{n-1} + F_{n-2}` (where F_0=0, F_1=1)

**Implementation:**
- Variable: `F_n` in `AxiomInputs`
- Semantic: `feedback` in `PrismComponents`
- Function: `fibonacci(n)` in `axiom/core_equation.py`
- Generator: `fibonacci_sequence(steps)`

**Usage:**
```python
from epiphany_engine import fibonacci, fibonacci_sequence

# Single value
F_4 = fibonacci(4)  # = 3

# Full sequence
fibs = list(fibonacci_sequence(steps=6))
# [0, 1, 1, 2, 3, 5, 8]
```

**Pre-built Update Rule:**
```python
sphere.add_update_rule("F_n", UpdateRules.fibonacci_rule())
```

---

## Introspective Application

### Semantic Interface

For introspective use (personal development, career analysis, etc.), use the semantic `PrismComponents` interface:

```python
from epiphany_engine.prism import PrismComponents, compute_prism_intelligence

# Define using semantic names
components = PrismComponents(
    impulses=0.8,         # A: Driving forces
    elements=0.7,         # B: Resources/skills
    pressure=0.6,         # C: External/internal pressures
    objectivity=0.8,      # X: Alignment with truth
    why_alignment=0.75,   # Y: Goal alignment
    time_progress=0.5,    # Z: Temporal maturity
    energy=5.0,           # E_n: Current momentum
    feedback=3.0,         # F_n: Feedback loops
)

# Compute intelligence
intelligence = compute_prism_intelligence(components)

# Convert to/from technical representation
axiom_inputs = components.to_axiom_inputs()
prism_comps = PrismComponents.from_axiom_inputs(axiom_inputs)
```

### Introspective Helpers

The `IntrospectivePrism` class provides assessment tools:

```python
from epiphany_engine.prism import IntrospectivePrism

prism = IntrospectivePrism()

# Assess each dimension
impulses_score, details = prism.assess_impulses(
    positive_impulses={"passion": 0.9, "ambition": 0.8},
    negative_impulses={"fear": 0.6}
)

elements_score, details = prism.assess_elements(
    skills={"technical": 0.8},
    knowledge={"domain": 0.9},
    emotional_state={"confidence": 0.7}
)

pressure_score, details = prism.assess_pressure(
    constructive={"goals": 0.8},
    destructive={"stress": 0.6}
)

why_score = prism.calculate_why_alignment(
    current_score=7.5,
    maximum_score=10.0
)
```

---

## Examples

### 1. Theoretical Validation
**File:** `examples/05_theoretical_validation.py`

Reproduces the exact calculation from the Universal Axiom Prism documentation:
- E_4 = 161
- F_4 = 3
- A=0.8, B=0.9, C=0.7
- X=0.625, Y=0.625, Z=0.4
- Result: Intelligence_4 = 50.715

### 2. Career Introspection
**File:** `src/epiphany_engine/prism.py` (example_career_introspection)

Demonstrates introspective application for personal career development analysis.

### 3. TimeSphere Simulations
**Files:** `examples/01_basic_growth.py` through `examples/04_ai_alignment.py`

Show temporal evolution of intelligence through various scenarios.

---

## Complete API Reference

### Core Functions
- `compute_intelligence(A, B, C, X, Y, Z, E_n, F_n)` - Main intelligence computation
- `e_recurrence(E_prev, a, b)` - Single E_n step
- `e_sequence(initial, steps, a, b)` - E_n sequence generator
- `fibonacci(n)` - Single Fibonacci value
- `fibonacci_sequence(steps)` - Fibonacci sequence generator
- `x_from_observations(noise, emotional_volatility, bias_indicator)` - Derive X from signals
- `label_x(x)` - Map X to semantic label

### Classes
- `AxiomInputs` - Technical representation (A, B, C, X, Y, Z, E_n, F_n)
- `PrismComponents` - Semantic representation (impulses, elements, pressure, etc.)
- `TimeSphere` - Simulation engine for temporal evolution
- `UpdateRules` - Pre-built evolution rules
- `IntrospectivePrism` - Introspective assessment tools

### Imports

**Top-level (recommended):**
```python
from epiphany_engine import (
    # Core
    compute_intelligence,
    e_recurrence,
    fibonacci,
    x_from_observations,
    label_x,
    # Classes
    TimeSphere,
    UpdateRules,
    AxiomInputs,
)
```

**Semantic/Introspective:**
```python
from epiphany_engine.prism import (
    PrismComponents,
    IntrospectivePrism,
    compute_prism_intelligence,
)
```

---

## Theoretical to Implementation Mapping

| Theory Concept | Variable | Implementation | Module |
|---------------|----------|----------------|---------|
| Impulses | A | `A` in `AxiomInputs`, `impulses` in `PrismComponents` | `engine.state`, `prism` |
| Elements | B | `B` in `AxiomInputs`, `elements` in `PrismComponents` | `engine.state`, `prism` |
| Pressure | C | `C` in `AxiomInputs`, `pressure` in `PrismComponents` | `engine.state`, `prism` |
| Objectivity Scale | X | `x_from_observations()`, `label_x()` | `axiom.subjectivity_scale` |
| Why Axis | Y | `calculate_why_alignment()` | `prism` |
| TimeSphere | Z | `TimeSphere` class | `engine.timesphere` |
| Exponential Growth | E_n | `e_recurrence()`, `e_sequence()` | `axiom.core_equation` |
| Fibonacci | F_n | `fibonacci()`, `fibonacci_sequence()` | `axiom.core_equation` |
| Core Equation | - | `compute_intelligence()` | `axiom.core_equation` |

---

## Next Steps

1. **Run theoretical validation:**
   ```bash
   python examples/05_theoretical_validation.py
   ```

2. **Try introspective example:**
   ```python
   python -c "from epiphany_engine.prism import example_career_introspection; example_career_introspection()"
   ```

3. **Build custom scenarios** using `TimeSphere` to model your own systems

4. **Explore examples** in `examples/` directory

---

## References

- **Universal Axiom Prism Documentation** - Theoretical foundation
- **Implementation** - `src/epiphany_engine/`
- **Examples** - `examples/`
- **Tests** - `tests/`
