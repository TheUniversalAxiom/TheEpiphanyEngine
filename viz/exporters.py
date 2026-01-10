"""
Export utilities for simulation results and analyses.
"""

import csv
import json
from datetime import datetime
from typing import Dict, Optional

from engine.timesphere import SimulationResult


def export_to_json(
    result: SimulationResult,
    filepath: str,
    include_summary: bool = True,
    indent: int = 2
) -> None:
    """
    Export simulation result to JSON format.

    Args:
        result: SimulationResult to export
        filepath: Output file path
        include_summary: Whether to include summary statistics
        indent: JSON indentation level
    """
    data = {
        "metadata": {
            "export_time": datetime.now().isoformat(),
            "total_steps": len(result.history),
        },
        "history": []
    }

    # Export each time step
    for step in result.history:
        step_data = {
            "step": step.step,
            "intelligence": step.intelligence,
            "inputs": {
                "A": step.inputs.A,
                "B": step.inputs.B,
                "C": step.inputs.C,
                "X": step.inputs.X,
                "Y": step.inputs.Y,
                "Z": step.inputs.Z,
                "E_n": step.inputs.E_n,
                "F_n": step.inputs.F_n,
            }
        }
        data["history"].append(step_data)

    # Add summary statistics
    if include_summary:
        data["summary"] = result.summary

    # Write to file
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=indent)


def export_to_csv(
    result: SimulationResult,
    filepath: str,
    include_metadata: bool = True
) -> None:
    """
    Export simulation result to CSV format.

    Args:
        result: SimulationResult to export
        filepath: Output file path
        include_metadata: Whether to include metadata rows
    """
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)

        # Optional metadata
        if include_metadata:
            writer.writerow(["# EPIPHANY Engine Simulation Export"])
            writer.writerow(["# Export Time", datetime.now().isoformat()])
            writer.writerow(["# Total Steps", len(result.history)])
            writer.writerow([])

        # Header
        writer.writerow([
            "Step", "Intelligence", "A", "B", "C", "X", "Y", "Z", "E_n", "F_n"
        ])

        # Data rows
        for step in result.history:
            writer.writerow([
                step.step,
                f"{step.intelligence:.6f}",
                f"{step.inputs.A:.4f}",
                f"{step.inputs.B:.4f}",
                f"{step.inputs.C:.4f}",
                f"{step.inputs.X:.4f}",
                f"{step.inputs.Y:.4f}",
                f"{step.inputs.Z:.4f}",
                f"{step.inputs.E_n:.4f}",
                f"{step.inputs.F_n:.4f}",
            ])

        # Summary statistics
        if include_metadata:
            writer.writerow([])
            writer.writerow(["# Summary Statistics"])
            for key, value in result.summary.items():
                writer.writerow([f"# {key}", value])


