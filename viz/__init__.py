"""
Visualization module for The EPIPHANY Engine.

Provides rich visualizations for axiom analysis, simulation results,
and comparative scenarios.
"""

from .exporters import export_to_csv, export_to_json, export_to_markdown, generate_report
from .plotter import (
    create_dashboard,
    plot_component_evolution,
    plot_heatmap_2d,
    plot_intelligence_trajectory,
    plot_scenario_comparison,
    plot_sensitivity_analysis,
)

__all__ = [
    'plot_intelligence_trajectory',
    'plot_component_evolution',
    'plot_sensitivity_analysis',
    'plot_scenario_comparison',
    'plot_heatmap_2d',
    'create_dashboard',
    'export_to_json',
    'export_to_csv',
    'export_to_markdown',
    'generate_report'
]
