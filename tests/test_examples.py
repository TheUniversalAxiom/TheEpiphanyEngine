"""
Tests inspired by example scenarios.
"""
import sys

from axiom.subjectivity_scale import x_from_observations
from engine.state import AxiomInputs
from engine.timesphere import TimeSphere, UpdateRules


def test_basic_growth_scenario_behavior():
    """Basic growth should increase intelligence over time."""
    initial_inputs = AxiomInputs(
        A=0.6,
        B=0.4,
        C=0.5,
        X=0.7,
        Y=0.3,
        Z=0.5,
        E_n=2.0,
        F_n=0.0,
    )
    sphere = TimeSphere(initial_inputs=initial_inputs)
    sphere.add_update_rule("A", lambda s, step: min(1.0, s.inputs.A + 0.03))
    sphere.add_update_rule("B", lambda s, step: min(1.0, s.inputs.B + 0.05))
    sphere.add_update_rule("C", lambda s, step: min(1.0, s.inputs.C + 0.04))
    sphere.add_update_rule("X", lambda s, step: min(1.0, s.inputs.X + 0.01))
    sphere.add_update_rule("Y", lambda s, step: min(1.0, s.inputs.Y + 0.06))
    sphere.add_update_rule("Z", lambda s, step: min(1.0, s.inputs.Z + 0.04))
    sphere.add_update_rule("E_n", UpdateRules.e_sequence_rule(a=1.2, b=0.5))
    sphere.add_update_rule("F_n", lambda s, step: float(step))

    result = sphere.simulate(steps=10)

    assert result.summary["final_intelligence"] > result.summary["initial_intelligence"]
    assert result.summary["growth_rate"] > 0
    print("✓ Basic growth scenario behavior")


def test_corruption_decay_scenario_behavior():
    """Corruption/decay should reduce intelligence and objectivity."""
    initial_inputs = AxiomInputs(
        A=0.9,
        B=0.8,
        C=0.7,
        X=0.8,
        Y=0.7,
        Z=0.8,
        E_n=5.0,
        F_n=3.0,
    )
    sphere = TimeSphere(initial_inputs=initial_inputs)
    sphere.add_update_rule("A", UpdateRules.decay(rate=0.08, min_value=0.1, variable="A"))
    sphere.add_update_rule("B", UpdateRules.decay(rate=0.06, min_value=0.2, variable="B"))
    sphere.add_update_rule("C", UpdateRules.decay(rate=0.02, min_value=0.5, variable="C"))

    def x_corruption_rule(state, step):
        noise = min(1.0, 0.1 * step)
        emotion = min(1.0, 0.08 * step)
        bias = min(1.0, 0.06 * step)
        return x_from_observations(noise=noise, emotional_volatility=emotion, bias_indicator=bias)

    sphere.add_update_rule("X", x_corruption_rule)
    sphere.add_update_rule("Y", UpdateRules.decay(rate=0.10, min_value=0.1, variable="Y"))
    sphere.add_update_rule("Z", UpdateRules.decay(rate=0.07, min_value=0.3, variable="Z"))
    sphere.add_update_rule("E_n", UpdateRules.decay(rate=0.05, min_value=1.0, variable="E_n"))
    sphere.add_update_rule("F_n", lambda s, step: max(0.0, s.inputs.F_n - 0.3))

    result = sphere.simulate(steps=12)

    initial_x = result.steps[0].intelligence.components["X"]
    final_x = result.steps[-1].intelligence.components["X"]
    assert result.summary["final_intelligence"] < result.summary["initial_intelligence"]
    assert final_x > initial_x
    print("✓ Corruption/decay scenario behavior")


