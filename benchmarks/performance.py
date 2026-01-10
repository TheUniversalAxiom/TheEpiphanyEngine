"""
Performance benchmarking utilities for the axiom engine.
"""

import time
import statistics
from typing import Dict, List, Callable, Any, Tuple
from axiom.core_equation import compute_intelligence, fibonacci_sequence
from engine.timesphere import TimeSphere, UpdateRules
from engine.state import AxiomInputs


def benchmark_computation(
    iterations: int = 10000,
    config: Dict[str, float] = None
) -> Dict[str, Any]:
    """
    Benchmark the core intelligence computation.

    Args:
        iterations: Number of iterations to run
        config: Parameter configuration (uses default if None)

    Returns:
        Dict with benchmark results including timing statistics
    """
    if config is None:
        config = {
            "A": 0.7, "B": 0.7, "C": 0.7,
            "X": 0.7, "Y": 0.7, "Z": 0.7,
            "E_n": 5.0, "F_n": 3.0
        }

    times = []

    # Warmup
    for _ in range(100):
        compute_intelligence(**config)

    # Benchmark
    for _ in range(iterations):
        start = time.perf_counter()
        compute_intelligence(**config, return_components=True)
        end = time.perf_counter()
        times.append((end - start) * 1000)  # Convert to milliseconds

    return {
        "operation": "core_computation",
        "iterations": iterations,
        "total_time_ms": sum(times),
        "mean_time_ms": statistics.mean(times),
        "median_time_ms": statistics.median(times),
        "stdev_time_ms": statistics.stdev(times) if len(times) > 1 else 0,
        "min_time_ms": min(times),
        "max_time_ms": max(times),
        "ops_per_second": 1000 / statistics.mean(times)
    }


def benchmark_simulation(
    steps: int = 100,
    iterations: int = 100
) -> Dict[str, Any]:
    """
    Benchmark TimeSphere simulation performance.

    Args:
        steps: Number of simulation steps
        iterations: Number of iterations to run

    Returns:
        Dict with benchmark results
    """
    initial_inputs = AxiomInputs(
        A=0.5, B=0.5, C=0.6,
        X=0.7, Y=0.6, Z=0.6,
        E_n=4.0, F_n=2.0
    )

    update_rules = {
        "A": UpdateRules.linear_growth(rate=0.02, max_value=0.9),
        "B": UpdateRules.linear_growth(rate=0.03, max_value=0.9),
        "Y": UpdateRules.linear_growth(rate=0.02, max_value=0.9),
        "E_n": UpdateRules.e_sequence_rule(a=1.05, b=0.2)
    }

    times = []

    # Warmup
    for _ in range(10):
        sphere = TimeSphere(initial_inputs, update_rules)
        sphere.simulate(steps=steps)

    # Benchmark
    for _ in range(iterations):
        sphere = TimeSphere(initial_inputs, update_rules)
        start = time.perf_counter()
        sphere.simulate(steps=steps)
        end = time.perf_counter()
        times.append((end - start) * 1000)

    return {
        "operation": "simulation",
        "steps": steps,
        "iterations": iterations,
        "total_time_ms": sum(times),
        "mean_time_ms": statistics.mean(times),
        "median_time_ms": statistics.median(times),
        "stdev_time_ms": statistics.stdev(times) if len(times) > 1 else 0,
        "min_time_ms": min(times),
        "max_time_ms": max(times),
        "steps_per_second": (steps * 1000) / statistics.mean(times)
    }


def benchmark_update_rules(
    steps: int = 1000,
    iterations: int = 100
) -> Dict[str, Dict[str, Any]]:
    """
    Benchmark different update rule types.

    Args:
        steps: Number of steps to simulate
        iterations: Number of iterations per rule

    Returns:
        Dict mapping rule names to benchmark results
    """
    initial_inputs = AxiomInputs(
        A=0.5, B=0.5, C=0.5,
        X=0.7, Y=0.7, Z=0.7,
        E_n=3.0, F_n=2.0
    )

    rules_to_test = {
        "constant": {"A": UpdateRules.constant(0.7)},
        "linear_growth": {"A": UpdateRules.linear_growth(rate=0.01, max_value=0.9)},
        "decay": {"A": UpdateRules.decay(rate=0.01, min_value=0.1)},
        "oscillate": {"A": UpdateRules.oscillate(amplitude=0.2, period=10, baseline=0.5)},
        "e_sequence": {"E_n": UpdateRules.e_sequence_rule(a=1.05, b=0.1)},
        "fibonacci": {"F_n": UpdateRules.fibonacci_rule(scale=0.1)}
    }

    results = {}

    for rule_name, rule_config in rules_to_test.items():
        times = []

        # Warmup
        for _ in range(10):
            sphere = TimeSphere(initial_inputs, rule_config)
            sphere.simulate(steps=steps)

        # Benchmark
        for _ in range(iterations):
            sphere = TimeSphere(initial_inputs, rule_config)
            start = time.perf_counter()
            sphere.simulate(steps=steps)
            end = time.perf_counter()
            times.append((end - start) * 1000)

        results[rule_name] = {
            "mean_time_ms": statistics.mean(times),
            "median_time_ms": statistics.median(times),
            "stdev_time_ms": statistics.stdev(times) if len(times) > 1 else 0,
            "min_time_ms": min(times),
            "max_time_ms": max(times)
        }

    return results


