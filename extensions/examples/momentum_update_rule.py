"""
Momentum-based update rule extension.

Demonstrates how to create a custom update rule that tracks
momentum (rate of change) and accelerates growth or decay.
"""

from typing import Callable

from engine.state import SystemState
from extensions.base import UpdateRuleExtension


class MomentumUpdateRule(UpdateRuleExtension):
    """
    Update rule that applies momentum-based updates.

    Tracks the rate of change and applies acceleration based on
    the direction of movement.
    """

    def __init__(
        self,
        variable: str,
        momentum_factor: float = 0.9,
        acceleration: float = 0.1,
        min_value: float = 0.0,
        max_value: float = 1.0,
    ):
        """
        Initialize momentum update rule.

        Args:
            variable: Variable name to track momentum for
            momentum_factor: How much to retain previous momentum (0-1)
            acceleration: Acceleration multiplier
            min_value: Minimum allowed value
            max_value: Maximum allowed value
        """
        super().__init__()
        self.variable = variable
        self.momentum_factor = momentum_factor
        self.acceleration = acceleration
        self.min_value = min_value
        self.max_value = max_value
        self._previous_value = None
        self._velocity = 0.0

    def get_update_rule(self, variable: str) -> Callable[[SystemState], float]:
        """
        Generate update rule function for the specified variable.

        Args:
            variable: Variable name to generate rule for

        Returns:
            Update function that applies momentum
        """
        if variable != self.variable:
            return None

        def momentum_update(state: SystemState) -> float:
            """Apply momentum-based update to variable."""
            current_value = getattr(state.inputs, variable)

            # Initialize on first call
            if self._previous_value is None:
                self._previous_value = current_value
                return current_value

            # Calculate velocity (rate of change)
            delta = current_value - self._previous_value

            # Update velocity with momentum
            self._velocity = self.momentum_factor * self._velocity + delta

            # Apply acceleration
            new_value = current_value + self._velocity * self.acceleration

            # Clamp to valid range
            new_value = max(self.min_value, min(self.max_value, new_value))

            # Update tracking
            self._previous_value = current_value

            return new_value

        return momentum_update

    def get_metadata(self) -> dict:
        """Get extension metadata."""
        return {
            "name": "MomentumUpdateRule",
            "version": "1.0.0",
            "author": "Epiphany Engine Team",
            "description": "Update rule with momentum-based acceleration",
            "variable": self.variable,
            "momentum_factor": self.momentum_factor,
            "acceleration": self.acceleration,
        }


# Example usage function
def create_momentum_rule(
    variable: str,
    momentum_factor: float = 0.9,
    acceleration: float = 0.1,
) -> Callable[[SystemState], float]:
    """
    Create a momentum update rule for a variable.

    Args:
        variable: Variable name (A, B, C, X, Y, Z, E_n, F_n)
        momentum_factor: Momentum retention (0-1)
        acceleration: Acceleration multiplier

    Returns:
        Update function with momentum

    Example:
        >>> from extensions.examples.momentum_update_rule import create_momentum_rule
        >>> from engine.timesphere import TimeSphere
        >>> from engine.state import AxiomInputs
        >>>
        >>> inputs = AxiomInputs(A=0.5, B=0.6, C=0.7, X=0.8, Y=0.9, Z=0.85, E_n=1.0, F_n=1.0)
        >>> sphere = TimeSphere(initial_inputs=inputs)
        >>> sphere.add_update_rule("A", create_momentum_rule("A", momentum_factor=0.95))
        >>> result = sphere.simulate(steps=50)
    """
    ext = MomentumUpdateRule(variable, momentum_factor, acceleration)
    return ext.get_update_rule(variable)