def export_to_markdown(
    result: SimulationResult,
    filepath: str,
    title: str = "Simulation Results",
    include_summary: bool = True,
    max_rows: Optional[int] = None
) -> None:
    """
    Export simulation result to Markdown format.

    Args:
        result: SimulationResult to export
        filepath: Output file path
        title: Document title
        include_summary: Whether to include summary section
        max_rows: Maximum number of rows to include (None = all)
    """
    lines = []

    # Title and metadata
    lines.append(f"# {title}\n")
    lines.append(f"**Export Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    lines.append(f"**Total Steps:** {len(result.history)}\n")
    lines.append("")

    # Summary statistics
    if include_summary:
        lines.append("## Summary Statistics\n")
        lines.append("| Metric | Value |")
        lines.append("|--------|-------|")
        for key, value in result.summary.items():
            formatted_key = key.replace('_', ' ').title()
            if isinstance(value, float):
                lines.append(f"| {formatted_key} | {value:.4f} |")
            else:
                lines.append(f"| {formatted_key} | {value} |")
        lines.append("")

    # History table
    lines.append("## Simulation History\n")
    lines.append("| Step | Intelligence | A | B | C | X | Y | Z | E_n | F_n |")
    lines.append("|------|-------------|---|---|---|---|---|---|-----|-----|")

    history = result.history if max_rows is None else result.history[:max_rows]

    for step in history:
        lines.append(
            f"| {step.step} | {step.intelligence:.4f} | "
            f"{step.inputs.A:.2f} | {step.inputs.B:.2f} | {step.inputs.C:.2f} | "
            f"{step.inputs.X:.2f} | {step.inputs.Y:.2f} | {step.inputs.Z:.2f} | "
            f"{step.inputs.E_n:.2f} | {step.inputs.F_n:.2f} |"
        )

    if max_rows and len(result.history) > max_rows:
        lines.append(f"\n*... {len(result.history) - max_rows} more rows ...*\n")

    # Write to file
    with open(filepath, 'w') as f:
        f.write('\n'.join(lines))


def generate_report(
    results: Dict[str, SimulationResult],
    filepath: str,
    title: str = "Intelligence Analysis Report",
    description: str = ""
) -> None:
    """
    Generate comprehensive Markdown report comparing multiple scenarios.

    Args:
        results: Dict mapping scenario names to SimulationResults
        filepath: Output file path
        title: Report title
        description: Optional report description
    """
    lines = []

    # Header
    lines.append(f"# {title}\n")
    if description:
        lines.append(f"{description}\n")
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    lines.append("---\n")

    # Executive summary
    lines.append("## Executive Summary\n")
    lines.append("| Scenario | Final Intelligence | Growth | Volatility |")
    lines.append("|----------|-------------------|--------|-----------|")

    for name, result in results.items():
        summary = result.summary
        lines.append(
            f"| {name} | {summary['final_intelligence']:.2f} | "
            f"{summary['total_growth_pct']:+.1f}% | {summary['volatility']:.2f} |"
        )

    lines.append("")

    # Detailed analysis per scenario
    for name, result in results.items():
        lines.append(f"## Scenario: {name}\n")

        summary = result.summary

        # Key metrics
        lines.append("### Key Metrics\n")
        lines.append(f"- **Intelligence Range:** {summary['min_intelligence']:.2f} → {summary['max_intelligence']:.2f}")
        lines.append(f"- **Average Intelligence:** {summary['avg_intelligence']:.2f}")
        lines.append(f"- **Total Growth:** {summary['total_growth_pct']:+.1f}%")
        lines.append(f"- **Volatility:** {summary['volatility']:.2f}")
        lines.append("")

        # Initial vs Final state
        initial = result.history[0]
        final = result.history[-1]

        lines.append("### Parameter Evolution\n")
        lines.append("| Parameter | Initial | Final | Change |")
        lines.append("|-----------|---------|-------|--------|")

        params = ['A', 'B', 'C', 'X', 'Y', 'Z', 'E_n', 'F_n']
        for param in params:
            initial_val = getattr(initial.inputs, param)
            final_val = getattr(final.inputs, param)
            change = final_val - initial_val
            lines.append(
                f"| {param} | {initial_val:.4f} | {final_val:.4f} | "
                f"{change:+.4f} |"
            )

        lines.append("")

        # Bottleneck analysis
        final_params = {p: getattr(final.inputs, p) for p in ['A', 'B', 'C', 'X', 'Y', 'Z']}
        bottleneck = min(final_params, key=final_params.get)
        lines.append("### Bottleneck Analysis\n")
        lines.append(f"**Primary Bottleneck:** {bottleneck} (value: {final_params[bottleneck]:.3f})\n")

        lines.append("---\n")

    # Recommendations
    lines.append("## Recommendations\n")

    # Find best and worst performers
    best_scenario = max(results.items(),
                       key=lambda x: x[1].summary['final_intelligence'])
    worst_scenario = min(results.items(),
                        key=lambda x: x[1].summary['final_intelligence'])

    lines.append(f"- **Highest Intelligence:** {best_scenario[0]} "
                f"({best_scenario[1].summary['final_intelligence']:.2f})")
    lines.append(f"- **Lowest Intelligence:** {worst_scenario[0]} "
                f"({worst_scenario[1].summary['final_intelligence']:.2f})")

    # Find most/least volatile
    most_volatile = max(results.items(),
                       key=lambda x: x[1].summary['volatility'])
    least_volatile = min(results.items(),
                        key=lambda x: x[1].summary['volatility'])

    lines.append(f"- **Most Stable:** {least_volatile[0]} "
                f"(volatility: {least_volatile[1].summary['volatility']:.2f})")
    lines.append(f"- **Most Volatile:** {most_volatile[0]} "
                f"(volatility: {most_volatile[1].summary['volatility']:.2f})")

    lines.append("")

    # Write to file
    with open(filepath, 'w') as f:
        f.write('\n'.join(lines))


def export_comparison_csv(
    results: Dict[str, SimulationResult],
    filepath: str
) -> None:
    """
    Export comparison of multiple scenarios to CSV.

    Args:
        results: Dict mapping scenario names to SimulationResults
        filepath: Output file path
    """
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)

        # Header
        writer.writerow(["# Multi-Scenario Comparison"])
        writer.writerow(["# Export Time", datetime.now().isoformat()])
        writer.writerow([])

        # Summary comparison
        writer.writerow(["Scenario", "Final Intelligence", "Growth %",
                        "Avg Intelligence", "Volatility",
                        "Final A", "Final B", "Final C"])

        for name, result in results.items():
            summary = result.summary
            final = result.history[-1]

            writer.writerow([
                name,
                f"{summary['final_intelligence']:.4f}",
                f"{summary['total_growth_pct']:.2f}",
                f"{summary['avg_intelligence']:.4f}",
                f"{summary['volatility']:.4f}",
                f"{final.inputs.A:.4f}",
                f"{final.inputs.B:.4f}",
                f"{final.inputs.C:.4f}",
            ])
