"""
TimeSphere: Time-based simulation engine for EPIPHANY systems.

Allows systems to evolve over discrete time steps while tracking:
- Intelligence scores over time
- Component evolution (A, B, C, X, Y, Z, E_n, F_n)
- State transitions and decision points
- Corruption vs coherence trends
"""
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from axiom.core_equation import compute_intelligence, e_recurrence, fibonacci
from engine.state import AxiomInputs, IntelligenceSnapshot, SystemState


@dataclass
class TimeStep:
    """Represents a single step in the simulation with full state."""
    step: int
    state: SystemState
    intelligence: IntelligenceSnapshot
    events: List[str] = field(default_factory=list)


@dataclass
class SimulationResult:
    """Results from a TimeSphere simulation run."""
    steps: List[TimeStep]
    summary: Dict[str, Any]

    def intelligence_history(self) -> List[float]:
        """Extract intelligence scores over time."""
        return [ts.intelligence.score for ts in self.steps]

    def component_history(self, component: str) -> List[float]:
        """Extract a specific component's values over time."""
        return [
            ts.intelligence.components.get(component, 0.0)
            for ts in self.steps
            if ts.intelligence.components
        ]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "steps": [
                {
                    "step": ts.step,
                    "state": ts.state.to_dict(),
                    "intelligence": ts.intelligence.to_dict(),
                    "events": ts.events,
                }
                for ts in self.steps
            ],
            "summary": self.summary,
        }


