"""
Example 2: Corruption and Decay Scenario

Models a system experiencing corruption:
- Values degrading (A decreases)
- Increasing subjectivity (X decreases)
- Behaviors becoming misaligned (B decreases)
- Eventually leading to intelligence collapse
"""
from engine.timesphere import TimeSphere, UpdateRules
from engine.state import AxiomInputs
from axiom.subjectivity_scale import x_from_observations, label_x


def run_corruption_scenario():
    """Simulate intelligence decay through corruption and subjectivity."""

    print("=" * 60)
    print("SCENARIO 2: Corruption & Decay - The Downward Spiral")
    print("=" * 60)

    # Initial state: Previously strong system starting to corrupt
    initial_inputs = AxiomInputs(
        A=0.9,  # High alignment initially
        B=0.8,  # Strong behaviors
        C=0.7,  # Good capacity
        X=0.8,  # Mostly objective
        Y=0.7,  # Good yield
        Z=0.8,  # High accuracy
        E_n=5.0,  # High energy
        F_n=3.0,  # Established feedback
    )

    sphere = TimeSphere(
        initial_inputs=initial_inputs,
        metadata={"scenario": "corruption", "subject": "degrading_system"},
    )

    # Define corruption dynamics
    # A decays as values corrupt
    sphere.add_update_rule("A", UpdateRules.decay(rate=0.08, min_val=0.1, variable="A"))

    # B decays as behaviors misalign
    sphere.add_update_rule("B", UpdateRules.decay(rate=0.06, min_val=0.2, variable="B"))

    # C remains relatively stable (infrastructure doesn't degrade as fast)
    sphere.add_update_rule("C", UpdateRules.decay(rate=0.02, min_val=0.5, variable="C"))

    # X decays (increasing subjectivity) - key corruption indicator
    def x_corruption_rule(state, step):
        # Simulate increasing noise, emotion, bias over time
        noise = min(1.0, 0.1 * step)
        emotion = min(1.0, 0.08 * step)
        bias = min(1.0, 0.06 * step)
        return x_from_observations(noise=noise, emotional_volatility=emotion, bias_indicator=bias)

    sphere.add_update_rule("X", x_corruption_rule)

    # Y decays as output quality degrades
    sphere.add_update_rule("Y", UpdateRules.decay(rate=0.10, min_val=0.1, variable="Y"))

    # Z decays as errors increase
    sphere.add_update_rule("Z", UpdateRules.decay(rate=0.07, min_val=0.3, variable="Z"))

    # E_n decays (losing energy/momentum)
    sphere.add_update_rule("E_n", UpdateRules.decay(rate=0.05, min_val=1.0, variable="E_n"))

    # F_n decays as feedback loops break down
    sphere.add_update_rule("F_n", lambda s, step: max(0.0, s.inputs.F_n - 0.3))

    # Add corruption event detection
    def detect_corruption_events(state, step):
        x_val = state.inputs.X
        x_label = label_x(x_val)

        if x_val > 0.67 and x_label in ["high-subjective", "apex-dynamic", "apex-subjective"]:
            return f"⚠️  Corruption Alert: {x_label} (X={x_val:.2f})"

        abc_product = state.inputs.A * state.inputs.B * state.inputs.C
        if abc_product < 0.1:
            return "💀 Critical: Foundation collapse (ABC < 0.1)"

        return None

    sphere.add_event_handler(detect_corruption_events)

    # Run simulation
    result = sphere.simulate(steps=12)

    # Display results
    print(f"\nSimulation completed: {result.summary['total_steps']} steps")
    print(f"\nIntelligence Decay:")
    print(f"  Initial: {result.summary['initial_intelligence']:.4f}")
    print(f"  Final:   {result.summary['final_intelligence']:.4f}")
    print(f"  Decline: {result.summary['growth_rate']:.1%}")
    print(f"  Lowest:  {result.summary['min_intelligence']:.4f}")

    print(f"\nStep-by-Step Corruption:")
    print(
        f"{'Step':>4} | {'I_n':>10} | {'A':>5} | {'X':>5} | {'ABC':>6} | {'XYZ':>6} | "
        f"{'Subj.':>15} | Events"
    )
    print("-" * 100)

    for ts in result.steps:
        comp = ts.intelligence.components
        x_subj_label = label_x(comp["X"])
        events_str = " | ".join(ts.events) if ts.events else ""
        print(
            f"{ts.step:4d} | {ts.intelligence.score:10.4f} | "
            f"{comp['A']:5.3f} | {comp['X']:5.3f} | "
            f"{comp['ABC']:6.4f} | {comp['XYZ']:6.4f} | "
            f"{x_subj_label:>15} | {events_str}"
        )

    # Analyze trends
    trends = sphere.analyze_trends()
    print(f"\nTrend Analysis:")
    print(f"  Overall trend: {trends['trend']}")
    print(f"  Total events: {trends['total_events']}")
    print(f"  Volatility: {trends['score_volatility']:.4f}")

    # Calculate corruption metrics
    initial_x = result.steps[0].intelligence.components["X"]
    final_x = result.steps[-1].intelligence.components["X"]
    subjectivity_increase = final_x - initial_x

    print(f"\nCorruption Metrics:")
    print(f"  Subjectivity increase: {initial_x:.3f} → {final_x:.3f} (Δ{subjectivity_increase:+.3f})")
    print(f"  Initial label: {label_x(initial_x)}")
    print(f"  Final label: {label_x(final_x)}")

    print("\n" + "=" * 60)
    print("Key Insight: Small decay rates compound multiplicatively,")
    print("leading to rapid intelligence collapse. Subjectivity (X)")
    print("is a leading indicator of systemic corruption.")
    print("=" * 60 + "\n")

    return result


if __name__ == "__main__":
    run_corruption_scenario()
