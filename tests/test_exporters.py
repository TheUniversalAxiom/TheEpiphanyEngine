"""
Tests for viz/exporters.py
"""
import csv
import json
import os
import tempfile
from pathlib import Path

from engine.state import AxiomInputs, IntelligenceSnapshot, SystemState
from engine.timesphere import SimulationResult, TimeStep
from viz.exporters import (
    export_comparison_csv,
    export_to_csv,
    export_to_json,
    export_to_markdown,
    generate_report,
)


def create_mock_simulation_result(num_steps: int = 5) -> SimulationResult:
    """
    Create a mock SimulationResult for testing.

    Args:
        num_steps: Number of simulation steps to generate

    Returns:
        Mock SimulationResult with test data
    """
    steps = []

    for i in range(num_steps):
        inputs = AxiomInputs(
            A=0.8 + i * 0.02,
            B=0.7 + i * 0.03,
            C=0.9 - i * 0.01,
            X=1.0,
            Y=0.95,
            Z=0.98,
            E_n=1.0 + i * 0.5,
            F_n=float(i),
        )

        state = SystemState(step=i, inputs=inputs, metadata={"scenario": "test"})

        intelligence = IntelligenceSnapshot(
            step=i,
            score=100.0 + i * 10.0,
            components={"ABC": 0.5, "XYZ": 0.9, "E_factor": 1.0}
        )

        step = TimeStep(
            step=i,
            state=state,
            intelligence=intelligence,
            events=[f"Event {i}"] if i % 2 == 0 else []
        )

        steps.append(step)

    summary = {
        "initial_intelligence": steps[0].intelligence.score,
        "final_intelligence": steps[-1].intelligence.score,
        "avg_intelligence": sum(s.intelligence.score for s in steps) / len(steps),
        "min_intelligence": min(s.intelligence.score for s in steps),
        "max_intelligence": max(s.intelligence.score for s in steps),
        "total_growth_pct": ((steps[-1].intelligence.score - steps[0].intelligence.score)
                            / steps[0].intelligence.score * 100),
        "volatility": 5.5,
    }

    return SimulationResult(steps=steps, summary=summary)


def test_export_to_json_basic():
    """Test basic JSON export functionality."""
    result = create_mock_simulation_result(num_steps=3)

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        filepath = f.name

    try:
        # Export to JSON
        export_to_json(result, filepath, include_summary=True, indent=2)

        # Verify file exists and is valid JSON
        assert os.path.exists(filepath), "JSON file should exist"

        with open(filepath, 'r') as f:
            data = json.load(f)

        # Check structure
        assert "metadata" in data, "Should have metadata"
        assert "history" in data, "Should have history"
        assert "summary" in data, "Should have summary"

        # Check metadata
        assert data["metadata"]["total_steps"] == 3, "Should have 3 steps"

        # Check history
        assert len(data["history"]) == 3, "Should have 3 history entries"
        assert data["history"][0]["step"] == 0, "First step should be 0"
        assert data["history"][0]["intelligence"] == 100.0, "First intelligence should be 100.0"

        # Check inputs
        first_inputs = data["history"][0]["inputs"]
        assert "A" in first_inputs, "Should have A component"
        assert "E_n" in first_inputs, "Should have E_n component"
        assert first_inputs["F_n"] == 0.0, "First F_n should be 0"

        print("✓ Basic JSON export")

    finally:
        if os.path.exists(filepath):
            os.unlink(filepath)


def test_export_to_json_without_summary():
    """Test JSON export without summary."""
    result = create_mock_simulation_result(num_steps=2)

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        filepath = f.name

    try:
        export_to_json(result, filepath, include_summary=False)

        with open(filepath, 'r') as f:
            data = json.load(f)

        assert "summary" not in data, "Should not have summary when include_summary=False"
        assert "history" in data, "Should still have history"

        print("✓ JSON export without summary")

    finally:
        if os.path.exists(filepath):
            os.unlink(filepath)


def test_export_to_csv_basic():
    """Test basic CSV export functionality."""
    result = create_mock_simulation_result(num_steps=4)

    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        filepath = f.name

    try:
        export_to_csv(result, filepath, include_metadata=True)

        assert os.path.exists(filepath), "CSV file should exist"

        with open(filepath, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)

        # Check for metadata rows (comments start with #)
        assert rows[0][0].startswith("#"), "First row should be metadata"

        # Find header row
        header_idx = None
        for i, row in enumerate(rows):
            if row and row[0] == "Step":
                header_idx = i
                break

        assert header_idx is not None, "Should have header row with 'Step'"

        header = rows[header_idx]
        assert "Intelligence" in header, "Should have Intelligence column"
        assert "A" in header, "Should have A column"
        assert "E_n" in header, "Should have E_n column"

        # Check data rows (should be 4 data rows)
        data_rows = [r for r in rows[header_idx+1:] if r and not r[0].startswith("#")]
        assert len(data_rows) >= 4, f"Should have at least 4 data rows, got {len(data_rows)}"

        # Verify first data row
        first_data = data_rows[0]
        assert first_data[0] == "0", "First step should be 0"

        print("✓ Basic CSV export")

    finally:
        if os.path.exists(filepath):
            os.unlink(filepath)


