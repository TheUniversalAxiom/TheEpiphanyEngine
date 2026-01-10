"""
Performance benchmarks for The EPIPHANY Engine.
"""

from .performance import (
    benchmark_computation,
    benchmark_simulation,
    benchmark_update_rules,
    run_all_benchmarks,
)

__all__ = [
    'benchmark_computation',
    'benchmark_simulation',
    'benchmark_update_rules',
    'run_all_benchmarks'
]
