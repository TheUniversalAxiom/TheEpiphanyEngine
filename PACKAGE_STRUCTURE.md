# Package Structure

## Overview

EPIPHANY Engine follows the **src-layout** structure, which is the modern Python packaging best practice.

## Directory Structure

```
TheEpiphanyEngine/
├── src/
│   └── epiphany_engine/          # Main package
│       ├── __init__.py            # Top-level exports
│       ├── axiom/                 # Core math module
│       │   ├── __init__.py
│       │   ├── core_equation.py
│       │   └── subjectivity_scale.py
│       └── engine/                # Simulation engine
│           ├── __init__.py
│           ├── state.py
│           └── timesphere.py
├── examples/                      # Example scenarios
├── tests/                         # Test suite
├── pyproject.toml                 # Package metadata
├── README.md
└── ...
```

## Installation

```bash
# Development/editable install (recommended for contributors)
pip install -e .

# Standard install (once published to PyPI)
pip install epiphany-engine
```

## Import Paths

### Top-Level Imports (Recommended)

The package exports commonly used classes and functions at the top level:

```python
from epiphany_engine import (
    TimeSphere,
    UpdateRules,
    AxiomInputs,
    SystemState,
    IntelligenceSnapshot,
    compute_intelligence,
    e_recurrence,
    fibonacci,
    x_from_observations,
    label_x,
)
```

### Module-Level Imports

You can also import from specific modules:

```python
# Axiom module
from epiphany_engine.axiom.core_equation import (
    compute_intelligence,
    e_recurrence,
    e_sequence,
    fibonacci,
    fibonacci_sequence,
)

from epiphany_engine.axiom.subjectivity_scale import (
    x_from_observations,
    label_x,
    x_with_label,
)

# Engine module
from epiphany_engine.engine.timesphere import (
    TimeSphere,
    UpdateRules,
    TimeStep,
    SimulationResult,
)

from epiphany_engine.engine.state import (
    AxiomInputs,
    IntelligenceSnapshot,
    SystemState,
)
```

## Why src-layout?

The src-layout has several advantages:

1. **Import correctness**: Forces you to install the package (even in editable mode) to import it, catching import errors early
2. **Namespace clarity**: Clear separation between package code and other files
3. **Test isolation**: Tests import from installed package, not local files
4. **Build reliability**: Prevents accidental inclusion of non-package files
5. **Modern standard**: Recommended by Python Packaging Authority (PyPA)

## Running Examples and Tests

After installing the package, all examples and tests work without sys.path manipulation:

```bash
# Run all examples
python examples/run_all.py

# Run all tests
python tests/run_all_tests.py

# Run analysis scripts
python axiom_analysis.py
python roadmap_analysis.py
python project_summary.py
```

## Package Metadata

Package configuration is in `pyproject.toml`:
- Package name: `epiphany-engine` (on PyPI)
- Import name: `epiphany_engine` (in Python code)
- Version: 0.1.0
- Python requirement: >=3.8

## For Contributors

When adding new modules:

1. Place them in `src/epiphany_engine/`
2. Add `__init__.py` if creating a new subpackage
3. Export important classes/functions in relevant `__init__.py` files
4. Update imports in examples/tests if needed
5. Run tests to verify: `python tests/run_all_tests.py`

## Migration from Old Structure

**Before:**
```python
from axiom.core_equation import compute_intelligence
from engine.timesphere import TimeSphere
```

**After:**
```python
# Top-level (recommended)
from epiphany_engine import compute_intelligence, TimeSphere

# Or module-level
from epiphany_engine.axiom.core_equation import compute_intelligence
from epiphany_engine.engine.timesphere import TimeSphere
```

All code has been updated to use the new structure.