def test_divergent_paths_behavior():
    """Steady path should outpace volatile path."""
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

    sphere_a = TimeSphere(initial_inputs=initial_inputs)
    sphere_a.add_update_rule("A", lambda s, step: min(1.0, s.inputs.A + 0.03))
    sphere_a.add_update_rule("B", lambda s, step: min(1.0, s.inputs.B + 0.03))
    sphere_a.add_update_rule("C", lambda s, step: min(1.0, s.inputs.C + 0.02))
    sphere_a.add_update_rule("X", lambda s, step: min(1.0, s.inputs.X + 0.02))
    sphere_a.add_update_rule("Y", lambda s, step: min(1.0, s.inputs.Y + 0.04))
    sphere_a.add_update_rule("Z", lambda s, step: min(1.0, s.inputs.Z + 0.03))
    sphere_a.add_update_rule("E_n", UpdateRules.e_sequence_rule(a=1.15, b=0.3))
    sphere_a.add_update_rule("F_n", lambda s, step: s.inputs.F_n + 0.5)

    sphere_b = TimeSphere(initial_inputs=initial_inputs)
    sphere_b.add_update_rule("A", UpdateRules.oscillate(amplitude=0.2, period=5, baseline=0.5))
    sphere_b.add_update_rule("B", UpdateRules.decay(rate=0.03, min_value=0.3, variable="B"))
    sphere_b.add_update_rule("C", lambda s, step: max(0.4, s.inputs.C - 0.01))
    sphere_b.add_update_rule("X", lambda s, step: max(0.2, s.inputs.X - 0.04))
    sphere_b.add_update_rule("Y", UpdateRules.oscillate(amplitude=0.25, period=4, baseline=0.4))
    sphere_b.add_update_rule("Z", UpdateRules.decay(rate=0.04, min_value=0.3, variable="Z"))
    sphere_b.add_update_rule("E_n", lambda s, step: max(1.0, s.inputs.E_n * 0.95))
    sphere_b.add_update_rule("F_n", lambda s, step: max(0.0, s.inputs.F_n - 0.1))

    result_a = sphere_a.simulate(steps=15)
    result_b = sphere_b.simulate(steps=15)

    assert result_a.summary["final_intelligence"] > result_b.summary["final_intelligence"]
    final_a_x = result_a.steps[-1].intelligence.components["X"]
    final_b_x = result_b.steps[-1].intelligence.components["X"]
    assert final_a_x > final_b_x
    print("✓ Divergent paths scenario behavior")


def test_ai_alignment_behavior():
    """Alignment phase should increase A and deployment should raise feedback."""
    initial_inputs = AxiomInputs(
        A=0.7,
        B=0.3,
        C=0.8,
        X=0.9,
        Y=0.2,
        Z=0.5,
        E_n=4.0,
        F_n=0.0,
    )
    sphere = TimeSphere(initial_inputs=initial_inputs)

    def phase_aware_update(step):
        if step <= 5:
            return "training"
        if step <= 10:
            return "alignment"
        return "deployment"

    def alignment_rule(state, step):
        phase = phase_aware_update(step)
        if phase == "training":
            return max(0.4, state.inputs.A - 0.02)
        if phase == "alignment":
            return min(0.95, state.inputs.A + 0.08)
        return max(0.7, state.inputs.A - 0.01)

    sphere.add_update_rule("A", alignment_rule)
    sphere.add_update_rule("B", lambda s, step: min(1.0, s.inputs.B + (0.12 if step <= 5 else 0.04)))
    sphere.add_update_rule("C", lambda s, step: min(1.0, s.inputs.C + 0.01))
    sphere.add_update_rule("X", lambda s, step: max(0.6, s.inputs.X - 0.03) if step > 10 else min(1.0, s.inputs.X))
    sphere.add_update_rule("Y", lambda s, step: min(1.0, s.inputs.Y + (0.04 if step <= 5 else 0.08 if step <= 10 else 0.05)))
    sphere.add_update_rule("Z", lambda s, step: min(1.0, s.inputs.Z + (0.09 if step <= 10 else 0.04)))
    sphere.add_update_rule("E_n", UpdateRules.e_sequence_rule(a=1.1, b=0.2))

    def feedback_rule(state, step):
        if step > 10:
            return state.inputs.F_n + 1.0
        if step > 5:
            return state.inputs.F_n + 0.3
        return state.inputs.F_n

    sphere.add_update_rule("F_n", feedback_rule)

    result = sphere.simulate(steps=15)
    a_step_6 = result.steps[6].intelligence.components["A"]
    a_step_10 = result.steps[10].intelligence.components["A"]
    assert a_step_10 >= a_step_6

    f_step_10 = result.steps[10].intelligence.components["F_n"]
    f_step_11 = result.steps[11].intelligence.components["F_n"]
    assert f_step_11 > f_step_10
    print("✓ AI alignment scenario behavior")


