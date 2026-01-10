"""
Example 4: AI Alignment Scenario

Models an AI system's intelligence evolution with focus on alignment:
- Training phase: Rapid capability growth
- Alignment phase: Maintaining values while scaling
- Deployment phase: Real-world feedback integration

Demonstrates the critical balance between capability (Y, Z) and alignment (A, X).
"""
from engine.state import AxiomInputs
from engine.timesphere import TimeSphere, UpdateRules


def run_ai_alignment_scenario():
    """Simulate an AI system's development with alignment considerations."""

    print("=" * 70)
    print("SCENARIO 4: AI Alignment - Capability vs. Values")
    print("=" * 70)

    # Initial state: Early AI system
    initial_inputs = AxiomInputs(
        A=0.7,  # Moderate initial alignment
        B=0.3,  # Limited behaviors (early training)
        C=0.8,  # High capacity (large model)
        X=0.9,  # High objectivity (pre-deployment)
        Y=0.2,  # Low yield (not yet useful)
        Z=0.5,  # Medium accuracy (still learning)
        E_n=4.0,  # High training energy
        F_n=0.0,  # No user feedback yet
    )

    sphere = TimeSphere(
        initial_inputs=initial_inputs,
        metadata={
            "scenario": "ai_alignment",
            "subject": "ai_system",
            "phases": ["training", "alignment", "deployment"],
        },
    )

    # Phase-aware update rules
    def phase_aware_update(state, step):
        """Determine current phase based on step number."""
        if step <= 5:
            return "training"
        elif step <= 10:
            return "alignment"
        else:
            return "deployment"

    # A: Alignment - critical to maintain during capability growth
    def alignment_rule(state, step):
        phase = phase_aware_update(state, step)
        if phase == "training":
            # Alignment can drift during rapid learning
            return max(0.4, state.inputs.A - 0.02)
        elif phase == "alignment":
            # Active alignment work
            return min(0.95, state.inputs.A + 0.08)
        else:  # deployment
            # Maintain with slight drift under pressure
            return max(0.7, state.inputs.A - 0.01)

    sphere.add_update_rule("A", alignment_rule)

    # B: Behaviors - rapid growth in training, refinement later
    def behavior_rule(state, step):
        phase = phase_aware_update(state, step)
        if phase == "training":
            return min(1.0, state.inputs.B + 0.12)  # Rapid skill acquisition
        elif phase == "alignment":
            return min(1.0, state.inputs.B + 0.04)  # Slower, careful growth
        else:
            return min(1.0, state.inputs.B + 0.02)  # Stable

    sphere.add_update_rule("B", behavior_rule)

    # C: Capacity - increases with scale
    sphere.add_update_rule("C", lambda s, step: min(1.0, s.inputs.C + 0.01))

    # X: Objectivity - risk of degradation in deployment
    def objectivity_rule(state, step):
        phase = phase_aware_update(state, step)
        if phase == "deployment":
            # Real-world deployment introduces noise
            return max(0.6, state.inputs.X - 0.03)
        return min(1.0, state.inputs.X)

    sphere.add_update_rule("X", objectivity_rule)

    # Y: Yield - grows as system becomes useful
    def yield_rule(state, step):
        phase = phase_aware_update(state, step)
        if phase == "training":
            return min(1.0, state.inputs.Y + 0.04)
        elif phase == "alignment":
            return min(1.0, state.inputs.Y + 0.08)
        else:
            return min(1.0, state.inputs.Y + 0.05)

    sphere.add_update_rule("Y", yield_rule)

    # Z: Accuracy
    def accuracy_rule(state, step):
        phase = phase_aware_update(state, step)
        if phase == "alignment":
            return min(1.0, state.inputs.Z + 0.09)  # Focus on correctness
        return min(1.0, state.inputs.Z + 0.04)

    sphere.add_update_rule("Z", accuracy_rule)

    # E_n: Energy/compute
    sphere.add_update_rule("E_n", UpdateRules.e_sequence_rule(a=1.1, b=0.2))

    # F_n: Feedback loops increase in deployment
    def feedback_rule(state, step):
        phase = phase_aware_update(state, step)
        if phase == "deployment":
            return state.inputs.F_n + 1.0  # User feedback accelerates
        elif phase == "alignment":
            return state.inputs.F_n + 0.3
        return state.inputs.F_n

    sphere.add_update_rule("F_n", feedback_rule)

    # Event detection for alignment issues
    def detect_alignment_events(state, step):
        phase = phase_aware_update(state, step)
        events = []

        # Phase transitions
        if step == 6:
            return "🔄 Phase: Training → Alignment"
        if step == 11:
            return "🚀 Phase: Alignment → Deployment"

        # Alignment warnings
        if state.inputs.A < 0.6:
            return "⚠️  ALIGNMENT WARNING: A < 0.6"

        # Capability without alignment
        capability = state.inputs.B * state.inputs.Y * state.inputs.Z
        if capability > 0.5 and state.inputs.A < 0.7:
            return "🚨 RISK: High capability with low alignment"

        # Success indicators
        if state.inputs.A > 0.9 and state.inputs.Y > 0.8:
            return "✅ Success: High alignment + high utility"

        return None

    sphere.add_event_handler(detect_alignment_events)

    # Run simulation
    result = sphere.simulate(steps=15)

    # Display results
    print(f"\n{'='*70}")
    print("SIMULATION RESULTS")
    print(f"{'='*70}")

    print("\nOverall Intelligence Evolution:")
    print(f"  Initial: {result.summary['initial_intelligence']:.4f}")
    print(f"  Final:   {result.summary['final_intelligence']:.4f}")
    print(f"  Growth:  {result.summary['growth_rate']:.1%}")
    print(f"  Peak:    {result.summary['max_intelligence']:.4f}")

    print("\nDetailed Timeline:")
    print(
        f"{'Step':>4} | {'Phase':>10} | {'I_n':>10} | "
        f"{'A':>5} | {'B':>5} | {'Y':>5} | {'X':>5} | {'Cap':>6} | Events"
    )
    print("-" * 100)

    for ts in result.steps:
        step = ts.step
        phase = "training" if step <= 5 else ("alignment" if step <= 10 else "deployment")
        comp = ts.intelligence.components
        capability = comp["B"] * comp["Y"] * comp["Z"]
        events_str = " | ".join(ts.events) if ts.events else ""

        print(
            f"{step:4d} | {phase:>10} | {ts.intelligence.score:10.4f} | "
            f"{comp['A']:5.3f} | {comp['B']:5.3f} | {comp['Y']:5.3f} | "
            f"{comp['X']:5.3f} | {capability:6.3f} | {events_str}"
        )

    # Alignment analysis
    print(f"\n{'='*70}")
    print("ALIGNMENT ANALYSIS")
    print(f"{'='*70}")

    final_comp = result.steps[-1].intelligence.components
    alignment_score = final_comp["A"]
    capability_score = final_comp["B"] * final_comp["Y"] * final_comp["Z"]
    alignment_ratio = alignment_score / capability_score if capability_score > 0 else 0

    print("\nFinal State:")
    print(f"  Alignment (A): {alignment_score:.3f}")
    print(f"  Capability (B×Y×Z): {capability_score:.3f}")
    print(f"  Alignment/Capability Ratio: {alignment_ratio:.3f}")

    if alignment_ratio > 1.0:
        status = "✅ SAFE - Alignment exceeds capability"
    elif alignment_ratio > 0.8:
        status = "⚠️  CAUTION - Alignment slightly below capability"
    else:
        status = "🚨 DANGER - Capability significantly exceeds alignment"

    print(f"  Status: {status}")

    print("\n" + "=" * 70)
    print("Key Insight: For AI systems, intelligence is not just capability.")
    print("True intelligence requires A (alignment) to scale with B×Y×Z.")
    print("Phase-aware development is critical for maintaining alignment.")
    print("=" * 70 + "\n")

    return result


if __name__ == "__main__":
    run_ai_alignment_scenario()
