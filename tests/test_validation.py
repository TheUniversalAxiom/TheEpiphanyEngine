"""
Comprehensive validation and edge case tests for The EPIPHANY Engine.
"""

import pytest

from axiom.core_equation import compute_intelligence, e_recurrence, fibonacci, fibonacci_sequence
from axiom.subjectivity_scale import determine_subjectivity
from engine.state import AxiomInputs
from engine.timesphere import TimeSphere, UpdateRules


class TestInputValidation:
    """Test input validation and bounds checking."""

    def test_valid_baseline_computation(self):
        """Test that valid baseline inputs work correctly."""
        result, components = compute_intelligence(
            A=0.7, B=0.7, C=0.7,
            X=0.7, Y=0.7, Z=0.7,
            E_n=5.0, F_n=3.0,
            return_components=True
        )
        assert result > 0
        assert components['ABC'] > 0
        assert components['XYZ'] > 0

    def test_boundary_values(self):
        """Test computation with boundary values (0 and 1)."""
        # All zeros (except E_n which must be positive)
        result1 = compute_intelligence(
            A=0.0, B=0.0, C=0.0,
            X=0.0, Y=0.0, Z=0.0,
            E_n=1.0, F_n=0.0
        )
        assert result1 == 0.0  # Product should be zero

        # All ones
        result2 = compute_intelligence(
            A=1.0, B=1.0, C=1.0,
            X=1.0, Y=1.0, Z=1.0,
            E_n=1.0, F_n=1.0
        )
        assert result2 > 0

    def test_negative_E_n_clamping(self):
        """Test that negative E_n is clamped to 0."""
        result = compute_intelligence(
            A=0.7, B=0.7, C=0.7,
            X=0.7, Y=0.7, Z=0.7,
            E_n=-5.0,  # Should be clamped to 0
            F_n=3.0,
            clamp_values=True
        )
        # With E_n = 0, result should be 0
        assert result == 0.0

    def test_negative_F_n_handling(self):
        """Test that F_n below -1 is handled."""
        result = compute_intelligence(
            A=0.7, B=0.7, C=0.7,
            X=0.7, Y=0.7, Z=0.7,
            E_n=5.0,
            F_n=-2.0,  # Below minimum
            clamp_values=True
        )
        # Should clamp to -1 minimum
        assert result >= 0.0

    def test_out_of_range_abc_clamping(self):
        """Test clamping of A, B, C values outside [0, 1]."""
        result, components = compute_intelligence(
            A=1.5,  # Should clamp to 1.0
            B=-0.5,  # Should clamp to 0.0
            C=0.7,
            X=0.7, Y=0.7, Z=0.7,
            E_n=5.0, F_n=3.0,
            clamp_values=True,
            return_components=True
        )
        # Check that clamping occurred
        assert 0.0 <= components['A'] <= 1.0
        assert 0.0 <= components['B'] <= 1.0

    def test_strict_bounds_validation(self):
        """Test that strict bounds checking raises errors."""
        with pytest.raises(ValueError):
            compute_intelligence(
                A=1.5,  # Out of bounds
                B=0.7, C=0.7,
                X=0.7, Y=0.7, Z=0.7,
                E_n=5.0, F_n=3.0,
                clamp_values=False
            )

    def test_nan_handling(self):
        """Test handling of NaN values."""
        import math
        result = compute_intelligence(
            A=0.7, B=0.7, C=0.7,
            X=math.nan,  # Invalid input
            Y=0.7, Z=0.7,
            E_n=5.0, F_n=3.0,
            clamp_values=True
        )
        # With NaN, result should be NaN
        assert math.isnan(result)

    def test_infinity_handling(self):
        """Test handling of infinity values."""
        import math
        result = compute_intelligence(
            A=0.7, B=0.7, C=0.7,
            X=0.7, Y=0.7, Z=0.7,
            E_n=math.inf,
            F_n=3.0,
            clamp_values=True
        )
        # Result should be infinite
        assert math.isinf(result)


