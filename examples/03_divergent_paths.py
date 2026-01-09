"""
Example 3: Divergent Paths - Two Systems Compared

Compares two systems starting from identical conditions:
- System A: Maintains objectivity, steady growth
- System B: Becomes subjective, volatile, eventually declines

Demonstrates how different update rules lead to vastly different outcomes.
"""
from engine.timesphere import TimeSphere, UpdateRules
from engine.state import AxiomInputs
from axiom.subjectivity_scale import label_x


def run_divergent_paths_scenario():
    """Compare two systems with different evolutionary paths."""

    print("=" * 70)
    print("SCENARIO 3: Divergent Paths - The Road Not Taken")
    print("=" * 70)

    # Identical starting conditions
    initial_inputs = AxiomInputs(
        A=0.6,
        B=0.6,
        C=0.6,
        X=0.6,
        Y=0.5,
        Z=0.6,
        E_n=3.0,
        F_n=1.0,
    )

    # ===== SYSTEM A: The Steady Path =====
    print("\n🔵 System A: Steady, objective growth")
    sphere_a = TimeSphere(
        initial_inputs=initial_inputs,
        metadata={"name": "System A - Steady Growth"},
    )

    # Steady improvement across all variables
    sphere_a.add_update_rule("A", lambda s, step: min(1.0, s.inputs.A + 0.03))
    sphere_a.add_update_rule("B", lambda s, step: min(1.0, s.inputs.B + 0.03))
    sphere_a.add_update_rule("C", lambda s, step: min(1.0, s.inputs.C + 0.02))
    sphere_a.add_update_rule("X", lambda s, step: min(1.0, s.inputs.X + 0.02))  # Increasing objectivity
    sphere_a.add_update_rule("Y", lambda s, step: min(1.0, s.inputs.Y + 0.04))
    sphere_a.add_update_rule("Z", lambda s, step: min(1.0, s.inputs.Z + 0.03))
    sphere_a.add_update_rule("E_n", UpdateRules.e_sequence_rule(a=1.15, b=0.3))
    sphere_a.add_update_rule("F_n", lambda s, step: s.inputs.F_n + 0.5)

    result_a = sphere_a.simulate(steps=15)

    # ===== SYSTEM B: The Volatile Path =====
    print("🔴 System B: Volatile, subjective, chaotic")
    sphere_b = TimeSphere(
        initial_inputs=initial_inputs,
        metadata={"name": "System B - Volatile Chaos"},
    )

    # Oscillating, degrading variables
    sphere_b.add_update_rule("A", UpdateRules.oscillate(amplitude=0.2, period=5, baseline=0.5))
    sphere_b.add_update_rule("B", UpdateRules.decay(rate=0.03, min_val=0.3, variable="B"))
    sphere_b.add_update_rule("C", lambda s, step: max(0.4, s.inputs.C - 0.01))
    sphere_b.add_update_rule("X", lambda s, step: max(0.2, s.inputs.X - 0.04))  # Increasing subjectivity
    sphere_b.add_update_rule("Y", UpdateRules.oscillate(amplitude=0.25, period=4, baseline=0.4))
    sphere_b.add_update_rule("Z", UpdateRules.decay(rate=0.04, min_val=0.3, variable="Z"))
    sphere_b.add_update_rule("E_n", lambda s, step: max(1.0, s.inputs.E_n * 0.95))  # Gradual energy loss
    sphere_b.add_update_rule("F_n", lambda s, step: max(0.0, s.inputs.F_n - 0.1))

    result_b = sphere_b.simulate(steps=15)

    # ===== COMPARISON =====
    print("\n" + "=" * 70)
    print("COMPARISON: Intelligence Over Time")
    print("=" * 70)
    print(
        f"{'Step':>4} | {'System A':>12} | {'A_X':>6} | {'A_ABC':>6} | "
        f"{'System B':>12} | {'B_X':>6} | {'B_ABC':>6} | {'Δ':>10}"
    )
    print("-" * 90)

    for i, (ts_a, ts_b) in enumerate(zip(result_a.steps, result_b.steps)):
        comp_a = ts_a.intelligence.components
        comp_b = ts_b.intelligence.components
        delta = ts_a.intelligence.score - ts_b.intelligence.score

        print(
            f"{i:4d} | {ts_a.intelligence.score:12.4f} | {comp_a['X']:6.3f} | {comp_a['ABC']:6.4f} | "
            f"{ts_b.intelligence.score:12.4f} | {comp_b['X']:6.3f} | {comp_b['ABC']:6.4f} | "
            f"{delta:+10.4f}"
        )

    # Summary comparison
    print("\n" + "=" * 70)
    print("FINAL OUTCOMES")
    print("=" * 70)

    print(f"\nSystem A (Steady Path):")
    print(f"  Final Intelligence: {result_a.summary['final_intelligence']:.4f}")
    print(f"  Growth Rate: {result_a.summary['growth_rate']:+.1%}")
    print(f"  Peak Intelligence: {result_a.summary['max_intelligence']:.4f}")
    final_a_x = result_a.steps[-1].intelligence.components["X"]
    print(f"  Final Objectivity: {final_a_x:.3f} ({label_x(final_a_x)})")

    print(f"\nSystem B (Volatile Path):")
    print(f"  Final Intelligence: {result_b.summary['final_intelligence']:.4f}")
    print(f"  Growth Rate: {result_b.summary['growth_rate']:+.1%}")
    print(f"  Peak Intelligence: {result_b.summary['max_intelligence']:.4f}")
    final_b_x = result_b.steps[-1].intelligence.components["X"]
    print(f"  Final Subjectivity: {final_b_x:.3f} ({label_x(final_b_x)})")

    # Calculate divergence
    divergence = result_a.summary["final_intelligence"] - result_b.summary["final_intelligence"]
    divergence_pct = (divergence / result_b.summary["final_intelligence"]) * 100

    print(f"\nDivergence:")
    print(f"  Absolute: {divergence:.4f}")
    print(f"  Relative: {divergence_pct:.1f}%")
    print(f"  Winner: {'System A' if divergence > 0 else 'System B'}")

    print("\n" + "=" * 70)
    print("Key Insight: Initial conditions matter less than update rules.")
    print("Sustained objectivity + steady growth >> volatile shortcuts.")
    print("Small differences in X (objectivity) compound dramatically.")
    print("=" * 70 + "\n")

    return {"system_a": result_a, "system_b": result_b}


if __name__ == "__main__":
    run_divergent_paths_scenario()
