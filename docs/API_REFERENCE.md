# API Reference

Complete API documentation for The EPIPHANY Engine.

## Table of Contents

1. [REST API Endpoints](#rest-api-endpoints)
2. [Core Equation](#core-equation)
3. [Subjectivity Scale](#subjectivity-scale)
4. [TimeSphere Engine](#timesphere-engine)
5. [State Management](#state-management)
6. [Update Rules](#update-rules)
7. [Visualization](#visualization)
8. [Export Utilities](#export-utilities)
9. [Extensions](#extensions)
10. [Benchmarks](#benchmarks)

---

## REST API Endpoints

### `GET /`

Root endpoint that returns the API overview.

**Response:**
```json
{
  "name": "Epiphany Engine API",
  "version": "0.1.0",
  "status": "ok",
  "docs_url": "/api/docs",
  "health_url": "/api/health",
  "info_url": "/api/info"
}
```

## Core Equation

### `axiom.core_equation`

#### `compute_intelligence(...)`

Compute intelligence score using the Universal Axiom.

**Signature:**
```python
def compute_intelligence(
    A: float,
    B: float,
    C: float,
    X: float,
    Y: float,
    Z: float,
    E_n: float,
    F_n: float,
    validate: bool = True,
    clamp_to_unit: bool = True,
    return_components: bool = False,
    strict_bounds: bool = False,
    clamp_values: Optional[bool] = None
) -> Union[float, Tuple[float, Dict[str, float]]]
```

**Parameters:**
- `A` (float): Alignment/Accuracy [0, 1]
- `B` (float): Broadness/Behavior [0, 1]
- `C` (float): Capacity [0, 1]
- `X` (float): Expressiveness/Objectivity [0, 1]
- `Y` (float): Yield [0, 1]
- `Z` (float): Zugehörigkeit (Belonging) [0, 1]
- `E_n` (float): Experience/Energy at step n [≥0]
- `F_n` (float): Fibonacci factor [≥-1]
- `validate` (bool): If True, enforce numeric type/finite checks
- `clamp_to_unit` (bool): If True, clamp out-of-range values to bounds
- `return_components` (bool): If True, return tuple with components breakdown
- `strict_bounds` (bool): If True, raise ValueError when values are out of bounds
- `clamp_values` (Optional[bool]): Deprecated alias for `clamp_to_unit`

**Returns:**
- If `return_components=False`: Intelligence score (float)
- If `return_components=True`: Tuple of (score, components_dict)

**Example:**
```python
from axiom.core_equation import compute_intelligence

score, components = compute_intelligence(
    A=0.8, B=0.7, C=0.6,
    X=0.8, Y=0.7, Z=0.7,
    E_n=5.0, F_n=3.0,
    return_components=True
)

print(f"Intelligence: {score:.2f}")
print(f"ABC: {components['ABC']:.4f}")
print(f"XYZ: {components['XYZ']:.4f}")
```

#### `e_recurrence(...)`

Compute next value in E sequence using linear recurrence.

**Signature:**
```python
def e_recurrence(E_prev: float, a: float, b: float) -> float
```

**Parameters:**
- `E_prev` (float): Previous E value
- `a` (float): Multiplicative coefficient
- `b` (float): Additive constant

**Returns:**
- float: E_n = a * E_{n-1} + b

**Example:**
```python
E_0 = 3.0
E_1 = e_recurrence(E_0, a=1.1, b=0.5)  # 3.8
E_2 = e_recurrence(E_1, a=1.1, b=0.5)  # 4.68
```

#### `fibonacci(n)`

Compute nth Fibonacci number.

**Signature:**
```python
def fibonacci(n: int) -> int
```

**Parameters:**
- `n` (int): Index (0-based)

**Returns:**
- int: nth Fibonacci number

**Raises:**
- ValueError: If n < 0

**Example:**
```python
fib_10 = fibonacci(10)  # 55
```

#### `fibonacci_sequence(count)`

Generate Fibonacci sequence.

**Signature:**
```python
def fibonacci_sequence(count: int) -> Generator[int, None, None]
```

**Parameters:**
- `count` (int): Number of terms to generate

**Yields:**
- int: Fibonacci numbers

**Example:**
```python
fibs = list(fibonacci_sequence(10))
# [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

---

## Subjectivity Scale

### `axiom.subjectivity_scale`

#### `determine_subjectivity(...)`

Determine subjectivity level from observation signals.

**Signature:**
```python
def determine_subjectivity(
    noise: float = 0.0,
    emotional_volatility: float = 0.0,
    bias_indicator: float = 0.0,
    *,
    weights: Optional[Dict[str, float]] = None,
    normalize: bool = True
) -> Tuple[float, str]
```

**Parameters:**
- `noise` (float): Signal noise (higher -> more subjectivity)
- `emotional_volatility` (float): Emotional component (higher -> more subjectivity)
- `bias_indicator` (float): Cognitive bias strength (higher -> more subjectivity)
- `weights` (dict, optional): Custom weights for each signal
- `normalize` (bool): If True, clamp computed value to [0, 1]

**Returns:**
- Tuple of (subjectivity_score, label)
  - subjectivity_score (float): [0, 1]
  - label (str): One of 7 tiers

**7-Tier Scale:**
1. apex-objective (<= 0.00)
2. objective (0.00 - 0.15]
3. base-static (0.15 - 0.33]
4. mid-dynamic (0.33 - 0.50]
5. high-subjective (0.50 - 0.67]
6. apex-dynamic (0.67 - 0.85]
7. apex-subjective (0.85 - 1.00]

**Example:**
```python
from axiom.subjectivity_scale import determine_subjectivity

level, label = determine_subjectivity(
    noise=0.2,
    emotional_volatility=0.3,
    bias_indicator=0.1
)
print(f"Subjectivity: {level:.2f} ({label})")
```

---

## TimeSphere Engine

### `engine.timesphere`

#### `TimeSphere`

Main simulation controller.

**Constructor:**
```python
def __init__(
    self,
    initial_inputs: AxiomInputs,
    update_rules: Dict[str, Callable] = None
)
```

**Parameters:**
- `initial_inputs` (AxiomInputs): Initial state
- `update_rules` (dict): Mapping of parameter names to update functions

**Methods:**

##### `simulate(steps, verbose=False)`

Run simulation for specified steps.

**Parameters:**
- `steps` (int): Number of steps to simulate
- `verbose` (bool): Print progress

**Returns:**
- SimulationResult

**Example:**
```python
from engine.timesphere import TimeSphere, UpdateRules
from engine.state import AxiomInputs

initial = AxiomInputs(
    A=0.5, B=0.5, C=0.6,
    X=0.7, Y=0.6, Z=0.6,
    E_n=4.0, F_n=2.0
)

rules = {
    "A": UpdateRules.linear_growth(rate=0.02, max_value=0.9),
    "B": UpdateRules.linear_growth(rate=0.03, max_value=0.9),
}

sphere = TimeSphere(initial, rules)
result = sphere.simulate(steps=20)
```

##### `add_event_handler(condition, handler, event_type)`

Register event handler.

**Parameters:**
- `condition` (Callable): Function that takes TimeStep and returns bool
- `handler` (Callable): Handler function that takes TimeStep
- `event_type` (str): Event identifier

**Example:**
```python
def milestone_reached(step):
    print(f"Milestone at step {step.step}!")

sphere.add_event_handler(
    lambda s: s.inputs.A > 0.8,
    milestone_reached,
    "alignment_milestone"
)
```

#### `SimulationResult`

Simulation results container.

**Attributes:**
- `history` (List[TimeStep]): Complete simulation history
- `summary` (Dict): Summary statistics
  - `min_intelligence`: Minimum intelligence score
  - `max_intelligence`: Maximum intelligence score
  - `avg_intelligence`: Average intelligence score
  - `final_intelligence`: Final intelligence score
  - `total_growth_pct`: Total growth percentage
  - `volatility`: Score volatility (std dev)

**Methods:**

##### `get_trend_analysis()`

Analyze intelligence trajectory trends.

**Returns:**
- Dict with trend information

---

## Update Rules

### `UpdateRules`

Pre-built update rule factory.

#### `UpdateRules.constant(value)`

Constant value rule.

**Parameters:**
- `value` (float): Constant value

**Returns:**
- Callable update function

**Example:**
```python
rule = UpdateRules.constant(0.7)
```

#### `UpdateRules.linear_growth(rate, max_value, min_value=0.0)`

Linear growth rule.

**Parameters:**
- `rate` (float): Growth rate per step
- `max_value` (float): Maximum value (ceiling)
- `min_value` (float): Minimum value (floor)

**Returns:**
- Callable update function

**Example:**
```python
rule = UpdateRules.linear_growth(rate=0.02, max_value=0.9)
```

#### `UpdateRules.decay(rate, min_value=0.0)`

Exponential decay rule.

**Parameters:**
- `rate` (float): Decay rate [0, 1]
- `min_value` (float): Minimum value (floor)

**Returns:**
- Callable update function

**Example:**
```python
rule = UpdateRules.decay(rate=0.05, min_value=0.1)
```

#### `UpdateRules.oscillate(amplitude, period, baseline=0.5)`

Sinusoidal oscillation rule.

**Parameters:**
- `amplitude` (float): Oscillation amplitude
- `period` (int): Oscillation period (steps)
- `baseline` (float): Center value

**Returns:**
- Callable update function

**Example:**
```python
rule = UpdateRules.oscillate(amplitude=0.2, period=10, baseline=0.6)
```

#### `UpdateRules.e_sequence_rule(a, b, min_value=0.0)`

E_n recurrence sequence rule.

**Parameters:**
- `a` (float): Multiplicative coefficient
- `b` (float): Additive constant
- `min_value` (float): Minimum value

**Returns:**
- Callable update function

**Example:**
```python
rule = UpdateRules.e_sequence_rule(a=1.05, b=0.2)
```

#### `UpdateRules.fibonacci_rule(scale=1.0, max_value=100.0)`

Fibonacci-based growth rule.

**Parameters:**
- `scale` (float): Scaling factor
- `max_value` (float): Maximum value

**Returns:**
- Callable update function

**Example:**
```python
rule = UpdateRules.fibonacci_rule(scale=0.1)
```

---

## Visualization

### `viz.plotter`

#### `plot_intelligence_trajectory(result, ...)`

Plot intelligence evolution over time.

**Parameters:**
- `result` (SimulationResult): Simulation result
- `title` (str): Plot title
- `figsize` (tuple): Figure size
- `show` (bool): Display plot
- `save_path` (str, optional): Save path

**Returns:**
- matplotlib Figure

**Example:**
```python
from viz.plotter import plot_intelligence_trajectory

fig = plot_intelligence_trajectory(
    result,
    title="My Simulation",
    save_path="trajectory.png"
)
```

#### `plot_component_evolution(result, components=None, ...)`

Plot individual component evolution.

**Parameters:**
- `result` (SimulationResult): Simulation result
- `components` (List[str], optional): Components to plot
- Other parameters same as plot_intelligence_trajectory

**Example:**
```python
from viz.plotter import plot_component_evolution

fig = plot_component_evolution(
    result,
    components=['A', 'B', 'C']
)
```

#### `create_dashboard(result, ...)`

Create comprehensive dashboard.

**Parameters:**
- `result` (SimulationResult): Simulation result
- `title` (str): Dashboard title
- `figsize` (tuple): Figure size
- `show` (bool): Display plot
- `save_path` (str, optional): Save path

**Returns:**
- matplotlib Figure

**Example:**
```python
from viz.plotter import create_dashboard

fig = create_dashboard(result, save_path="dashboard.png")
```

---

## Export Utilities

### `viz.exporters`

#### `export_to_json(result, filepath, ...)`

Export to JSON format.

**Parameters:**
- `result` (SimulationResult): Data to export
- `filepath` (str): Output path
- `include_summary` (bool): Include summary stats
- `indent` (int): JSON indentation

**Example:**
```python
from viz.exporters import export_to_json

export_to_json(result, "simulation.json")
```

#### `export_to_csv(result, filepath, ...)`

Export to CSV format.

**Parameters:**
- `result` (SimulationResult): Data to export
- `filepath` (str): Output path
- `include_metadata` (bool): Include metadata rows

**Example:**
```python
from viz.exporters import export_to_csv

export_to_csv(result, "simulation.csv")
```

#### `export_to_markdown(result, filepath, ...)`

Export to Markdown format.

**Parameters:**
- `result` (SimulationResult): Data to export
- `filepath` (str): Output path
- `title` (str): Document title
- `include_summary` (bool): Include summary
- `max_rows` (int, optional): Maximum rows to include

**Example:**
```python
from viz.exporters import export_to_markdown

export_to_markdown(result, "report.md", title="Simulation Report")
```

#### `generate_report(results, filepath, ...)`

Generate comparative report for multiple scenarios.

**Parameters:**
- `results` (Dict[str, SimulationResult]): Multiple scenarios
- `filepath` (str): Output path
- `title` (str): Report title
- `description` (str): Report description

**Example:**
```python
from viz.exporters import generate_report

results = {
    "Scenario A": result_a,
    "Scenario B": result_b
}

generate_report(results, "comparison.md")
```

---

## Extensions

### `extensions.base`

#### `BaseExtension`

Base class for all extensions.

**Methods:**
- `initialize()`: Called when extension is loaded
- `get_metadata()`: Return extension metadata
- `enable()`: Enable extension
- `disable()`: Disable extension

#### `UpdateRuleExtension`

Extension for custom update rules.

**Abstract Methods:**
- `get_update_rules()`: Return dict of update functions
- `get_rule_descriptions()`: Return dict of descriptions

#### `EventHandlerExtension`

Extension for custom event handlers.

**Abstract Methods:**
- `get_event_handlers()`: Return dict of handlers
- `get_event_types()`: Return dict of event descriptions

### `extensions.registry`

#### `get_registry()`

Get global extension registry.

**Returns:**
- ExtensionRegistry instance

**Example:**
```python
from extensions import get_registry, load_extension

registry = get_registry()
my_extension = load_extension(MyCustomExtension)
```

---

## Benchmarks

### `benchmarks.performance`

#### `benchmark_computation(iterations=10000, config=None)`

Benchmark core computation performance.

**Returns:**
- Dict with timing statistics

**Example:**
```python
from benchmarks import benchmark_computation

results = benchmark_computation(iterations=10000)
print(f"Mean time: {results['mean_time_ms']:.4f} ms")
print(f"Ops/sec: {results['ops_per_second']:.0f}")
```

#### `benchmark_simulation(steps=100, iterations=100)`

Benchmark simulation performance.

**Returns:**
- Dict with timing statistics

#### `run_all_benchmarks(verbose=True)`

Run comprehensive benchmark suite.

**Returns:**
- Dict with all benchmark results

**Example:**
```python
from benchmarks import run_all_benchmarks

results = run_all_benchmarks(verbose=True)
```

---

## Web API

### Endpoints

#### `POST /api/simulate`

Run simulation via REST API.

**Request Body:**
```json
{
  "initial": {
    "A": 0.5,
    "B": 0.5,
    "C": 0.6,
    "X": 0.7,
    "Y": 0.6,
    "Z": 0.6,
    "E_n": 4.0,
    "F_n": 2.0
  },
  "steps": 20,
  "preset": "baseline"
}
```

**Response:**
```json
{
  "history": [...],
  "summary": {...}
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/simulate \
  -H "Content-Type: application/json" \
  -d '{"preset": "growth", "steps": 20}'
```

---

## Error Handling

### Common Exceptions

#### `ValueError`

Raised when:
- Parameters are out of bounds (with `strict_bounds=True`)
- Invalid Fibonacci index (negative)
- Invalid configuration

#### `TypeError`

Raised when:
- Wrong parameter types provided
- Extension class is not proper subclass

#### `KeyError`

Raised when:
- Extension not found in registry
- Invalid preset name

---

## Best Practices

1. **Always use `return_components=True`** when analyzing results
2. **Enable clamping** for robustness: `clamp_to_unit=True`
3. **Use event handlers** for milestone detection
4. **Export results** for reproducibility
5. **Benchmark** custom update rules before deploying
6. **Validate** extensions before registration
7. **Use presets** for common scenarios

---

## Version Information

- API Version: 0.1.0
- Core Engine: Stable
- Extensions API: Experimental
- Visualization: Stable

---

For more examples, see the `examples/` directory and Jupyter notebooks in `notebooks/`.