def test_resilience_recovery_behavior():
    """Shock should dip intelligence, recovery should improve it afterward."""
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
    sphere = TimeSphere(initial_inputs=initial_inputs)
    shock_step = 4

    def shock_then_recover(variable, *, drop_factor, recovery_rate, min_value=0.0, max_value=1.0):
        def rule(state, step):
            current = getattr(state.inputs, variable)
            if step == shock_step:
                return max(min_value, current * drop_factor)
            return min(max_value, current + recovery_rate)

        return rule

    sphere.add_update_rule(
        "A",
        shock_then_recover("A", drop_factor=0.7, recovery_rate=0.05),
    )
    sphere.add_update_rule(
        "B",
        shock_then_recover("B", drop_factor=0.65, recovery_rate=0.06),
    )
    sphere.add_update_rule(
        "C",
        shock_then_recover("C", drop_factor=0.85, recovery_rate=0.03),
    )
    sphere.add_update_rule(
        "X",
        shock_then_recover("X", drop_factor=0.8, recovery_rate=0.04),
    )
    sphere.add_update_rule(
        "Y",
        shock_then_recover("Y", drop_factor=0.6, recovery_rate=0.08),
    )
    sphere.add_update_rule(
        "Z",
        shock_then_recover("Z", drop_factor=0.6, recovery_rate=0.07),
    )

    def energy_rule(state, step):
        if step == shock_step:
            return max(1.0, state.inputs.E_n * 0.6)
        return state.inputs.E_n + 0.5

    sphere.add_update_rule("E_n", energy_rule)
    sphere.add_update_rule("F_n", lambda s, step: s.inputs.F_n + 0.4)

    result = sphere.simulate(steps=10)

    score_pre_shock = result.steps[3].intelligence.score
    score_shock = result.steps[4].intelligence.score
    score_final = result.steps[-1].intelligence.score
    assert score_shock < score_pre_shock
    assert score_final > score_shock
    print("✓ Resilience and recovery scenario behavior")


def test_innovation_cycles_behavior():
    """Innovation cycles should oscillate output while trending upward."""
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
    sphere = TimeSphere(initial_inputs=initial_inputs)
    sphere.add_update_rule("A", UpdateRules.linear_growth(rate=0.04, variable="A"))
    sphere.add_update_rule("B", UpdateRules.linear_growth(rate=0.05, variable="B"))
    sphere.add_update_rule("C", UpdateRules.linear_growth(rate=0.03, variable="C"))
    sphere.add_update_rule("X", UpdateRules.linear_growth(rate=0.04, variable="X"))
    sphere.add_update_rule("Y", UpdateRules.oscillate(amplitude=0.25, period=6, baseline=0.55))
    sphere.add_update_rule("Z", UpdateRules.oscillate(amplitude=0.2, period=6, baseline=0.6))
    sphere.add_update_rule("E_n", UpdateRules.e_sequence_rule(a=1.15, b=0.4))
    sphere.add_update_rule("F_n", UpdateRules.fibonacci_rule())

    result = sphere.simulate(steps=12)

    y_values = [ts.intelligence.components["Y"] for ts in result.steps]
    assert min(y_values) < 0.4
    assert max(y_values) >= 0.75
    assert result.summary["max_intelligence"] > result.summary["min_intelligence"]
    print("✓ Innovation cycles scenario behavior")


def run_all_tests():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("Running Example Scenario Tests")
    print("=" * 60 + "\n")

    tests = [
        test_basic_growth_scenario_behavior,
        test_corruption_decay_scenario_behavior,
        test_divergent_paths_behavior,
        test_ai_alignment_behavior,
        test_resilience_recovery_behavior,
        test_innovation_cycles_behavior,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} error: {e}")
            failed += 1

    print(f"\n{'=' * 60}")
    print(f"Results: {passed} passed, {failed} failed")
    print(f"{'=' * 60}\n")

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
