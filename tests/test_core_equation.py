"""
Tests for axiom/core_equation.py
"""
import sys

from axiom.core_equation import (
    compute_intelligence,
    e_recurrence,
    e_sequence,
    fibonacci,
    fibonacci_sequence,
)


def test_compute_intelligence_basic():
    """Test basic intelligence computation."""
    result = compute_intelligence(
        A=1.0, B=1.0, C=1.0, X=1.0, Y=1.0, Z=1.0, E_n=1.0, F_n=0.0
    )
    expected = 1.0 * (1 + 0) * 1.0 * 1.0 * 1.0 * (1.0 * 1.0 * 1.0)
    assert abs(result - expected) < 0.0001, f"Expected {expected}, got {result}"
    print("✓ Basic intelligence computation")


def test_compute_intelligence_with_fibonacci():
    """Test with Fibonacci factor."""
    result = compute_intelligence(
        A=1.0, B=1.0, C=1.0, X=1.0, Y=1.0, Z=1.0, E_n=2.0, F_n=1.0
    )
    expected = 2.0 * (1 + 1.0) * 1.0 * (1.0)
    assert abs(result - expected) < 0.0001, f"Expected {expected}, got {result}"
    print("✓ Intelligence with Fibonacci factor")


def test_compute_intelligence_returns_components():
    """Test that components are returned when requested."""
    result, components = compute_intelligence(
        A=0.5, B=0.6, C=0.7, X=0.8, Y=0.9, Z=1.0, E_n=2.0, F_n=1.0,
        return_components=True
    )

    assert "ABC" in components
    assert "XYZ" in components
    assert "E_factor" in components
    assert abs(components["ABC"] - (0.5 * 0.6 * 0.7)) < 0.0001
    assert abs(components["XYZ"] - (0.8 * 0.9 * 1.0)) < 0.0001
    assert abs(components["E_factor"] - (2.0 * 2.0)) < 0.0001
    print("✓ Components returned correctly")


def test_e_recurrence():
    """Test E_n recurrence."""
    E_0 = 1.0
    E_1 = e_recurrence(E_0, a=3.0, b=2.0)
    expected = 3.0 * 1.0 + 2.0
    assert abs(E_1 - expected) < 0.0001, f"Expected {expected}, got {E_1}"
    print("✓ E_n recurrence")


def test_e_sequence():
    """Test E sequence generation."""
    seq = list(e_sequence(initial=1.0, steps=3, a=2.0, b=1.0))
    expected = [1.0, 3.0, 7.0, 15.0]  # E_0=1, E_1=2*1+1=3, E_2=2*3+1=7, E_3=2*7+1=15
    for i, (actual, exp) in enumerate(zip(seq, expected)):
        assert abs(actual - exp) < 0.0001, f"Step {i}: Expected {exp}, got {actual}"
    print("✓ E sequence generation")


def test_fibonacci():
    """Test Fibonacci calculation."""
    fib_values = [fibonacci(n) for n in range(10)]
    expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    assert fib_values == expected, f"Expected {expected}, got {fib_values}"
    print("✓ Fibonacci calculation")


def test_fibonacci_sequence():
    """Test Fibonacci sequence generation."""
    seq = list(fibonacci_sequence(steps=9))
    expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    assert seq == expected, f"Expected {expected}, got {seq}"
    print("✓ Fibonacci sequence generation")


def test_clamping():
    """Test value clamping."""
    result = compute_intelligence(
        A=1.5, B=1.2, C=-0.1, X=0.8, Y=0.9, Z=1.0, E_n=2.0, F_n=-2.0,
        clamp_to_unit=True
    )
    # Should clamp A, B, C to [0,1] and F_n to >= -1
    _, components = compute_intelligence(
        A=1.5, B=1.2, C=-0.1, X=0.8, Y=0.9, Z=1.0, E_n=2.0, F_n=-2.0,
        clamp_to_unit=True,
        return_components=True
    )
    assert components["A"] == 1.0, f"A should be clamped to 1.0, got {components['A']}"
    assert components["B"] == 1.0, f"B should be clamped to 1.0, got {components['B']}"
    assert components["C"] == 0.0, f"C should be clamped to 0.0, got {components['C']}"
    assert components["F_n"] == -1.0, f"F_n should be clamped to -1.0, got {components['F_n']}"
    print("✓ Value clamping")


def run_all_tests():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("Running Core Equation Tests")
    print("=" * 60 + "\n")

    tests = [
        test_compute_intelligence_basic,
        test_compute_intelligence_with_fibonacci,
        test_compute_intelligence_returns_components,
        test_e_recurrence,
        test_e_sequence,
        test_fibonacci,
        test_fibonacci_sequence,
        test_clamping,
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
