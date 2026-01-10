"""
Master runner for all EPIPHANY examples.

Executes all example scenarios and provides a comprehensive overview
of the framework's capabilities.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import importlib.util


def load_module_from_file(filepath, module_name):
    """Load a module from a file path."""
    spec = importlib.util.spec_from_file_location(module_name, filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Load example modules
example_dir = Path(__file__).parent
basic_growth = load_module_from_file(example_dir / "01_basic_growth.py", "basic_growth")
corruption = load_module_from_file(example_dir / "02_corruption_decay.py", "corruption")
divergent = load_module_from_file(example_dir / "03_divergent_paths.py", "divergent")
ai_alignment = load_module_from_file(example_dir / "04_ai_alignment.py", "ai_alignment")
resilience = load_module_from_file(example_dir / "05_resilience_recovery.py", "resilience")
innovation = load_module_from_file(example_dir / "06_innovation_cycles.py", "innovation")

run_basic_growth_scenario = basic_growth.run_basic_growth_scenario
run_corruption_scenario = corruption.run_corruption_scenario
run_divergent_paths_scenario = divergent.run_divergent_paths_scenario
run_ai_alignment_scenario = ai_alignment.run_ai_alignment_scenario
run_resilience_recovery_scenario = resilience.run_resilience_recovery_scenario
run_innovation_cycles_scenario = innovation.run_innovation_cycles_scenario


def main():
    """Run all example scenarios."""
    print("\n" + "╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "EPIPHANY ENGINE - EXAMPLE SUITE" + " " * 22 + "║")
    print("║" + " " * 10 + "The Universal Axiom Organic Intelligence Model" + " " * 11 + "║")
    print("╚" + "=" * 68 + "╝\n")

    scenarios = [
        ("Basic Growth", run_basic_growth_scenario),
        ("Corruption & Decay", run_corruption_scenario),
        ("Divergent Paths", run_divergent_paths_scenario),
        ("AI Alignment", run_ai_alignment_scenario),
        ("Resilience & Recovery", run_resilience_recovery_scenario),
        ("Innovation Cycles", run_innovation_cycles_scenario),
    ]

    results = {}

    for name, scenario_func in scenarios:
        try:
            print(f"\n{'🔹' * 35}")
            print(f"Running: {name}")
            print(f"{'🔹' * 35}\n")
            result = scenario_func()
            results[name] = {"status": "success", "result": result}
            print(f"\n✅ {name} completed successfully\n")
        except Exception as e:
            print(f"\n❌ {name} failed: {e}\n")
            results[name] = {"status": "failed", "error": str(e)}

    # Summary
    print("\n" + "╔" + "=" * 68 + "╗")
    print("║" + " " * 25 + "EXECUTION SUMMARY" + " " * 26 + "║")
    print("╚" + "=" * 68 + "╝\n")

    success_count = sum(1 for r in results.values() if r["status"] == "success")
    total_count = len(results)

    for name, result in results.items():
        status_icon = "✅" if result["status"] == "success" else "❌"
        print(f"  {status_icon} {name}")

    print(f"\nResults: {success_count}/{total_count} scenarios completed successfully")

    if success_count == total_count:
        print("\n🎉 All examples executed successfully!")
        print("\nThe EPIPHANY Engine demonstrates:")
        print("  • Intelligence as a computable, measurable quantity")
        print("  • Time-evolution dynamics through TimeSphere")
        print("  • Corruption detection via subjectivity metrics")
        print("  • Multi-factor analysis (A·B·C × X·Y·Z × E_n·F_n)")
        print("  • Practical applications to AI, organizations, and individuals")
    else:
        print(f"\n⚠️  {total_count - success_count} scenario(s) failed")

    print("\n" + "=" * 70 + "\n")

    return results


if __name__ == "__main__":
    main()
