"""
Tests for axiom component modules.
"""

from axiom.components import (
    Elements,
    ExponentialGrowth,
    FibonacciSequence,
    Impulses,
    Pressure,
    SubjectivityScale,
    TimeSphere,
    WhyAxis,
)


def test_impulses_clamps_to_unit_range():
    impulses = Impulses(value=1.5)
    assert impulses.normalized() == 1.0


def test_elements_clamps_to_unit_range():
    elements = Elements(value=-0.2)
    assert elements.normalized() == 0.0


def test_pressure_clamps_to_unit_range():
    pressure = Pressure(value=0.75)
    assert pressure.normalized() == 0.75


def test_subjectivity_scale_clamps_to_unit_range():
    subjectivity_scale = SubjectivityScale(value=1.2)
    assert subjectivity_scale.normalized() == 1.0


def test_why_axis_clamps_to_unit_range():
    why_axis = WhyAxis(value=-1.0)
    assert why_axis.normalized() == 0.0


def test_timesphere_clamps_to_lower_bound():
    timesphere = TimeSphere(value=-0.5)
    assert timesphere.normalized() == 0.0


def test_exponential_growth_clamps_to_lower_bound():
    exponential_growth = ExponentialGrowth(value=-2.0)
    assert exponential_growth.normalized() == 0.0


def test_fibonacci_sequence_clamps_to_lower_bound():
    fibonacci_sequence = FibonacciSequence(value=-5.0)
    assert fibonacci_sequence.normalized() == -1.0
