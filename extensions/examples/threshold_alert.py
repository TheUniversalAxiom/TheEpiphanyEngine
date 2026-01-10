"""
Threshold alert event handler extension.

Demonstrates how to create custom event handlers that trigger
alerts when intelligence or component values cross thresholds.
"""

import logging
from typing import List, Dict, Any

from extensions.base import EventHandlerExtension
from engine.state import SystemState


logger = logging.getLogger(__name__)


class ThresholdAlertHandler(EventHandlerExtension):
    """
    Event handler that monitors thresholds and triggers alerts.

    Tracks when intelligence or component values cross
    configurable thresholds and logs alerts.
    """

    def __init__(
        self,
        intelligence_thresholds: List[float] = None,
        component_thresholds: Dict[str, List[float]] = None,
    ):
        """
        Initialize threshold alert handler.

        Args:
            intelligence_thresholds: List of intelligence values to monitor
            component_thresholds: Dict mapping variable names to threshold lists
        """
        super().__init__()
        self.intelligence_thresholds = intelligence_thresholds or []
        self.component_thresholds = component_thresholds or {}
        self._triggered_intelligence = set()
        self._triggered_components = {var: set() for var in self.component_thresholds}
        self.alerts = []

    def handle_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """
        Handle simulation events and check thresholds.

        Args:
            event_type: Type of event (step_complete, simulation_complete, etc.)
            data: Event data including state and intelligence
        """
        if event_type != "step_complete":
            return

        state = data.get("state")
        intelligence = data.get("intelligence", 0.0)
        step = data.get("step", 0)

        if not state:
            return

        # Check intelligence thresholds
        for threshold in self.intelligence_thresholds:
            threshold_key = f"intelligence_{threshold}"
            if intelligence >= threshold and threshold_key not in self._triggered_intelligence:
                self._triggered_intelligence.add(threshold_key)
                alert = {
                    "step": step,
                    "type": "intelligence_threshold",
                    "threshold": threshold,
                    "value": intelligence,
                    "message": f"Intelligence crossed threshold {threshold} at step {step}",
                }
                self.alerts.append(alert)
                logger.warning(alert["message"])

        # Check component thresholds
        for var, thresholds in self.component_thresholds.items():
            value = getattr(state.inputs, var, None)
            if value is None:
                continue

            for threshold in thresholds:
                threshold_key = f"{var}_{threshold}"
                if value >= threshold and threshold_key not in self._triggered_components[var]:
                    self._triggered_components[var].add(threshold_key)
                    alert = {
                        "step": step,
                        "type": "component_threshold",
                        "variable": var,
                        "threshold": threshold,
                        "value": value,
                        "message": f"{var} crossed threshold {threshold} at step {step}",
                    }
                    self.alerts.append(alert)
                    logger.warning(alert["message"])

    def get_alerts(self) -> List[Dict[str, Any]]:
        """
        Get all triggered alerts.

        Returns:
            List of alert dictionaries
        """
        return self.alerts

    def reset(self):
        """Reset alert tracking."""
        self._triggered_intelligence.clear()
        for var in self._triggered_components:
            self._triggered_components[var].clear()
        self.alerts.clear()

    def get_metadata(self) -> dict:
        """Get extension metadata."""
        return {
            "name": "ThresholdAlertHandler",
            "version": "1.0.0",
            "author": "Epiphany Engine Team",
            "description": "Event handler for threshold-based alerts",
            "intelligence_thresholds": self.intelligence_thresholds,
            "component_thresholds": self.component_thresholds,
            "alerts_triggered": len(self.alerts),
        }


# Example usage
if __name__ == "__main__":
    from engine.timesphere import TimeSphere
    from engine.state import AxiomInputs

    # Create simulation
    inputs = AxiomInputs(A=0.3, B=0.4, C=0.5, X=0.6, Y=0.7, Z=0.8, E_n=1.0, F_n=1.0)
    sphere = TimeSphere(initial_inputs=inputs)

    # Create threshold alert handler
    alert_handler = ThresholdAlertHandler(
        intelligence_thresholds=[1.0, 2.0, 5.0, 10.0],
        component_thresholds={
            "A": [0.5, 0.8, 1.0],
            "E_n": [5.0, 10.0, 20.0],
        },
    )

    # Add event handler (if supported by TimeSphere)
    # sphere.add_event_handler(alert_handler)

    # Run simulation
    # result = sphere.simulate(steps=100)

    # Get alerts
    print(f"Alerts triggered: {len(alert_handler.get_alerts())}")
    for alert in alert_handler.get_alerts():
        print(f"  {alert['message']}")
