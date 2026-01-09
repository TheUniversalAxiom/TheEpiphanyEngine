"""
Core Axiom: Intelligence computation and simple recurrences.

Implements:
- E_n recurrence (linear recurrence e.g., E_n = a * E_{n-1} + b)
- F_n recurrence / Fibonacci helper
- compute_intelligence(A, B, C, X, Y, Z, E_n, F_n)
- optional symbolic representation using sympy (if available)
"""
from typing import Union, Tuple, Dict, Optional, Iterable

Number = Union[int, float]


def e_recurrence(E_prev: Number, a: Number = 3.0, b: Number = 2.0) -> float:
    """
    Simple linear recurrence for E_n.

    Default: E_n = 3 * E_{n-1} + 2

    Returns the next E_n.
    """
    return float(a * E_prev + b)


def e_sequence(initial: Number, steps: int, a: Number = 3.0, b: Number = 2.0) -> Iterable[float]:
    """
    Generator for E sequence starting from `initial`. Yields E_0, E_1, ..., E_{steps}.
    """
    val = float(initial)
    yield val
    for _ in range(steps):
        val = e_recurrence(val, a=a, b=b)
        yield val


def fibonacci(n: int) -> int:
    """
    Return the n-th Fibonacci number (F_0 = 0, F_1 = 1).
    Uses an iterative approach for stability/speed.
    """
    if n < 0:
        raise ValueError("n must be >= 0")
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def fibonacci_sequence(steps: int) -> Iterable[int]:
    """
    Yield Fibonacci numbers starting at F_0 for `steps+1` values.
    """
    a, b = 0, 1
    for _ in range(steps + 1):
        yield a
        a, b = b, a + b


def compute_intelligence(
    A: Number,
    B: Number,
    C: Number,
    X: Number,
    Y: Number,
    Z: Number,
    E_n: Number,
    F_n: Number,
    *,
    validate: bool = True,
    clamp_to_unit: bool = True,
    return_components: bool = False,
) -> Union[float, Tuple[float, Dict[str, float]]]:
    """
    Compute the EPIPHANY core axiom:

        Intelligence_n = E_n * (1 + F_n) * X * Y * Z * (A * B * C)

    Parameters
    ----------
    A, B, C, X, Y, Z, E_n, F_n : numbers
        Inputs to the formula.
    validate : whether to check numeric types and some simple bounds.
    clamp_to_unit : if True, clamp A/B/C/X/Y to [0,1] and Z/E_n >= 0, F_n >= -1.
    return_components : if True return (score, components_dict).

    Returns
    -------
    float or (float, dict)
    """
    inputs = dict(A=A, B=B, C=C, X=X, Y=Y, Z=Z, E_n=E_n, F_n=F_n)

    if validate:
        for k, v in inputs.items():
            if not isinstance(v, (int, float)):
                raise TypeError(f"{k} must be numeric, got {type(v).__name__}")

    if clamp_to_unit:
        # clamp A/B/C/X/Y to [0,1]; Z,E_n >= 0; F_n >= -1
        inputs["A"] = max(0.0, min(1.0, float(inputs["A"])))
        inputs["B"] = max(0.0, min(1.0, float(inputs["B"])))
        inputs["C"] = max(0.0, min(1.0, float(inputs["C"])))
        inputs["X"] = max(0.0, min(1.0, float(inputs["X"])))
        inputs["Y"] = max(0.0, min(1.0, float(inputs["Y"])))
        inputs["Z"] = max(0.0, float(inputs["Z"]))
        inputs["E_n"] = max(0.0, float(inputs["E_n"]))
        # F_n may be negative but not less than -1 (so that (1+F_n) >= 0)
        inputs["F_n"] = max(-1.0, float(inputs["F_n"]))
    else:
        for k in inputs:
            inputs[k] = float(inputs[k])

    A = inputs["A"]
    B = inputs["B"]
    C = inputs["C"]
    X = inputs["X"]
    Y = inputs["Y"]
    Z = inputs["Z"]
    E_n = inputs["E_n"]
    F_n = inputs["F_n"]

    ABC = A * B * C
    XYZ = X * Y * Z
    E_factor = E_n * (1.0 + F_n)

    score = E_factor * XYZ * ABC

    if return_components:
        return score, {
            "A": A,
            "B": B,
            "C": C,
            "ABC": ABC,
            "X": X,
            "Y": Y,
            "Z": Z,
            "XYZ": XYZ,
            "E_n": E_n,
            "F_n": F_n,
            "E_factor": E_factor,
        }

    return float(score)


# Optional: symbolic representation (if sympy is present)
try:
    import sympy as sp  # type: ignore

    def symbolic_axiom():
        """
        Return a sympy expression and symbols for the core axiom:

            Intelligence_n = E_n * (1 + F_n) * X * Y * Z * (A * B * C)
        """
        A, B, C, X, Y, Z, E_n, F_n = sp.symbols("A B C X Y Z E_n F_n")
        expr = E_n * (1 + F_n) * X * Y * Z * (A * B * C)
        return expr, (A, B, C, X, Y, Z, E_n, F_n)
except Exception:
    # sympy not installed; symbolic functions not available
    pass
