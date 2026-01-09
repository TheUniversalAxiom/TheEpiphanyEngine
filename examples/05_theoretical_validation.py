"""
Example 5: Theoretical Validation

Validates our implementation against the theoretical calculation example
from the Universal Axiom Prism framework documentation.

Expected result: Intelligence_4 = 50.2155
"""
from epiphany_engine.axiom.core_equation import compute_intelligence, e_recurrence, fibonacci


def validate_theoretical_example():
    """
    Reproduce the exact calculation from the Universal Axiom Prism theory.

    From the documentation:
    For n = 4:
    - E_4 = 161 (using E_n = 3*E_{n-1} + 2)
    - F_4 = 3 (Fibonacci sequence)
    - X = 0.625
    - Y = 0.625
    - Z = 0.4
    - A = 0.8
    - B = 0.9
    - C = 0.7

    Expected: Intelligence_4 = 50.2155
    """
    print("\n" + "=" * 70)
    print("THEORETICAL VALIDATION - Universal Axiom Prism")
    print("=" * 70 + "\n")

    # Step 1: Calculate E_4 using the recurrence E_n = 3*E_{n-1} + 2
    print("Step 1: Calculate E_4 using E_n = 3*E_{n-1} + 2")
    print("  Starting with E_0 = 1 (initial energy):")

    E_0 = 1
    E_1 = e_recurrence(E_0, a=3.0, b=2.0)
    E_2 = e_recurrence(E_1, a=3.0, b=2.0)
    E_3 = e_recurrence(E_2, a=3.0, b=2.0)
    E_4 = e_recurrence(E_3, a=3.0, b=2.0)

    print(f"  E_0 = {E_0}")
    print(f"  E_1 = 3*{E_0} + 2 = {E_1}")
    print(f"  E_2 = 3*{E_1} + 2 = {E_2}")
    print(f"  E_3 = 3*{E_2} + 2 = {E_3}")
    print(f"  E_4 = 3*{E_3} + 2 = {E_4}")
    print()

    # Step 2: Get F_4 from Fibonacci
    print("Step 2: Get F_4 from Fibonacci sequence")
    print("  Fibonacci sequence: 0, 1, 1, 2, 3, 5, 8, ...")
    F_4 = fibonacci(4)
    print(f"  F_4 = {F_4}")
    print()

    # Step 3: Define other parameters
    print("Step 3: Define context and foundation parameters")
    X = 0.625
    Y = 0.625
    Z = 0.4
    A = 0.8
    B = 0.9
    C = 0.7
    print(f"  X (Objectivity) = {X}")
    print(f"  Y (Why Alignment) = {Y}")
    print(f"  Z (Time Progress) = {Z}")
    print(f"  A (Impulses) = {A}")
    print(f"  B (Elements) = {B}")
    print(f"  C (Pressure) = {C}")
    print()

    # Step 4: Manual calculation (as shown in theory)
    print("Step 4: Manual calculation following theoretical steps")
    step_1 = 1 + F_4
    print(f"  1. Calculate 1 + F_n: 1 + {F_4} = {step_1}")

    step_2 = E_4 * step_1
    print(f"  2. Multiply E_n by {step_1}: {E_4} * {step_1} = {step_2}")

    step_3 = step_2 * X
    print(f"  3. Multiply by X: {step_2} * {X} = {step_3}")

    step_4 = step_3 * Y
    print(f"  4. Multiply by Y: {step_3} * {Y} = {step_4}")

    step_5 = step_4 * Z
    print(f"  5. Multiply by Z: {step_4} * {Z} = {step_5}")

    step_6 = A * B * C
    print(f"  6. Calculate A * B * C: {A} * {B} * {C} = {step_6}")

    manual_result = step_5 * step_6
    print(f"  7. Multiply by ABC: {step_5} * {step_6} = {manual_result}")
    print()

    # Step 5: Use our compute_intelligence function
    print("Step 5: Validate using compute_intelligence() function")
    computed_result = compute_intelligence(
        A=A, B=B, C=C,
        X=X, Y=Y, Z=Z,
        E_n=E_4, F_n=F_4
    )
    print(f"  compute_intelligence() = {computed_result}")
    print()

    # Step 6: Compare with expected
    expected_in_doc = 50.2155
    correct_calculation = 50.715
    print("=" * 70)
    print("VALIDATION RESULTS")
    print("=" * 70)
    print(f"  Expected (from doc):       {expected_in_doc}")
    print(f"  Correct calculation:       {correct_calculation:.4f}")
    print(f"  Manual calculation:        {manual_result:.4f}")
    print(f"  Implementation result:     {computed_result:.4f}")
    print()

    # Check accuracy against correct calculation
    manual_error = abs(manual_result - correct_calculation)
    computed_error = abs(computed_result - correct_calculation)

    if manual_error < 0.01 and computed_error < 0.01:
        print(f"  ✅ VALIDATION SUCCESSFUL!")
        print(f"     Manual matches correct: {manual_error:.6f} error")
        print(f"     Implementation matches: {computed_error:.6f} error")
        print(f"\n  The implementation correctly reproduces the theoretical framework.")
        print(f"\n  Note: The theoretical document shows 50.2155, but the correct")
        print(f"        calculation of 100.625 × 0.504 = 50.715")
    else:
        print(f"  ⚠️  VALIDATION ISSUES DETECTED")
        print(f"     Manual error: {manual_error:.6f}")
        print(f"     Implementation error: {computed_error:.6f}")

    print()
    print("=" * 70)
    print()

    return computed_result


if __name__ == "__main__":
    validate_theoretical_example()
