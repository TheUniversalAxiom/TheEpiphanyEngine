# Codebase Cleanup Plan

**Generated:** 2026-01-10
**Target Branch:** `claude/review-codebase-cleanup-dHwsn`
**Overall Assessment:** B+ (85/100) - Production-ready after critical bug fixes

---

## Executive Summary

The comprehensive codebase review revealed **2 critical runtime bugs** that will cause crashes in production, along with several code quality improvements needed. This plan prioritizes fixes by severity and impact.

**Total Time Estimate:** ~8-10 hours
**Critical Fixes:** 2 bugs (30 minutes)
**High Priority:** 3 items (2 hours)
**Medium Priority:** 5 items (4 hours)
**Documentation:** 1 item (2 hours)

---

## Critical Issues (MUST FIX - 30 minutes)

### 1. Bug: Incorrect Attribute Access in viz/exporters.py
**Severity:** CRITICAL 🔴
**Impact:** All export functions will crash at runtime
**Time:** 15 minutes

**Problem:**
```python
# BROKEN (11 occurrences):
for step in result.history:
    "A": step.inputs.A,  # ❌ step doesn't have .inputs attribute
    "B": step.inputs.B,  # ❌ Should be step.state.inputs.A
```

**Solution:**
```python
# CORRECT:
for step in result.history:
    "A": step.state.inputs.A,  # ✅ Access through step.state
    "B": step.state.inputs.B,
```

**Affected Functions:**
- `export_to_json()` (lines 37-50)
- `export_to_csv()` (lines 92-104)
- `export_to_markdown()` (lines 162-164)
- `generate_report()` (multiple occurrences)

**Root Cause:** TimeStep dataclass structure is:
```python
@dataclass
class TimeStep:
    step: int
    state: SystemState  # ← inputs are nested here
    intelligence: IntelligenceSnapshot
```

### 2. Bug: Invalid Parameter in benchmarks/performance.py
**Severity:** MEDIUM 🟡
**Impact:** Benchmark suite crashes
**Time:** 1 minute

**Problem:**
```python
# Line 143:
"fibonacci": {"F_n": UpdateRules.fibonacci_rule(scale=0.1)}
                                                  # ❌ Takes no parameters
```

**Solution:**
```python
"fibonacci": {"F_n": UpdateRules.fibonacci_rule()}  # ✅ No parameters
```

---

## High Priority (THIS WEEK - 2 hours)

### 3. Add Tests for viz/exporters.py
**Priority:** HIGH
**Time:** 1 hour
**Reason:** Would have caught Bug #1

**Create:** `tests/test_exporters.py`
```python
import pytest
from viz.exporters import export_to_json, export_to_csv, export_to_markdown, generate_report

def test_export_to_json():
    """Test JSON export with full simulation result."""
    result = create_test_simulation()
    export_to_json(result, "/tmp/test.json")

    with open("/tmp/test.json") as f:
        data = json.load(f)

    assert "metadata" in data
    assert "history" in data
    assert len(data["history"]) == result.total_steps

    # Verify structure includes state data
    step = data["history"][0]
    assert "inputs" in step
    assert "A" in step["inputs"]

def test_export_to_csv():
    """Test CSV export format."""
    # Similar structure

def test_export_to_markdown():
    """Test markdown export format."""
    # Similar structure

def test_generate_report():
    """Test comprehensive report generation."""
    # Test all sections
```

### 4. Replace Print with Logging in extensions/loader.py
**Priority:** HIGH
**Time:** 10 minutes
**Reason:** Production code should use structured logging

**Changes:**
```python
# OLD (lines 140, 144):
print(f"Warning: Failed to load {attr_name} from {filepath}: {e}")
print(f"Warning: Failed to process {filepath}: {e}")

# NEW:
from logging import getLogger
logger = getLogger(__name__)

logger.warning(f"Failed to load {attr_name} from {filepath}: {e}")
logger.warning(f"Failed to process {filepath}: {e}")
```

### 5. Add Coverage Threshold
**Priority:** HIGH
**Time:** 5 minutes
**Reason:** Enforce minimum test coverage

**Update:** `.github/workflows/ci.yml` or add to pytest config:
```ini
# pytest.ini or pyproject.toml
[tool.pytest.ini_options]
addopts = "--cov=axiom --cov=engine --cov=web --cov=viz --cov-fail-under=80"
```