class TimeSphere:
    """
    Simulation engine for evolving EPIPHANY systems over time.

    Example usage:
        sphere = TimeSphere(initial_state)
        sphere.add_update_rule("E_n", lambda state, step: e_recurrence(state.inputs.E_n))
        sphere.add_update_rule("F_n", lambda state, step: fibonacci(step))
        result = sphere.simulate(steps=10)
    """

    def __init__(
        self,
        initial_inputs: AxiomInputs,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize TimeSphere with starting conditions.

        Parameters
        ----------
        initial_inputs : AxiomInputs
            Starting values for A, B, C, X, Y, Z, E_n, F_n
        metadata : optional dict
            Additional metadata about the system
        """
        self.initial_state = SystemState(step=0, inputs=initial_inputs, metadata=metadata or {})
        self.update_rules: Dict[str, Callable[[SystemState, int], float]] = {}
        self.event_handlers: List[Callable[[SystemState, int], Optional[str]]] = []
        self.history: List[TimeStep] = []

    def add_update_rule(self, variable: str, rule: Callable[[SystemState, int], float]):
        """
        Add a rule for updating a variable at each time step.

        Parameters
        ----------
        variable : str
            One of: A, B, C, X, Y, Z, E_n, F_n
        rule : callable
            Function taking (current_state, step_number) -> new_value
        """
        valid_vars = {"A", "B", "C", "X", "Y", "Z", "E_n", "F_n"}
        if variable not in valid_vars:
            raise ValueError(f"Variable must be one of {valid_vars}")
        self.update_rules[variable] = rule

    def add_event_handler(self, handler: Callable[[SystemState, int], Optional[str]]):
        """
        Add an event detection handler.

        Parameters
        ----------
        handler : callable
            Function taking (state, step) -> optional event description string
        """
        self.event_handlers.append(handler)

    def step(self, current_state: SystemState, step_num: int) -> TimeStep:
        """
        Execute one time step of the simulation.

        Parameters
        ----------
        current_state : SystemState
            Current system state
        step_num : int
            Current step number

        Returns
        -------
        TimeStep with new state and intelligence
        """
        # Create new inputs by applying update rules
        new_inputs_dict = current_state.inputs.to_dict()

        for var, rule in self.update_rules.items():
            new_inputs_dict[var] = rule(current_state, step_num)

        new_inputs = AxiomInputs(**new_inputs_dict)

        # Compute intelligence with components
        # Mypy doesn't understand the conditional return type
        intelligence_score, components = compute_intelligence(  # type: ignore[misc]
            **new_inputs.to_dict(), return_components=True  # type: ignore[arg-type]
        )

        # Create new state
        new_state = SystemState(
            step=step_num,
            inputs=new_inputs,
            metadata=current_state.metadata,
        )

        intelligence_snapshot = IntelligenceSnapshot(
            step=step_num, score=intelligence_score, components=components
        )

        # Check for events
        events = []
        for handler in self.event_handlers:
            event = handler(new_state, step_num)
            if event:
                events.append(event)

        return TimeStep(
            step=step_num,
            state=new_state,
            intelligence=intelligence_snapshot,
            events=events,
        )

    def simulate(self, steps: int, record_history: bool = True) -> SimulationResult:
        """
        Run the simulation for N steps.

        Parameters
        ----------
        steps : int
            Number of time steps to simulate
        record_history : bool
            Whether to keep full history (default True)

        Returns
        -------
        SimulationResult with timeline and analysis
        """
        history: List[TimeStep] = []
        current_state = self.initial_state

        # Record initial state
        # Mypy doesn't understand the conditional return type
        initial_score, initial_components = compute_intelligence(  # type: ignore[misc]
            **current_state.inputs.to_dict(), return_components=True  # type: ignore[arg-type]
        )
        initial_snapshot = IntelligenceSnapshot(
            step=0, score=initial_score, components=initial_components
        )
        initial_timestep = TimeStep(
            step=0,
            state=current_state,
            intelligence=initial_snapshot,
            events=["Simulation started"],
        )
        history.append(initial_timestep)

        # Simulate each step
        for step_num in range(1, steps + 1):
            timestep = self.step(current_state, step_num)
            if record_history:
                history.append(timestep)
            current_state = timestep.state

        # Generate summary statistics
        intelligence_scores = [ts.intelligence.score for ts in history]
        summary = {
            "total_steps": steps,
            "initial_intelligence": intelligence_scores[0],
            "final_intelligence": intelligence_scores[-1],
            "max_intelligence": max(intelligence_scores),
            "min_intelligence": min(intelligence_scores),
            "avg_intelligence": sum(intelligence_scores) / len(intelligence_scores),
            "growth_rate": (
                (intelligence_scores[-1] - intelligence_scores[0]) / intelligence_scores[0]
                if intelligence_scores[0] != 0
                else float("inf")
            ),
        }

        self.history = history
        return SimulationResult(steps=history, summary=summary)

    def analyze_trends(self) -> Dict[str, Any]:
        """
        Analyze trends from simulation history.

        Returns
        -------
        Dict with trend analysis including:
        - Growth trajectory (accelerating, decelerating, stable)
        - Critical events/inflection points
        - Component correlations
        """
        if not self.history:
            return {"error": "No simulation history available"}

        scores = [ts.intelligence.score for ts in self.history]

        # Detect trend
        if len(scores) < 3:
            trend = "insufficient_data"
        else:
            first_half_avg = sum(scores[: len(scores) // 2]) / (len(scores) // 2)
            second_half_avg = sum(scores[len(scores) // 2 :]) / (len(scores) - len(scores) // 2)

            if second_half_avg > first_half_avg * 1.1:
                trend = "accelerating_growth"
            elif second_half_avg < first_half_avg * 0.9:
                trend = "declining"
            else:
                trend = "stable"

        # Find inflection points (where growth rate changes significantly)
        inflection_points = []
        for i in range(1, len(scores) - 1):
            delta_before = scores[i] - scores[i - 1]
            delta_after = scores[i + 1] - scores[i]
            if abs(delta_after - delta_before) > 0.1 * scores[i]:
                inflection_points.append(
                    {"step": self.history[i].step, "score": scores[i], "type": "significant_change"}
                )

        return {
            "trend": trend,
            "inflection_points": inflection_points,
            "total_events": sum(len(ts.events) for ts in self.history),
            "score_volatility": max(scores) - min(scores) if scores else 0,
        }


# Pre-built update rules for common scenarios
class UpdateRules:
    """Collection of common update rules for TimeSphere simulations."""

    @staticmethod
    def constant(value: float) -> Callable[[SystemState, int], float]:
        """Keep value constant."""
        return lambda state, step: value

    @staticmethod
    def linear_growth(
        rate: float,
        max_val: float = 1.0,
        *,
        variable: str = "A",
    ) -> Callable[[SystemState, int], float]:
        """Linear growth with optional cap."""

        def rule(state: SystemState, step: int) -> float:
            inputs = state.inputs.to_dict()
            current = inputs.get(variable, 0.0)  # default lookup
            new_val = current + rate
            return min(max_val, max(0.0, new_val))

        return rule

    @staticmethod
    def e_sequence_rule(a: float = 3.0, b: float = 2.0) -> Callable[[SystemState, int], float]:
        """E_n recurrence: E_n = a * E_{n-1} + b"""

        def rule(state: SystemState, step: int) -> float:
            return e_recurrence(state.inputs.E_n, a=a, b=b)

        return rule

    @staticmethod
    def fibonacci_rule() -> Callable[[SystemState, int], float]:
        """F_n follows Fibonacci sequence."""
        return lambda state, step: float(fibonacci(step))

    @staticmethod
    def decay(
        rate: float,
        min_val: float = 0.0,
        *,
        variable: str = "A",
    ) -> Callable[[SystemState, int], float]:
        """Exponential decay with floor."""

        def rule(state: SystemState, step: int) -> float:
            inputs = state.inputs.to_dict()
            current = inputs.get(variable, 1.0)
            new_val = current * (1.0 - rate)
            return max(min_val, new_val)

        return rule

    @staticmethod
    def oscillate(amplitude: float = 0.3, period: int = 10, baseline: float = 0.5) -> Callable[[SystemState, int], float]:
        """Sinusoidal oscillation."""
        import math

        def rule(state: SystemState, step: int) -> float:
            value = baseline + amplitude * math.sin(2 * math.pi * step / period)
            # Clamp to [0, 1] to match bounded input semantics.
            return min(1.0, max(0.0, value))

        return rule
