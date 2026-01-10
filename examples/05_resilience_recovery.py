"""
Example 5: Resilience and Recovery Scenario

Models a system that experiences a shock event but regains strength through
re-alignment, process improvements, and renewed energy.
"""
from engine.timesphere import TimeSphere, UpdateRules
from engine.state import AxiomInputs


def shock_then_recover(variable, *, shock_step, drop_factor, recovery_rate, min_val=0.0, max_val=1.0):
    """Apply a one-time shock, then steady recovery."""

    def rule(state, step):
        current = getattr(state.inputs, variable)
        if step == shock_step:
            return max(min_val, current * drop_factor)
        return min(max_val, current + recovery_rate)

    return rule


def run_resilience_recovery_scenario():
    """Simulate a shock followed by a resilient recovery."""

    print("=" * 60)
    print("SCENARIO 5: Resilience & Recovery - The Comeback")
    print("=" * 60)

    initial_inputs = AxiomInputs(
        A=0.75,
        B=0.6,
        C=0.65,
        X=0.7,
        Y=0.55,
        Z=0.6,
        E_n=3.5,
        F_n=1.0,
    )

    sphere = TimeSphere(
        initial_inputs=initial_inputs,
        metadata={"scenario": "resilience_recovery", "subject": "adaptive_team"},
    )

    shock_step = 4

    sphere.add_update_rule(
        "A",
        shock_then_recover("A", shock_step=shock_step, drop_factor=0.7, recovery_rate=0.05),
    )
    sphere.add_update_rule(
        "B",
        shock_then_recover("B", shock_step=shock_step, drop_factor=0.65, recovery_rate=0.06),
    )
    sphere.add_update_rule(
        "C",
        shock_then_recover("C", shock_step=shock_step, drop_factor=0.85, recovery_rate=0.03),
    )
    sphere.add_update_rule(
        "X",
        shock_then_recover("X", shock_step=shock_step, drop_factor=0.8, recovery_rate=0.04),
    )
    sphere.add_update_rule(
        "Y",
        shock_then_recover("Y", shock_step=shock_step, drop_factor=0.6, recovery_rate=0.08),
    )
    sphere.add_update_rule(
        "Z",
        shock_then_recover("Z", shock_step=shock_step, drop_factor=0.6, recovery_rate=0.07),
    )

    def energy_rule(state, step):
        if step == shock_step:
            return max(1.0, state.inputs.E_n * 0.6)
        return state.inputs.E_n + 0.5

    sphere.add_update_rule("E_n", energy_rule)
    sphere.add_update_rule("F_n", lambda s, step: s.inputs.F_n + 0.4)

    def detect_recovery_events(state, step):
        if step == shock_step:
            return "💥 Shock event: External disruption"
        if step > shock_step and state.inputs.A * state.inputs.B * state.inputs.C > 0.5:
            return "🛡️ Resilience milestone: Foundation restored"
        if state.inputs.Y > 0.8 and step > shock_step:
            return "🌱 Recovery milestone: High yield regained"
        return None

    sphere.add_event_handler(detect_recovery_events)

    result = sphere.simulate(steps=10)

    print(f"\nSimulation completed: {result.summary['total_steps']} steps")
    print(f"\nResilience Arc:")
    print(f"  Initial: {result.summary['initial_intelligence']:.4f}")
    print(f"  Final:   {result.summary['final_intelligence']:.4f}")
    print(f"  Growth:  {result.summary['growth_rate']:.1%}")
    print(f"  Peak:    {result.summary['max_intelligence']:.4f}")

    print(f"\nStep-by-Step Recovery:")
    print(
        f"{'Step':>4} | {'I_n':>10} | {'ABC':>6} | {'XYZ':>6} | {'E_n':>6} | {'F_n':>6} | Events"
    )
    print("-" * 80)

    for ts in result.steps:
        comp = ts.intelligence.components
        events_str = " | ".join(ts.events) if ts.events else ""
        print(
            f"{ts.step:4d} | {ts.intelligence.score:10.4f} | "
            f"{comp['ABC']:6.3f} | {comp['XYZ']:6.3f} | "
            f"{comp['E_n']:6.2f} | {comp['F_n']:6.1f} | {events_str}"
        )

    trends = sphere.analyze_trends()
    print(f"\nTrend Analysis:")
    print(f"  Overall trend: {trends['trend']}")
    print(f"  Total events: {trends['total_events']}")
    print(f"  Volatility: {trends['score_volatility']:.4f}")

    print("\n" + "=" * 60)
    print("Key Insight: Resilience comes from restoring alignment and")
    print("capability quickly after shocks, preventing long-term decay.")
    print("=" * 60 + "\n")

    return result


if __name__ == "__main__":
    run_resilience_recovery_scenario()