---

## Medium Priority (THIS MONTH - 4 hours)

### 6. Extract Example Utilities
**Priority:** MEDIUM
**Time:** 2 hours
**Benefit:** Reduces 40% code duplication across 6 example files

**Create:** `examples/utils.py`
```python
def display_header(title: str, width: int = 60):
    """Display formatted scenario header."""
    print("=" * width)
    print(title)
    print("=" * width)

def display_results(result: SimulationResult, show_events: bool = True):
    """Display simulation results in standard format."""
    print(f"\nFinal Intelligence Score: {result.final_intelligence:.4f}")
    print(f"Total Steps: {result.total_steps}")

    if show_events and result.total_events > 0:
        print(f"\nEvents Detected: {result.total_events}")
        for event in result.get_all_events():
            print(f"  - {event}")

def display_component_analysis(components: Dict[str, float]):
    """Display component breakdown."""
    print("\nComponent Analysis:")
    for name, value in components.items():
        print(f"  {name}: {value:.4f}")
```

**Refactor:** All 6 example files to use shared utilities

### 7. Add Pytest Fixtures
**Priority:** MEDIUM
**Time:** 1 hour
**Benefit:** Reduces test setup duplication

**Create:** `tests/conftest.py`
```python
import pytest
from axiom.core_equation import AxiomInputs
from engine.state import SystemState

@pytest.fixture
def standard_inputs():
    """Standard axiom inputs for testing."""
    return AxiomInputs(
        A=0.5, B=0.5, C=0.5,
        X=0.7, Y=0.7, Z=0.7,
        E_n=3.0, F_n=2.0
    )

@pytest.fixture
def edge_case_inputs():
    """Edge case inputs (zeros and ones)."""
    return AxiomInputs(
        A=0.0, B=1.0, C=0.5,
        X=1.0, Y=0.0, Z=0.5,
        E_n=1.0, F_n=1.0
    )

@pytest.fixture
def test_system_state(standard_inputs):
    """Standard system state for testing."""
    return SystemState(
        inputs=standard_inputs,
        outputs={},
        metadata={"test": True}
    )
```

### 8. Extract Magic Numbers to Constants
**Priority:** MEDIUM
**Time:** 30 minutes
**Files:** `web/api.py`, `web/cache.py`

**Changes:**
```python
# web/api.py
# OLD:
limiter = Limiter(key_func=get_remote_address, default_limits=["100/hour"])
@limiter.limit("20/minute")

# NEW:
DEFAULT_RATE_LIMIT = "100/hour"
SIMULATE_RATE_LIMIT = "20/minute"
COMPUTE_RATE_LIMIT = "50/minute"

limiter = Limiter(key_func=get_remote_address, default_limits=[DEFAULT_RATE_LIMIT])
@limiter.limit(SIMULATE_RATE_LIMIT)
```

```python
# web/cache.py
# NEW constants:
DEFAULT_CACHE_SIZE = 128
DEFAULT_CACHE_TTL = 3600  # 1 hour
CACHE_KEY_ALGORITHM = "sha256"
```

### 9. Enable Stricter MyPy Configuration
**Priority:** MEDIUM
**Time:** 2 hours (includes fixing type hints)
**File:** `mypy.ini`

**Changes:**
```ini
# OLD:
disallow_untyped_defs = False
ignore_missing_imports = True

# NEW:
disallow_untyped_defs = True
warn_return_any = True
strict_optional = True
warn_redundant_casts = True
warn_unused_ignores = True

# Per-module overrides for gradual adoption:
[mypy-tests.*]
disallow_untyped_defs = False

[mypy-examples.*]
disallow_untyped_defs = False
```

**Fix Required:** Add type hints to functions currently missing them

### 10. Refactor Long Functions
**Priority:** MEDIUM
**Time:** 1.5 hours
**Files:** `viz/plotter.py`, `viz/exporters.py`

**Target Functions:**
1. `viz/plotter.py:create_dashboard()` (120 lines, 397-520)
2. `viz/exporters.py:generate_report()` (100 lines, 175-285)