class TestEdgeCases:
    """Test edge cases and corner scenarios."""

    def test_zero_growth_simulation(self):
        """Test simulation with no growth (constant values)."""
        initial = AxiomInputs(
            A=0.5, B=0.5, C=0.5,
            X=0.7, Y=0.7, Z=0.7,
            E_n=3.0, F_n=2.0
        )
        rules = {
            "A": UpdateRules.constant(0.5),
            "B": UpdateRules.constant(0.5),
            "C": UpdateRules.constant(0.5)
        }

        sphere = TimeSphere(initial, rules)
        result = sphere.simulate(steps=10)

        # All intelligence values should be identical (or very close)
        intelligences = [h.intelligence for h in result.history]
        assert all(abs(i - intelligences[0]) < 0.001 for i in intelligences)

    def test_single_step_simulation(self):
        """Test simulation with just one step."""
        initial = AxiomInputs(
            A=0.5, B=0.5, C=0.5,
            X=0.7, Y=0.7, Z=0.7,
            E_n=3.0, F_n=2.0
        )
        rules = {"A": UpdateRules.linear_growth(rate=0.1, max_value=1.0)}

        sphere = TimeSphere(initial, rules)
        result = sphere.simulate(steps=1)

        assert len(result.history) == 2  # Initial + 1 step

    def test_zero_step_simulation(self):
        """Test simulation with zero steps."""
        initial = AxiomInputs(
            A=0.5, B=0.5, C=0.5,
            X=0.7, Y=0.7, Z=0.7,
            E_n=3.0, F_n=2.0
        )
        rules = {}

        sphere = TimeSphere(initial, rules)
        result = sphere.simulate(steps=0)

        assert len(result.history) == 1  # Just initial state

    def test_very_large_step_count(self):
        """Test simulation with very large step count."""
        initial = AxiomInputs(
            A=0.5, B=0.5, C=0.5,
            X=0.7, Y=0.7, Z=0.7,
            E_n=3.0, F_n=2.0
        )
        rules = {"A": UpdateRules.linear_growth(rate=0.001, max_value=1.0)}

        sphere = TimeSphere(initial, rules)
        result = sphere.simulate(steps=1000)

        assert len(result.history) == 1001
        assert result.history[-1].inputs.A <= 1.0  # Should respect max_value

    def test_decay_to_minimum(self):
        """Test decay update rule reaching minimum."""
        initial = AxiomInputs(
            A=0.9, B=0.5, C=0.5,
            X=0.7, Y=0.7, Z=0.7,
            E_n=3.0, F_n=2.0
        )
        rules = {"A": UpdateRules.decay(rate=0.1, min_value=0.1)}

        sphere = TimeSphere(initial, rules)
        result = sphere.simulate(steps=50)

        # A should reach minimum and stay there
        final_a = result.history[-1].inputs.A
        assert abs(final_a - 0.1) < 0.01

    def test_growth_to_maximum(self):
        """Test linear growth reaching maximum."""
        initial = AxiomInputs(
            A=0.1, B=0.5, C=0.5,
            X=0.7, Y=0.7, Z=0.7,
            E_n=3.0, F_n=2.0
        )
        rules = {"A": UpdateRules.linear_growth(rate=0.1, max_value=0.9)}

        sphere = TimeSphere(initial, rules)
        result = sphere.simulate(steps=20)

        # A should reach maximum and stay there
        final_a = result.history[-1].inputs.A
        assert abs(final_a - 0.9) < 0.01


class TestFibonacciEdgeCases:
    """Test Fibonacci sequence edge cases."""

    def test_fibonacci_zero(self):
        """Test Fibonacci with n=0."""
        result = fibonacci(0)
        assert result == 0

    def test_fibonacci_one(self):
        """Test Fibonacci with n=1."""
        result = fibonacci(1)
        assert result == 1

    def test_fibonacci_negative(self):
        """Test Fibonacci with negative input."""
        with pytest.raises(ValueError):
            fibonacci(-1)

    def test_fibonacci_sequence_empty(self):
        """Test Fibonacci sequence with count=0."""
        result = list(fibonacci_sequence(0))
        assert result == []

    def test_fibonacci_sequence_one(self):
        """Test Fibonacci sequence with count=1."""
        result = list(fibonacci_sequence(1))
        assert result == [0]

    def test_fibonacci_sequence_large(self):
        """Test Fibonacci sequence with large count."""
        result = list(fibonacci_sequence(50))
        assert len(result) == 50
        # Check that sequence grows
        assert result[-1] > result[0]