def test_export_to_csv_without_metadata():
    """Test CSV export without metadata."""
    result = create_mock_simulation_result(num_steps=2)

    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        filepath = f.name

    try:
        export_to_csv(result, filepath, include_metadata=False)

        with open(filepath, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)

        # First row should be header, not metadata
        assert rows[0][0] == "Step", "First row should be header when no metadata"

        print("✓ CSV export without metadata")

    finally:
        if os.path.exists(filepath):
            os.unlink(filepath)


def test_export_to_markdown_basic():
    """Test basic Markdown export functionality."""
    result = create_mock_simulation_result(num_steps=3)

    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        filepath = f.name

    try:
        export_to_markdown(result, filepath, title="Test Simulation", include_summary=True)

        assert os.path.exists(filepath), "Markdown file should exist"

        with open(filepath, 'r') as f:
            content = f.read()

        # Check title
        assert "# Test Simulation" in content, "Should have title"

        # Check metadata
        assert "**Total Steps:** 3" in content, "Should have step count"
        assert "**Export Time:**" in content, "Should have export time"

        # Check summary section
        assert "## Summary Statistics" in content, "Should have summary section"
        assert "| Metric | Value |" in content, "Should have summary table"

        # Check history section
        assert "## Simulation History" in content, "Should have history section"
        assert "| Step | Intelligence |" in content, "Should have history table header"

        # Check that all 3 steps are present
        lines = content.split('\n')
        step_lines = [l for l in lines if l.startswith('| 0 |') or l.startswith('| 1 |') or l.startswith('| 2 |')]
        assert len(step_lines) == 3, "Should have 3 step rows in table"

        print("✓ Basic Markdown export")

    finally:
        if os.path.exists(filepath):
            os.unlink(filepath)


def test_export_to_markdown_without_summary():
    """Test Markdown export without summary."""
    result = create_mock_simulation_result(num_steps=2)

    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        filepath = f.name

    try:
        export_to_markdown(result, filepath, include_summary=False)

        with open(filepath, 'r') as f:
            content = f.read()

        assert "## Summary Statistics" not in content, "Should not have summary section"
        assert "## Simulation History" in content, "Should still have history section"

        print("✓ Markdown export without summary")

    finally:
        if os.path.exists(filepath):
            os.unlink(filepath)


def test_export_to_markdown_with_max_rows():
    """Test Markdown export with row limit."""
    result = create_mock_simulation_result(num_steps=10)

    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        filepath = f.name

    try:
        export_to_markdown(result, filepath, max_rows=3)

        with open(filepath, 'r') as f:
            content = f.read()

        # Should have truncation message
        assert "more rows" in content.lower(), "Should indicate more rows available"

        # Count step rows in history table
        lines = content.split('\n')
        step_lines = [l for l in lines if l.startswith('| ') and not l.startswith('| Step |')
                     and not l.startswith('|--')]

        # Should have exactly max_rows in history section
        history_section = content.split("## Simulation History")[1] if "## Simulation History" in content else ""
        history_lines = [l for l in history_section.split('\n') if l.startswith('| ')
                        and not l.startswith('| Step |') and not l.startswith('|--')]

        assert len(history_lines) == 3, f"Should have exactly 3 rows, got {len(history_lines)}"

        print("✓ Markdown export with max_rows")

    finally:
        if os.path.exists(filepath):
            os.unlink(filepath)


def test_generate_report():
    """Test comprehensive report generation."""
    # Create multiple scenarios
    results = {
        "Growth": create_mock_simulation_result(num_steps=5),
        "Decline": create_mock_simulation_result(num_steps=5),
        "Stable": create_mock_simulation_result(num_steps=5),
    }

    # Modify scenarios to have different characteristics
    results["Decline"].summary["final_intelligence"] = 80.0
    results["Decline"].summary["total_growth_pct"] = -20.0
    results["Stable"].summary["volatility"] = 1.0

    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        filepath = f.name

    try:
        generate_report(
            results,
            filepath,
            title="Intelligence Analysis Report",
            description="Comparative analysis of scenarios"
        )

        assert os.path.exists(filepath), "Report file should exist"

        with open(filepath, 'r') as f:
            content = f.read()

        # Check title and description
        assert "# Intelligence Analysis Report" in content, "Should have title"
        assert "Comparative analysis of scenarios" in content, "Should have description"

        # Check executive summary
        assert "## Executive Summary" in content, "Should have executive summary"
        assert "Growth" in content, "Should mention Growth scenario"
        assert "Decline" in content, "Should mention Decline scenario"
        assert "Stable" in content, "Should mention Stable scenario"

        # Check detailed analysis sections
        assert "## Scenario: Growth" in content or "## Scenario:" in content, "Should have scenario sections"

        # Check for key metrics
        assert "Key Metrics" in content, "Should have key metrics section"
        assert "Parameter Evolution" in content, "Should have parameter evolution"
        assert "Bottleneck Analysis" in content, "Should have bottleneck analysis"

        # Check recommendations
        assert "## Recommendations" in content, "Should have recommendations"
        assert "Highest Intelligence" in content, "Should identify best performer"
        assert "Lowest Intelligence" in content, "Should identify worst performer"

        print("✓ Report generation")

    finally:
        if os.path.exists(filepath):
            os.unlink(filepath)


