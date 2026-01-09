"""
Tests for engine/timesphere.py
"""
from engine.timesphere import TimeSphere, UpdateRules
from engine.state import AxiomInputs


def test_timesphere_initialization():
    """Test TimeSphere initialization."""
    inputs = AxiomInputs(A=0.5, B=0.5, C=0.5, X=0.5, Y=0.5, Z=0.5, E_n=1.0, F_n=0.0)
    sphere = TimeSphere(initial_inputs=inputs)

    assert sphere.initial_state.inputs.A == 0.5
    assert sphere.initial_state.step == 0
    assert len(sphere.update_rules) == 0
    print("✓ TimeSphere initialization")


def test_add_update_rule():
    """Test adding update rules."""
    inputs = AxiomInputs(A=0.5, B=0.5, C=0.5, X=0.5, Y=0.5, Z=0.5, E_n=1.0, F_n=0.0)
    sphere = TimeSphere(initial_inputs=inputs)

    sphere.add_update_rule("A", lambda s, step: min(1.0, s.inputs.A + 0.1))
    assert "A" in sphere.update_rules
    print("✓ Adding update rules")


def test_constant_simulation():
    """Test simulation with constant values."""
    inputs = AxiomInputs(A=0.5, B=0.5, C=0.5, X=0.5, Y=0.5, Z=0.5, E_n=1.0, F_n=0.0)
    sphere = TimeSphere(initial_inputs=inputs)

    # No update rules = all values stay constant
    result = sphere.simulate(steps=5)

    assert len(result.steps) == 6  # Initial + 5 steps
    assert result.summary["total_steps"] == 5

    # All scores should be identical
    scores = [ts.intelligence.score for ts in result.steps]
    for score in scores:
        assert abs(score - scores[0]) < 0.0001, "Constant values should have constant intelligence"

    print("✓ Constant value simulation")


def test_growth_simulation():
    """Test simulation with growth."""
    inputs = AxiomInputs(A=0.5, B=0.5, C=0.5, X=0.5, Y=0.5, Z=0.5, E_n=1.0, F_n=0.0)
    sphere = TimeSphere(initial_inputs=inputs)

    # Add growth rule for A
    sphere.add_update_rule("A", lambda s, step: min(1.0, s.inputs.A + 0.1))

    result = sphere.simulate(steps=5)

    # A should grow each step
    a_values = [ts.state.inputs.A for ts in result.steps]
    for i in range(1, len(a_values)):
        assert a_values[i] >= a_values[i - 1], "A should grow or stay constant"

    # Intelligence should grow (since A is part of ABC)
    assert result.summary["final_intelligence"] > result.summary["initial_intelligence"]
    assert result.summary["growth_rate"] > 0

    print("✓ Growth simulation")


def test_decay_simulation():
    """Test simulation with decay."""
    inputs = AxiomInputs(A=0.9, B=0.9, C=0.9, X=0.9, Y=0.9, Z=0.9, E_n=5.0, F_n=3.0)
    sphere = TimeSphere(initial_inputs=inputs)

    # Add decay rules
    sphere.add_update_rule("A", UpdateRules.decay(rate=0.1, min_val=0.1, variable="A"))
    sphere.add_update_rule("B", UpdateRules.decay(rate=0.1, min_val=0.1, variable="B"))

    result = sphere.simulate(steps=5)

    # Intelligence should decline
    assert result.summary["final_intelligence"] < result.summary["initial_intelligence"]
    assert result.summary["growth_rate"] < 0

    print("✓ Decay simulation")


def test_event_detection():
    """Test event detection."""
    inputs = AxiomInputs(A=0.5, B=0.5, C=0.5, X=0.5, Y=0.5, Z=0.5, E_n=1.0, F_n=0.0)
    sphere = TimeSphere(initial_inputs=inputs)

    # Add event handler
    def detect_event(state, step):
        if step == 3:
            return "Test event at step 3"
        return None

    sphere.add_event_handler(detect_event)

    result = sphere.simulate(steps=5)

    # Check that event was detected
    step_3_events = result.steps[3].events
    assert "Test event at step 3" in step_3_events, f"Event not found in {step_3_events}"

    print("✓ Event detection")


def test_update_rules_collection():
    """Test pre-built update rules."""
    # Test constant rule
    rule = UpdateRules.constant(0.7)
    inputs = AxiomInputs(A=0.5, B=0.5, C=0.5, X=0.5, Y=0.5, Z=0.5, E_n=1.0, F_n=0.0)
    state_dummy = type('obj', (object,), {'inputs': inputs})()
    assert rule(state_dummy, 0) == 0.7

    # Test e_sequence_rule
    e_rule = UpdateRules.e_sequence_rule(a=2.0, b=1.0)
    # Should compute E_n = 2 * E_{n-1} + 1
    # With E_0 = 1.0, should get E_1 = 3.0
    result = e_rule(state_dummy, 1)
    assert abs(result - 3.0) < 0.0001, f"Expected 3.0, got {result}"

    # Test fibonacci_rule
    fib_rule = UpdateRules.fibonacci_rule()
    assert fib_rule(state_dummy, 0) == 0.0
    assert fib_rule(state_dummy, 1) == 1.0
    assert fib_rule(state_dummy, 5) == 5.0

    # Test variable-aware decay and growth
    decay_rule = UpdateRules.decay(rate=0.1, min_val=0.0, variable="B")
    growth_rule = UpdateRules.linear_growth(rate=0.2, max_val=1.0, variable="C")
    assert abs(decay_rule(state_dummy, 0) - (inputs.B * 0.9)) < 0.0001
    assert abs(growth_rule(state_dummy, 0) - (inputs.C + 0.2)) < 0.0001

    print("✓ Pre-built update rules")


def test_trend_analysis():
    """Test trend analysis."""
    inputs = AxiomInputs(A=0.3, B=0.3, C=0.3, X=0.3, Y=0.3, Z=0.3, E_n=1.0, F_n=0.0)
    sphere = TimeSphere(initial_inputs=inputs)

    # Add strong growth
    sphere.add_update_rule("A", lambda s, step: min(1.0, s.inputs.A + 0.1))
    sphere.add_update_rule("B", lambda s, step: min(1.0, s.inputs.B + 0.1))
    sphere.add_update_rule("E_n", UpdateRules.e_sequence_rule(a=1.5, b=1.0))

    result = sphere.simulate(steps=10)
    trends = sphere.analyze_trends()

    assert trends["trend"] == "accelerating_growth"
    assert trends["total_events"] >= 0

    print("✓ Trend analysis")


def run_all_tests():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("Running TimeSphere Tests")
    print("=" * 60 + "\n")

    tests = [
        test_timesphere_initialization,
        test_add_update_rule,
        test_constant_simulation,
        test_growth_simulation,
        test_decay_simulation,
        test_event_detection,
        test_update_rules_collection,
        test_trend_analysis,
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