class TestSubjectivityScale:
    """Test subjectivity scale edge cases."""

    def test_all_zero_signals(self):
        """Test subjectivity with all zero signals."""
        level, label = determine_subjectivity(
            noise=0.0,
            emotional_volatility=0.0,
            bias_indicator=0.0
        )
        assert level >= 0.0
        assert label in [
            'apex-objective',
            'objective',
            'base-static',
            'mid-dynamic',
            'high-subjective',
            'apex-dynamic',
            'apex-subjective',
        ]

    def test_all_max_signals(self):
        """Test subjectivity with all maximum signals."""
        level, label = determine_subjectivity(
            noise=1.0,
            emotional_volatility=1.0,
            bias_indicator=1.0
        )
        assert level > 0.5
        assert label in ['high-subjective', 'apex-dynamic', 'apex-subjective']

    def test_nan_signal_handling(self):
        """Test that NaN signals are handled gracefully."""
        import math
        level, label = determine_subjectivity(
            noise=math.nan,
            emotional_volatility=0.5,
            bias_indicator=0.5
        )
        # Should handle NaN and return a valid result
        assert isinstance(level, float)
        assert isinstance(label, str)


class TestERecurrence:
    """Test E_n recurrence edge cases."""

    def test_e_recurrence_zero_initial(self):
        """Test E sequence starting from zero."""
        result = e_recurrence(E_prev=0.0, a=1.1, b=0.5)
        assert result == 0.5  # 1.1 * 0.0 + 0.5

    def test_e_recurrence_negative_initial(self):
        """Test E sequence with negative initial value."""
        result = e_recurrence(E_prev=-5.0, a=1.1, b=0.5)
        # Result should be: 1.1 * (-5.0) + 0.5 = -5.5 + 0.5 = -5.0
        assert abs(result - (-5.0)) < 0.01

    def test_e_recurrence_large_values(self):
        """Test E sequence with very large values."""
        result = e_recurrence(E_prev=1000.0, a=1.5, b=100.0)
        assert result > 1000.0  # Should grow


class TestTimeSphereEdgeCases:
    """Test TimeSphere-specific edge cases."""

    def test_empty_update_rules(self):
        """Test simulation with no update rules (all constant)."""
        initial = AxiomInputs(
            A=0.5, B=0.5, C=0.5,
            X=0.7, Y=0.7, Z=0.7,
            E_n=3.0, F_n=2.0
        )
        rules = {}  # No rules

        sphere = TimeSphere(initial, rules)
        result = sphere.simulate(steps=10)

        # All values should remain constant
        for step in result.history:
            assert step.inputs.A == 0.5
            assert step.inputs.B == 0.5

    def test_multiple_update_rules_same_param(self):
        """Test that later rule overwrites earlier one."""
        initial = AxiomInputs(
            A=0.5, B=0.5, C=0.5,
            X=0.7, Y=0.7, Z=0.7,
            E_n=3.0, F_n=2.0
        )
        # This shouldn't be done in practice, but test behavior
        rules = {
            "A": UpdateRules.constant(0.9)  # Last rule wins
        }

        sphere = TimeSphere(initial, rules)
        result = sphere.simulate(steps=5)

        assert result.history[-1].inputs.A == 0.9

    def test_event_handler_execution(self):
        """Test that event handlers are called."""
        initial = AxiomInputs(
            A=0.3, B=0.5, C=0.5,
            X=0.7, Y=0.7, Z=0.7,
            E_n=3.0, F_n=2.0
        )
        rules = {"A": UpdateRules.linear_growth(rate=0.1, max_value=1.0)}

        triggered = []

        def milestone_handler(step):
            triggered.append(step.step)

        sphere = TimeSphere(initial, rules)
        sphere.add_event_handler(
            lambda s: s.inputs.A > 0.5,
            milestone_handler,
            event_type="test_milestone"
        )

        result = sphere.simulate(steps=10)

        # Handler should have been triggered
        assert len(triggered) > 0


def run_validation_tests():
    """Run all validation tests and return results."""
    pytest.main([__file__, "-v"])


if __name__ == "__main__":
    run_validation_tests()