def test_export_comparison_csv():
    """Test CSV comparison export."""
    # Create multiple scenarios
    results = {
        "Scenario_A": create_mock_simulation_result(num_steps=3),
        "Scenario_B": create_mock_simulation_result(num_steps=3),
    }

    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        filepath = f.name

    try:
        export_comparison_csv(results, filepath)

        assert os.path.exists(filepath), "Comparison CSV should exist"

        with open(filepath, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)

        # Find header row
        header_idx = None
        for i, row in enumerate(rows):
            if row and row[0] == "Scenario":
                header_idx = i
                break

        assert header_idx is not None, "Should have header row"

        header = rows[header_idx]
        assert "Final Intelligence" in header, "Should have Final Intelligence column"
        assert "Growth %" in header, "Should have Growth % column"
        assert "Volatility" in header, "Should have Volatility column"

        # Check data rows (should have both scenarios)
        data_rows = [r for r in rows[header_idx+1:] if r and not r[0].startswith("#")]
        assert len(data_rows) == 2, f"Should have 2 scenario rows, got {len(data_rows)}"

        # Check scenario names are present
        scenario_names = [row[0] for row in data_rows]
        assert "Scenario_A" in scenario_names, "Should have Scenario_A"
        assert "Scenario_B" in scenario_names, "Should have Scenario_B"

        print("✓ Comparison CSV export")

    finally:
        if os.path.exists(filepath):
            os.unlink(filepath)


def test_export_to_json_large_simulation():
    """Test JSON export with larger simulation."""
    result = create_mock_simulation_result(num_steps=50)

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        filepath = f.name

    try:
        export_to_json(result, filepath)

        with open(filepath, 'r') as f:
            data = json.load(f)

        assert len(data["history"]) == 50, "Should have all 50 steps"
        assert data["metadata"]["total_steps"] == 50, "Metadata should show 50 steps"

        print("✓ Large simulation JSON export")

    finally:
        if os.path.exists(filepath):
            os.unlink(filepath)


def test_all_export_formats_data_consistency():
    """Test that all export formats contain consistent data."""
    result = create_mock_simulation_result(num_steps=3)

    with tempfile.TemporaryDirectory() as tmpdir:
        json_path = os.path.join(tmpdir, "test.json")
        csv_path = os.path.join(tmpdir, "test.csv")
        md_path = os.path.join(tmpdir, "test.md")

        # Export to all formats
        export_to_json(result, json_path)
        export_to_csv(result, csv_path, include_metadata=False)
        export_to_markdown(result, md_path)

        # Read JSON data
        with open(json_path, 'r') as f:
            json_data = json.load(f)

        # Read CSV data
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            csv_data = list(reader)

        # Read Markdown data
        with open(md_path, 'r') as f:
            md_content = f.read()

        # Verify data consistency
        assert len(json_data["history"]) == 3, "JSON should have 3 steps"
        assert len(csv_data) == 3, "CSV should have 3 steps"
        assert "| 0 |" in md_content and "| 1 |" in md_content and "| 2 |" in md_content, \
            "Markdown should show all 3 steps"

        # Check intelligence values match
        json_intel_0 = json_data["history"][0]["intelligence"]
        csv_intel_0 = float(csv_data[0]["Intelligence"])

        assert abs(json_intel_0 - csv_intel_0) < 0.001, \
            f"Intelligence values should match: JSON={json_intel_0}, CSV={csv_intel_0}"

        print("✓ Data consistency across formats")


if __name__ == "__main__":
    # Run all tests
    test_export_to_json_basic()
    test_export_to_json_without_summary()
    test_export_to_csv_basic()
    test_export_to_csv_without_metadata()
    test_export_to_markdown_basic()
    test_export_to_markdown_without_summary()
    test_export_to_markdown_with_max_rows()
    test_generate_report()
    test_export_comparison_csv()
    test_export_to_json_large_simulation()
    test_all_export_formats_data_consistency()

    print("\n✅ All exporter tests passed!")
