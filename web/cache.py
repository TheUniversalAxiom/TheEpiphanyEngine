"""
Caching utilities for Epiphany Engine API.

Provides in-memory caching for simulation results to improve performance.
"""

import hashlib
import json
import time
from functools import lru_cache
from typing import Any, Dict, Optional, Tuple


class SimulationCache:
    """
    LRU cache for simulation results with TTL support.

    Uses a simple dict-based cache with time-based expiration.
    For production with multiple workers, consider Redis.
    """

    def __init__(self, max_size: int = 128, ttl_seconds: int = 3600):
        """
        Initialize simulation cache.

        Args:
            max_size: Maximum number of cached results
            ttl_seconds: Time-to-live for cache entries (default: 1 hour)
        """
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self._cache: Dict[str, Tuple[float, Any]] = {}
        self._access_times: Dict[str, float] = {}

    def _generate_cache_key(self, request_data: Dict[str, Any]) -> str:
        """
        Generate a cache key from request parameters.

        Creates a deterministic hash from the sorted request parameters.

        Args:
            request_data: Request parameters

        Returns:
            Cache key (hex string)
        """
        # Sort keys for deterministic hashing
        sorted_data = json.dumps(request_data, sort_keys=True)
        return hashlib.sha256(sorted_data.encode()).hexdigest()

    def get(self, request_data: Dict[str, Any]) -> Optional[Any]:
        """
        Get cached result if available and not expired.

        Args:
            request_data: Request parameters to look up

        Returns:
            Cached result or None if not found/expired
        """
        cache_key = self._generate_cache_key(request_data)

        if cache_key not in self._cache:
            return None

        timestamp, cached_value = self._cache[cache_key]
        current_time = time.time()

        # Check if expired
        if current_time - timestamp > self.ttl_seconds:
            # Remove expired entry
            del self._cache[cache_key]
            if cache_key in self._access_times:
                del self._access_times[cache_key]
            return None

        # Update access time for LRU
        self._access_times[cache_key] = current_time
        return cached_value

    def set(self, request_data: Dict[str, Any], result: Any) -> None:
        """
        Cache a simulation result.

        If cache is full, removes least recently used entry.

        Args:
            request_data: Request parameters (cache key)
            result: Simulation result to cache
        """
        cache_key = self._generate_cache_key(request_data)
        current_time = time.time()

        # If cache is full, remove LRU entry
        if len(self._cache) >= self.max_size and cache_key not in self._cache:
            # Find least recently used
            lru_key = min(self._access_times.items(), key=lambda x: x[1])[0]
            del self._cache[lru_key]
            del self._access_times[lru_key]

        # Store result with timestamp
        self._cache[cache_key] = (current_time, result)
        self._access_times[cache_key] = current_time

    def clear(self) -> None:
        """Clear all cached entries."""
        self._cache.clear()
        self._access_times.clear()

    def size(self) -> int:
        """Get current cache size."""
        return len(self._cache)

    def stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            Dictionary with cache stats
        """
        return {
            "size": len(self._cache),
            "max_size": self.max_size,
            "ttl_seconds": self.ttl_seconds,
            "utilization": len(self._cache) / self.max_size if self.max_size > 0 else 0,
        }


# Global cache instance
# For production with multiple workers, use Redis instead
_simulation_cache = SimulationCache(max_size=128, ttl_seconds=3600)


def get_simulation_cache() -> SimulationCache:
    """
    Get the global simulation cache instance.

    Returns:
        SimulationCache instance
    """
    return _simulation_cache


@lru_cache(maxsize=32)
def cached_fibonacci(n: int) -> int:
    """
    Cached Fibonacci sequence computation.

    Uses LRU cache for frequently accessed Fibonacci numbers.

    Args:
        n: Index in Fibonacci sequence

    Returns:
        Fibonacci number at index n
    """
    if n <= 0:
        return 0
    if n == 1:
        return 1

    prev, current = 0, 1
    for _ in range(2, n + 1):
        prev, current = current, prev + current
    return current


@lru_cache(maxsize=64)
def cached_e_sequence(n: int, a: float = 3.0, b: float = 2.0) -> float:
    """
    Cached E_n sequence computation.

    Uses LRU cache for frequently accessed E_n values.

    Args:
        n: Step number
        a: Recurrence coefficient
        b: Recurrence constant

    Returns:
        E_n value at step n
    """
    if n == 0:
        return b
    return a * cached_e_sequence(n - 1, a, b) + b


def clear_all_caches() -> None:
    """Clear all caches (simulation cache and LRU caches)."""
    _simulation_cache.clear()
    cached_fibonacci.cache_clear()
    cached_e_sequence.cache_clear()


def get_cache_stats() -> Dict[str, Any]:
    """
    Get statistics for all caches.

    Returns:
        Dictionary with cache statistics
    """
    return {
        "simulation_cache": _simulation_cache.stats(),
        "fibonacci_cache": {
            "hits": cached_fibonacci.cache_info().hits,
            "misses": cached_fibonacci.cache_info().misses,
            "size": cached_fibonacci.cache_info().currsize,
            "max_size": cached_fibonacci.cache_info().maxsize,
        },
        "e_sequence_cache": {
            "hits": cached_e_sequence.cache_info().hits,
            "misses": cached_e_sequence.cache_info().misses,
            "size": cached_e_sequence.cache_info().currsize,
            "max_size": cached_e_sequence.cache_info().maxsize,
        },
    }