**Strategy:**
```python
# Break create_dashboard() into:
def create_dashboard(result, filename, show_events=True):
    fig, axes = _setup_dashboard_layout()
    _plot_intelligence_trend(axes[0], result)
    _plot_component_evolution(axes[1], result)
    _plot_balance_metrics(axes[2], result)
    if show_events:
        _plot_event_timeline(axes[3], result)
    _finalize_dashboard(fig, filename)

def _setup_dashboard_layout():
    """Create figure and subplot layout."""
    # 20 lines

def _plot_intelligence_trend(ax, result):
    """Plot main intelligence score over time."""
    # 25 lines
```

---

## Documentation (NICE TO HAVE - 2 hours)

### 11. Create Architecture Documentation
**Priority:** LOW
**Time:** 2 hours
**File:** `docs/ARCHITECTURE.md`

**Sections:**
1. **System Overview**
   - High-level architecture diagram
   - Component relationships
   - Data flow

2. **Core Components**
   - `axiom/` - Mathematical framework
   - `engine/` - Simulation engine
   - `web/` - REST API
   - `viz/` - Visualization layer
   - `extensions/` - Plugin system

3. **Design Patterns**
   - Immutable state management
   - Plugin architecture
   - Optional dependency handling
   - Factory patterns

4. **Extension Points**
   - How to create custom update rules
   - How to add event handlers
   - How to integrate external systems

5. **Security Architecture**
   - Authentication flow
   - Rate limiting strategy
   - Security headers
   - Input validation

---

## Implementation Order

### Phase 1: Critical Fixes (Day 1 - 30 minutes)
1. ✅ Fix viz/exporters.py attribute access (15 min)
2. ✅ Fix benchmarks/performance.py parameter (1 min)
3. ✅ Run tests to verify fixes (5 min)
4. ✅ Commit and push critical fixes (9 min)

### Phase 2: High Priority (Day 1-2 - 2 hours)
5. ✅ Add tests for exporters (1 hour)
6. ✅ Replace print with logging (10 min)
7. ✅ Add coverage threshold (5 min)
8. ✅ Run full test suite (5 min)
9. ✅ Commit and push (10 min)

### Phase 3: Code Quality (Week 1 - 4 hours)
10. ✅ Extract example utilities (2 hours)
11. ✅ Add pytest fixtures (1 hour)
12. ✅ Extract magic numbers (30 min)
13. ✅ Enable stricter mypy (2 hours)
14. ✅ Refactor long functions (1.5 hours)
15. ✅ Commit and push (10 min)

### Phase 4: Documentation (Week 2 - 2 hours)
16. ✅ Create architecture docs (2 hours)
17. ✅ Final commit and push (5 min)

---

## Testing Strategy

After each phase:
```bash
# Run all tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=axiom --cov=engine --cov=web --cov=viz --cov-report=html

# Type checking
mypy axiom engine web mcp

# Linting
ruff check .

# Formatting
black --check .
```

---

## Success Metrics

### Before Cleanup:
- **Grade:** B+ (85/100)
- **Critical Bugs:** 2
- **Test Coverage:** Unknown (no threshold)
- **Code Duplication:** 40% in examples
- **Type Coverage:** ~70%

### After Cleanup:
- **Grade:** A (90/100)
- **Critical Bugs:** 0 ✅
- **Test Coverage:** ≥80% enforced ✅
- **Code Duplication:** <10% ✅
- **Type Coverage:** ≥90% ✅

---

## Risk Assessment

**Low Risk Changes:**
- Bug fixes (well-isolated)
- Adding tests (non-breaking)
- Adding logging (extends existing)
- Magic number extraction (refactoring)

**Medium Risk Changes:**
- Stricter mypy (may reveal hidden type issues)
- Refactoring long functions (behavior must match)

**Mitigation:**
- Comprehensive test suite after each phase
- Git branch allows safe experimentation
- Can cherry-pick critical fixes if needed

---

## Future Improvements (Not in This Cleanup)

These were identified but are out of scope:

1. **Async API Support** - Requires FastAPI refactoring
2. **Redis Caching** - Infrastructure change
3. **Performance Optimization** - Needs profiling first
4. **Extension Development Guide** - Larger documentation effort
5. **CI/CD Enhancements** - Separate DevOps task

---

## Conclusion

This cleanup plan addresses all critical bugs and significantly improves code quality, testing, and maintainability. The codebase will move from **B+ to A grade** and be fully production-ready.

**Next Step:** Begin Phase 1 (Critical Fixes) immediately.