def benchmark_fibonacci(
    n: int = 100,
    iterations: int = 1000
) -> Dict[str, Any]:
    """
    Benchmark Fibonacci sequence generation.

    Args:
        n: Number of Fibonacci terms to generate
        iterations: Number of iterations

    Returns:
        Dict with benchmark results
    """
    times = []

    # Warmup
    for _ in range(100):
        list(fibonacci_sequence(n))

    # Benchmark
    for _ in range(iterations):
        start = time.perf_counter()
        list(fibonacci_sequence(n))
        end = time.perf_counter()
        times.append((end - start) * 1000)

    return {
        "operation": "fibonacci_sequence",
        "terms": n,
        "iterations": iterations,
        "mean_time_ms": statistics.mean(times),
        "median_time_ms": statistics.median(times),
        "stdev_time_ms": statistics.stdev(times) if len(times) > 1 else 0,
        "min_time_ms": min(times),
        "max_time_ms": max(times)
    }


def run_all_benchmarks(verbose: bool = True) -> Dict[str, Any]:
    """
    Run comprehensive benchmark suite.

    Args:
        verbose: Whether to print results as they complete

    Returns:
        Dict with all benchmark results
    """
    results = {}

    if verbose:
        print("=" * 70)
        print("EPIPHANY Engine Performance Benchmarks")
        print("=" * 70)
        print()

    # Core computation benchmark
    if verbose:
        print("Running: Core Intelligence Computation...")
    results["core_computation"] = benchmark_computation(iterations=10000)
    if verbose:
        print(f"  Mean: {results['core_computation']['mean_time_ms']:.4f} ms")
        print(f"  Ops/sec: {results['core_computation']['ops_per_second']:.0f}")
        print()

    # Simulation benchmarks
    simulation_configs = [
        (10, 1000),
        (100, 100),
        (1000, 10)
    ]

    results["simulation"] = {}
    for steps, iters in simulation_configs:
        if verbose:
            print(f"Running: Simulation ({steps} steps, {iters} iterations)...")
        key = f"{steps}_steps"
        results["simulation"][key] = benchmark_simulation(steps=steps, iterations=iters)
        if verbose:
            print(f"  Mean: {results['simulation'][key]['mean_time_ms']:.2f} ms")
            print(f"  Steps/sec: {results['simulation'][key]['steps_per_second']:.0f}")
            print()

    # Update rules benchmark
    if verbose:
        print("Running: Update Rules Performance...")
    results["update_rules"] = benchmark_update_rules(steps=1000, iterations=100)
    if verbose:
        for rule_name, rule_results in results["update_rules"].items():
            print(f"  {rule_name:15s}: {rule_results['mean_time_ms']:.2f} ms")
        print()

    # Fibonacci benchmark
    if verbose:
        print("Running: Fibonacci Sequence...")
    results["fibonacci"] = benchmark_fibonacci(n=100, iterations=1000)
    if verbose:
        print(f"  Mean: {results['fibonacci']['mean_time_ms']:.4f} ms")
        print()

    if verbose:
        print("=" * 70)
        print("Benchmark Suite Complete")
        print("=" * 70)

    return results


def compare_configurations(
    configs: Dict[str, Dict[str, float]],
    iterations: int = 1000
) -> Dict[str, Any]:
    """
    Compare performance across different parameter configurations.

    Args:
        configs: Dict mapping config names to parameter dicts
        iterations: Number of iterations per config

    Returns:
        Dict with comparison results
    """
    results = {}

    for name, config in configs.items():
        times = []

        for _ in range(iterations):
            start = time.perf_counter()
            compute_intelligence(**config, return_components=True)
            end = time.perf_counter()
            times.append((end - start) * 1000)

        results[name] = {
            "mean_time_ms": statistics.mean(times),
            "median_time_ms": statistics.median(times),
            "stdev_time_ms": statistics.stdev(times) if len(times) > 1 else 0
        }

    return results


if __name__ == "__main__":
    # Run benchmarks when executed directly
    run_all_benchmarks(verbose=True)
