"""
Tests for Critical Bug Fixes

Validates the fixes for issues identified in BUGFIXES.md:
1. X semantic mismatch (objectivity vs subjectivity)
2. UpdateRules hard-coded to variable A
3. simulate(record_history=False) produces wrong summary
4. x_from_observations missing key validation
"""
from epiphany_engine.engine.timesphere import TimeSphere, UpdateRules
from epiphany_engine.engine.state import AxiomInputs
from epiphany_engine.axiom.subjectivity_scale import x_from_observations


def test_x_semantic_correctness():
    """
    Test Issue #1: X semantic mismatch fixed.

    X should represent OBJECTIVITY (inverse of subjectivity).
    - High noise/emotion/bias → LOW X (low objectivity)
    - Low noise/emotion/bias → HIGH X (high objectivity)
    """
    # Low noise/emotion/bias = high objectivity
    x_objective = x_from_observations(noise=0.1, emotional_volatility=0.1, bias_indicator=0.1)

    # High noise/emotion/bias = low objectivity
    x_subjective = x_from_observations(noise=0.9, emotional_volatility=0.9, bias_indicator=0.9)

    # Verify objectivity is higher when noise is lower
    assert x_objective > x_subjective, (
        f"Expected high objectivity ({x_objective:.3f}) > low objectivity ({x_subjective:.3f})"
    )

    # Verify high objectivity is close to 1.0
    assert x_objective > 0.7, f"Expected objectivity > 0.7, got {x_objective:.3f}"

    # Verify low objectivity is close to 0.0
    assert x_subjective < 0.3, f"Expected objectivity < 0.3, got {x_subjective:.3f}"

    print("✓ X semantic correctness (objectivity scale)")


def test_updaterules_variable_parameter():
    """
    Test Issue #2: UpdateRules fixed to accept variable parameter.

    UpdateRules.decay() and linear_growth() should update the specified
    variable, not always use A.
    """
    # Create system with different initial values
    inputs = AxiomInputs(
        A=0.9,  # High A
        B=0.5,  # Medium B
        C=0.3,  # Low C
        X=0.8, Y=0.7, Z=0.6,
        E_n=3.0, F_n=2.0
    )

    sphere = TimeSphere(initial_inputs=inputs)

    # Apply decay to B specifically
    sphere.add_update_rule("B", UpdateRules.decay("B", rate=0.2, min_val=0.1))

    result = sphere.simulate(steps=3, record_history=True)

    # Verify B decreased (decayed)
    initial_b = result.steps[0].state.inputs.B
    final_b = result.steps[-1].state.inputs.B

    assert final_b < initial_b, (
        f"Expected B to decay: initial={initial_b:.3f}, final={final_b:.3f}"
    )

    # Verify A remained constant (no rule applied)
    initial_a = result.steps[0].state.inputs.A
    final_a = result.steps[-1].state.inputs.A

    assert abs(final_a - initial_a) < 0.001, (
        f"Expected A to remain constant: initial={initial_a:.3f}, final={final_a:.3f}"
    )

    print("✓ UpdateRules variable parameter correctness")


def test_simulate_without_history():
    """
    Test Issue #3: simulate(record_history=False) summary fixed.

    When record_history=False, summary statistics should still reflect
    the actual final state, not just the initial state.
    """
    inputs = AxiomInputs(
        A=0.5, B=0.5, C=0.5,
        X=0.5, Y=0.5, Z=0.5,
        E_n=2.0, F_n=1.0
    )

    sphere = TimeSphere(initial_inputs=inputs)

    # Add growth rule for A
    sphere.add_update_rule("A", lambda s, step: min(1.0, s.inputs.A + 0.1))
    sphere.add_update_rule("B", lambda s, step: min(1.0, s.inputs.B + 0.1))

    # Simulate WITHOUT recording history
    result = sphere.simulate(steps=5, record_history=False)

    # Verify summary shows growth
    initial = result.summary["initial_intelligence"]
    final = result.summary["final_intelligence"]

    assert final > initial, (
        f"Expected final ({final:.4f}) > initial ({initial:.4f}) even without history"
    )

    # Verify growth rate is positive
    growth_rate = result.summary["growth_rate"]
    assert growth_rate > 0, f"Expected positive growth rate, got {growth_rate:.1%}"

    # Verify history contains at least initial and final
    assert len(result.steps) >= 2, (
        f"Expected at least initial and final states, got {len(result.steps)}"
    )

    print("✓ simulate(record_history=False) summary correctness")


def test_x_from_observations_partial_weights():
    """
    Test Issue #4: x_from_observations handles partial weight dicts.

    Should not crash when weights dict is missing some keys.
    """
    # Provide only partial weights
    x1 = x_from_observations(
        noise=0.5,
        emotional_volatility=0.5,
        bias_indicator=0.5,
        weights={"noise": 0.5}  # Missing emotion and bias keys
    )

    # Should use defaults for missing keys
    assert 0.0 <= x1 <= 1.0, f"Expected X in [0, 1], got {x1}"

    # Empty weights dict should work
    x2 = x_from_observations(
        noise=0.5,
        emotional_volatility=0.5,
        bias_indicator=0.5,
        weights={}
    )

    assert 0.0 <= x2 <= 1.0, f"Expected X in [0, 1], got {x2}"

    # No weights parameter should work (use defaults)
    x3 = x_from_observations(
        noise=0.5,
        emotional_volatility=0.5,
        bias_indicator=0.5
    )

    assert 0.0 <= x3 <= 1.0, f"Expected X in [0, 1], got {x3}"

    print("✓ x_from_observations partial weights handling")


def test_updaterules_linear_growth():
    """
    Additional test: Verify linear_growth also uses variable parameter correctly.
    """
    inputs = AxiomInputs(
        A=0.3, B=0.3, C=0.3,
        X=0.5, Y=0.5, Z=0.5,
        E_n=2.0, F_n=1.0
    )

    sphere = TimeSphere(initial_inputs=inputs)

    # Apply linear growth to C specifically
    sphere.add_update_rule("C", UpdateRules.linear_growth("C", rate=0.1, max_val=1.0))

    result = sphere.simulate(steps=3, record_history=True)

    # Verify C increased
    initial_c = result.steps[0].state.inputs.C
    final_c = result.steps[-1].state.inputs.C

    assert final_c > initial_c, (
        f"Expected C to grow: initial={initial_c:.3f}, final={final_c:.3f}"
    )

    # Verify A remained constant
    initial_a = result.steps[0].state.inputs.A
    final_a = result.steps[-1].state.inputs.A

    assert abs(final_a - initial_a) < 0.001, (
        f"Expected A to remain constant: initial={initial_a:.3f}, final={final_a:.3f}"
    )

    print("✓ UpdateRules.linear_growth variable parameter correctness")


def run_all_tests():
    """Run all bug fix validation tests."""
    print("\n" + "=" * 60)
    print("Running Bug Fix Validation Tests")
    print("=" * 60 + "\n")

    tests = [
        test_x_semantic_correctness,
        test_updaterules_variable_parameter,
        test_simulate_without_history,
        test_x_from_observations_partial_weights,
        test_updaterules_linear_growth,
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

    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60 + "\n")

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    if success:
        print("🎉 ALL BUG FIX TESTS PASSED!")
    else:
        print("❌ Some tests failed")
