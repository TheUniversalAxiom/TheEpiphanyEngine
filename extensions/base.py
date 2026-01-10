"""
Base classes for EPIPHANY Engine extensions.
"""

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict


class BaseExtension(ABC):
    """
    Base class for all extensions.

    Extensions can provide custom functionality and register with the
    extension registry for discovery and management.
    """

    def __init__(self, name: str, version: str = "1.0.0"):
        """
        Initialize extension.

        Args:
            name: Extension name (should be unique)
            version: Extension version
        """
        self.name = name
        self.version = version
        self.enabled = True

    @abstractmethod
    def initialize(self) -> None:
        """
        Initialize the extension.
        Called when the extension is loaded.
        """
        pass

    @abstractmethod
    def get_metadata(self) -> Dict[str, Any]:
        """
        Return extension metadata.

        Returns:
            Dict with metadata (author, description, dependencies, etc.)
        """
        pass

    def enable(self) -> None:
        """Enable this extension."""
        self.enabled = True

    def disable(self) -> None:
        """Disable this extension."""
        self.enabled = False


class UpdateRuleExtension(BaseExtension):
    """
    Extension for custom update rules.

    Allows users to register domain-specific update logic that can be
    used in TimeSphere simulations.
    """

    @abstractmethod
    def get_update_rules(self) -> Dict[str, Callable]:
        """
        Return custom update rules.

        Returns:
            Dict mapping rule names to update functions
            Update function signature: (AxiomInputs, step: int) -> float
        """
        pass

    @abstractmethod
    def get_rule_descriptions(self) -> Dict[str, str]:
        """
        Return descriptions for each update rule.

        Returns:
            Dict mapping rule names to human-readable descriptions
        """
        pass


class EventHandlerExtension(BaseExtension):
    """
    Extension for custom event handlers.

    Allows users to register handlers for simulation milestones,
    warnings, or custom events.
    """

    @abstractmethod
    def get_event_handlers(self) -> Dict[str, Callable]:
        """
        Return custom event handlers.

        Returns:
            Dict mapping event types to handler functions
            Handler signature: (TimeStep, **kwargs) -> None
        """
        pass

    @abstractmethod
    def get_event_types(self) -> Dict[str, str]:
        """
        Return event type descriptions.

        Returns:
            Dict mapping event type names to descriptions
        """
        pass


class IntegrationExtension(BaseExtension):
    """
    Extension for external system integrations.

    Allows users to integrate with databases, APIs, monitoring systems,
    or other external tools.
    """

    @abstractmethod
    def connect(self, **kwargs) -> None:
        """
        Establish connection to external system.

        Args:
            **kwargs: Connection parameters
        """
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Disconnect from external system."""
        pass

    @abstractmethod
    def export_result(self, result: Any) -> None:
        """
        Export simulation result to external system.

        Args:
            result: SimulationResult or other data to export
        """
        pass


class DomainModelExtension(BaseExtension):
    """
    Extension for domain-specific intelligence models.

    Allows users to create specialized models for specific domains
    (e.g., organizational intelligence, ecological systems, etc.)
    """

    @abstractmethod
    def get_parameter_mappings(self) -> Dict[str, str]:
        """
        Return domain-specific parameter interpretations.

        Returns:
            Dict mapping axiom parameters to domain concepts
            Example: {"A": "Team Alignment", "B": "Skill Breadth", ...}
        """
        pass

    @abstractmethod
    def get_default_config(self) -> Dict[str, float]:
        """
        Return recommended default configuration for this domain.

        Returns:
            Dict with parameter values
        """
        pass

    @abstractmethod
    def validate_config(self, config: Dict[str, float]) -> bool:
        """
        Validate configuration for domain-specific constraints.

        Args:
            config: Parameter configuration

        Returns:
            True if valid, False otherwise
        """
        pass


class AnalysisExtension(BaseExtension):
    """
    Extension for custom analysis and metrics.

    Allows users to add domain-specific analytics on top of
    simulation results.
    """

    @abstractmethod
    def analyze(self, result: Any) -> Dict[str, Any]:
        """
        Perform custom analysis on simulation result.

        Args:
            result: SimulationResult to analyze

        Returns:
            Dict with analysis results
        """
        pass

    @abstractmethod
    def get_metrics(self) -> Dict[str, str]:
        """
        Return available metrics with descriptions.

        Returns:
            Dict mapping metric names to descriptions
        """
        pass
