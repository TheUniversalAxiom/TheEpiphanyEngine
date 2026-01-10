"""
Example 6: Innovation Cycles Scenario

Models a team iterating through experimentation cycles:
- Foundations steadily improve (A, B, C)
- Output quality oscillates during experimentation (Y, Z)
- Objectivity stabilizes after noisy exploration (X)
- Energy and feedback loops accelerate iteration
"""
from engine.timesphere import TimeSphere, UpdateRules
from engine.state import AxiomInputs


def run_innovation_cycles_scenario():
    """Simulate innovation cycles with oscillating performance."""

    print("=" * 60)
    print("SCENARIO 6: Innovation Cycles - Experimentation to Breakthrough")
    print("=" * 60)

    initial_inputs = AxiomInputs(
        A=0.65,
        B=0.55,
        C=0.6,
        X=0.5,
        Y=0.45,
        Z=0.5,
        E_n=2.5,
        F_n=0.5,
    )

    sphere = TimeSphere(
        initial_inputs=initial_inputs,
        metadata={"scenario": "innovation_cycles", "subject": "product_team"},
    )

    sphere.add_update_rule("A", UpdateRules.linear_growth(rate=0.04, variable="A"))
    sphere.add_update_rule("B", UpdateRules.linear_growth(rate=0.05, variable="B"))
    sphere.add_update_rule("C", UpdateRules.linear_growth(rate=0.03, variable="C"))
    sphere.add_update_rule("X", UpdateRules.linear_growth(rate=0.04, variable="X"))

    sphere.add_update_rule("Y", UpdateRules.oscillate(amplitude=0.25, period=6, baseline=0.55))
    sphere.add_update_rule("Z", UpdateRules.oscillate(amplitude=0.2, period=6, baseline=0.6))

    sphere.add_update_rule("E_n", UpdateRules.e_sequence_rule(a=1.15, b=0.4))
    sphere.add_update_rule("F_n", UpdateRules.fibonacci_rule())

    def detect_innovation_events(state, step):
        if state.inputs.Y > 0.8 and state.inputs.X > 0.7:
            return "🚀 Breakthrough: High yield with clarity"
        if state.inputs.Y < 0.4 and step > 0:
            return "🧪 Experimentation dip: Learning from failures"
        return None

    sphere.add_event_handler(detect_innovation_events)

    result = sphere.simulate(steps=12)

    print(f"\nSimulation completed: {result.summary['total_steps']} steps")
    print(f"\nInnovation Trajectory:")
    print(f"  Initial: {result.summary['initial_intelligence']:.4f}")
    print(f"  Final:   {result.summary['final_intelligence']:.4f}")
    print(f"  Growth:  {result.summary['growth_rate']:.1%}")
    print(f"  Peak:    {result.summary['max_intelligence']:.4f}")

    print(f"\nCycle View:")
    print(
        f"{'Step':>4} | {'I_n':>10} | {'A':>5} | {'X':>5} | {'Y':>5} | {'Z':>5} | {'F_n':>6} | Events"
    )
    print("-" * 90)

    for ts in result.steps:
        comp = ts.intelligence.components
        events_str = " | ".join(ts.events) if ts.events else ""
        print(
            f"{ts.step:4d} | {ts.intelligence.score:10.4f} | "
            f"{comp['A']:5.3f} | {comp['X']:5.3f} | {comp['Y']:5.3f} | "
            f"{comp['Z']:5.3f} | {comp['F_n']:6.1f} | {events_str}"
        )

    trends = sphere.analyze_trends()
    print(f"\nTrend Analysis:")
    print(f"  Overall trend: {trends['trend']}")
    print(f"  Total events: {trends['total_events']}")
    print(f"  Volatility: {trends['score_volatility']:.4f}")

    print("\n" + "=" * 60)
    print("Key Insight: Oscillation in output is normal during innovation,")
    print("but steady alignment and clarity enable compounding gains.")
    print("=" * 60 + "\n")

    return result


if __name__ == "__main__":
    run_innovation_cycles_scenario()
