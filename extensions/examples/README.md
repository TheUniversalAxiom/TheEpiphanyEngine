# Example Extensions

This directory contains example extensions demonstrating how to extend the Epiphany Engine using the plugin architecture.

## Available Examples

### 1. Momentum Update Rule (`momentum_update_rule.py`)

A custom update rule that applies momentum-based updates to variables, creating more realistic acceleration and deceleration patterns.

**Features:**
- Tracks rate of change (velocity) over time
- Applies momentum factor to smooth updates
- Supports configurable acceleration
- Automatically clamps values to valid ranges

**Usage:**
```python
from extensions.examples.momentum_update_rule import create_momentum_rule
from engine.timesphere import TimeSphere
from engine.state import AxiomInputs

# Create simulation
inputs = AxiomInputs(A=0.5, B=0.6, C=0.7, X=0.8, Y=0.9, Z=0.85, E_n=1.0, F_n=1.0)
sphere = TimeSphere(initial_inputs=inputs)

# Add momentum-based update rule
sphere.add_update_rule("A", create_momentum_rule("A", momentum_factor=0.95, acceleration=0.1))

# Run simulation
result = sphere.simulate(steps=50)
```

### 2. Threshold Alert Handler (`threshold_alert.py`)

An event handler that monitors intelligence and component values, triggering alerts when they cross configurable thresholds.

**Features:**
- Monitor intelligence thresholds
- Monitor component variable thresholds
- Track all triggered alerts with timestamps
- Log warnings when thresholds are crossed
- Reset capability for reuse

**Usage:**
```python
from extensions.examples.threshold_alert import ThresholdAlertHandler
from engine.timesphere import TimeSphere
from engine.state import AxiomInputs

# Create alert handler
alert_handler = ThresholdAlertHandler(
    intelligence_thresholds=[1.0, 2.0, 5.0, 10.0],
    component_thresholds={
        "A": [0.5, 0.8, 1.0],
        "E_n": [5.0, 10.0, 20.0],
    },
)

# Create and run simulation
inputs = AxiomInputs(A=0.3, B=0.4, C=0.5, X=0.6, Y=0.7, Z=0.8, E_n=1.0, F_n=1.0)
sphere = TimeSphere(initial_inputs=inputs)

# Note: Event handler integration requires TimeSphere event support
# For now, you can manually call alert_handler.handle_event() with simulation data

# Get triggered alerts
alerts = alert_handler.get_alerts()
for alert in alerts:
    print(alert['message'])
```

## Creating Your Own Extensions

### Update Rule Extensions

Extend `UpdateRuleExtension` to create custom variable update logic:

```python
from extensions.base import UpdateRuleExtension
from engine.state import SystemState
from typing import Callable

class MyUpdateRule(UpdateRuleExtension):
    def __init__(self, variable: str, **params):
        super().__init__()
        self.variable = variable
        self.params = params

    def get_update_rule(self, variable: str) -> Callable[[SystemState], float]:
        if variable != self.variable:
            return None

        def my_update(state: SystemState) -> float:
            # Your custom update logic here
            current = getattr(state.inputs, variable)
            # ... compute new value ...
            return new_value

        return my_update

    def get_metadata(self) -> dict:
        return {
            "name": "MyUpdateRule",
            "version": "1.0.0",
            "description": "My custom update rule",
        }
```

### Event Handler Extensions

Extend `EventHandlerExtension` to react to simulation events:

```python
from extensions.base import EventHandlerExtension
from typing import Dict, Any

class MyEventHandler(EventHandlerExtension):
    def __init__(self):
        super().__init__()

    def handle_event(self, event_type: str, data: Dict[str, Any]) -> None:
        if event_type == "step_complete":
            # React to step completion
            state = data.get("state")
            intelligence = data.get("intelligence")
            # ... your logic ...

    def get_metadata(self) -> dict:
        return {
            "name": "MyEventHandler",
            "version": "1.0.0",
            "description": "My custom event handler",
        }
```

## Extension Types

The extension system supports multiple types:

1. **UpdateRuleExtension** - Custom variable update logic
2. **EventHandlerExtension** - React to simulation events
3. **IntegrationExtension** - Integrate with external systems
4. **DomainModelExtension** - Domain-specific intelligence models
5. **AnalysisExtension** - Custom analysis and metrics

See `extensions/base.py` for base class details.

## Best Practices

1. **Always call `super().__init__()`** in your extension constructors
2. **Provide complete metadata** via `get_metadata()`
3. **Use type hints** for better IDE support
4. **Document parameters** in docstrings
5. **Test your extensions** thoroughly before use
6. **Handle edge cases** (None values, invalid inputs)
7. **Keep extensions focused** - one responsibility per extension

## Contributing Extensions

If you create a useful extension, consider contributing it to the project:

1. Add it to `extensions/examples/`
2. Include comprehensive docstrings
3. Add usage examples
4. Update this README
5. Submit a pull request

## Questions?

See the main [CONTRIBUTING.md](../../CONTRIBUTING.md) for development guidelines.
