"""
Example 1: Basic Growth Scenario

Models a learner developing intelligence over time through:
- Steady improvement in foundational values (A, B, C)
- Maintaining objectivity (X stays high)
- Increasing capability and output (Y, Z growth)
- Energy and feedback growing over time
"""
from engine.state import AxiomInputs
from engine.timesphere import TimeSphere, UpdateRules


def run_basic_growth_scenario():
    """Simulate a learner's intelligence growth over 10 time steps."""

    print("=" * 60)
    print("SCENARIO 1: Basic Growth - A Learner's Journey")
    print("=" * 60)

    # Initial state: Beginner with solid foundation but low skills
    initial_inputs = AxiomInputs(
        A=0.6,  # Moderate alignment with truth
        B=0.4,  # Limited behaviors/skills
        C=0.5,  # Medium capacity for growth
        X=0.7,  # Fairly objective perspective
        Y=0.3,  # Low output/yield initially
        Z=0.5,  # Medium accuracy/zero-error
        E_n=2.0,  # Starting energy
        F_n=0.0,  # No feedback loops yet
    )

    # Create TimeSphere
    sphere = TimeSphere(
        initial_inputs=initial_inputs,
        metadata={"scenario": "basic_growth", "subject": "eager_learner"},
    )

    # Define evolution rules
    # A, B, C gradually improve (learning)
    sphere.add_update_rule("A", lambda s, step: min(1.0, s.inputs.A + 0.03))
    sphere.add_update_rule("B", lambda s, step: min(1.0, s.inputs.B + 0.05))
    sphere.add_update_rule("C", lambda s, step: min(1.0, s.inputs.C + 0.04))

    # X stays high (maintains objectivity)
    sphere.add_update_rule("X", lambda s, step: min(1.0, s.inputs.X + 0.01))

    # Y and Z improve as skills develop
    sphere.add_update_rule("Y", lambda s, step: min(1.0, s.inputs.Y + 0.06))
    sphere.add_update_rule("Z", lambda s, step: min(1.0, s.inputs.Z + 0.04))

    # E_n grows with momentum
    sphere.add_update_rule("E_n", UpdateRules.e_sequence_rule(a=1.2, b=0.5))

    # F_n grows as feedback loops establish
    sphere.add_update_rule("F_n", lambda s, step: float(step))

    # Add event detection
    def milestone_message(state, step):
        score_estimate = state.inputs.A * state.inputs.B * state.inputs.C
        if score_estimate > 0.5 and step > 0:
            prev_estimate = 0.5  # simplified check
            if score_estimate > prev_estimate and step == 5:
                return "🎯 Milestone: Crossed foundation threshold (ABC > 0.5)"
        if state.inputs.Y > 0.8 and step > 0:
            if step == 9:
                return "🚀 Milestone: High yield achieved (Y > 0.8)"
        return None

    sphere.add_event_handler(
        lambda state, step: milestone_message(state, step) is not None,
        milestone_message,
    )

    # Run simulation
    result = sphere.simulate(steps=10)

    # Display results
    print(f"\nSimulation completed: {result.summary['total_steps']} steps")
    print("\nIntelligence Growth:")
    print(f"  Initial: {result.summary['initial_intelligence']:.4f}")
    print(f"  Final:   {result.summary['final_intelligence']:.4f}")
    print(f"  Growth:  {result.summary['growth_rate']:.1%}")
    print(f"  Peak:    {result.summary['max_intelligence']:.4f}")

    print("\nStep-by-Step Evolution:")
    print(f"{'Step':>4} | {'I_n':>10} | {'ABC':>6} | {'XYZ':>6} | {'E_n':>6} | {'F_n':>6} | Events")
    print("-" * 80)

    for ts in result.steps:
        comp = ts.intelligence.components
        events_str = " | ".join(ts.events) if ts.events else ""
        print(
            f"{ts.step:4d} | {ts.intelligence.score:10.4f} | "
            f"{comp['ABC']:6.3f} | {comp['XYZ']:6.3f} | "
            f"{comp['E_n']:6.2f} | {comp['F_n']:6.1f} | {events_str}"
        )

    # Analyze trends
    trends = sphere.analyze_trends()
    print("\nTrend Analysis:")
    print(f"  Overall trend: {trends['trend']}")
    print(f"  Total events: {trends['total_events']}")
    print(f"  Volatility: {trends['score_volatility']:.4f}")

    print("\n" + "=" * 60)
    print("Key Insight: Consistent improvement in all variables leads")
    print("to exponential intelligence growth due to multiplicative effects.")
    print("=" * 60 + "\n")

    return result


if __name__ == "__main__":
    run_basic_growth_scenario()
