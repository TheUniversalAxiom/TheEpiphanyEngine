# Development Guide - The Epiphany Engine

This guide provides detailed information for developers working on The Epiphany Engine.

## Table of Contents

1. [Environment Setup](#environment-setup)
2. [Project Structure](#project-structure)
3. [Running Tests](#running-tests)
4. [Code Style](#code-style)
5. [Debugging](#debugging)
6. [Common Tasks](#common-tasks)

## Environment Setup

### Recommended Tools

- **IDE:** VS Code, PyCharm, or similar with Python support
- **Python:** 3.9, 3.10, 3.11, or 3.12
- **Docker:** For containerized development (optional)

### IDE Configuration

#### VS Code

Create `.vscode/settings.json`:

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["tests"],
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "editor.formatOnSave": true
}
```

Create `.vscode/launch.json` for debugging:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Current File",
      "type": "python",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal"
    },
    {
      "name": "Python: Run Tests",
      "type": "python",
      "request": "launch",
      "module": "pytest",
      "args": ["-v"],
      "console": "integratedTerminal"
    },
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["web.api:app", "--reload"],
      "console": "integratedTerminal"
    }
  ]
}
```

#### PyCharm

1. File → Settings → Project → Python Interpreter
2. Add virtual environment: `./venv`
3. Enable pytest as test runner
4. Configure Black as formatter

## Project Structure

```
TheEpiphanyEngine/
├── axiom/                    # Core axiom implementation
│   ├── core_equation.py     # Intelligence computation engine
│   ├── subjectivity_scale.py # X-axis (objectivity) measurement
│   └── components/          # Component-based architecture
│
├── engine/                  # TimeSphere simulation engine
│   ├── state.py            # Data models (AxiomInputs, IntelligenceSnapshot, SystemState)
│   └── timesphere.py       # Time-based evolution simulation
│
├── web/                     # REST API and web services
│   ├── api.py              # FastAPI application (endpoints, routes)
│   ├── auth.py             # Authentication/authorization logic
│   ├── security.py         # Security headers and middleware
│   ├── cache.py            # Caching utilities
│   └── logging_config.py   # Structured logging setup
│
├── viz/                     # Visualization & export
│   ├── plotter.py          # Matplotlib-based plotting
│   └── exporters.py        # JSON/CSV/Markdown export
│
├── mcp/                     # Model Context Protocol server
│   └── server.py           # MCP implementation
│
├── extensions/              # Plugin/extension system
│   ├── base.py             # Base extension classes
│   ├── registry.py         # Extension discovery/loading
│   ├── loader.py           # Dynamic extension loading
│   └── examples/           # Example extensions
│
├── benchmarks/             # Performance benchmarking
│   └── performance.py      # Benchmark suite
│
├── examples/               # Runnable scenario examples (6 examples)
│   └── run_all.py         # Run all examples
│
└── tests/                  # Comprehensive test suite (97 tests)
    └── test_*.py          # Test modules
```

## Running Tests

### Test Organization

```
tests/
├── test_core_equation.py    # Mathematical core tests
├── test_timesphere.py        # Simulation engine tests
├── test_api.py               # REST API integration tests
├── test_validation.py        # Input validation tests
├── test_exporters.py         # Export functionality tests
├── test_plotter.py           # Visualization tests
├── test_components.py        # Component system tests
├── test_examples.py          # Example scenario tests
└── test_logging_context.py  # Logging system tests
```

### Test Commands Reference

```bash
# Run all tests
pytest

# Verbose output
pytest -v

# Stop on first failure
pytest -x

# Run specific test
pytest tests/test_core_equation.py::test_compute_intelligence_basic

# Run tests matching pattern
pytest -k "intelligence"

# Show print statements
pytest -s

# Generate HTML coverage report
pytest --cov=axiom --cov=engine --cov-report=html
# Open htmlcov/index.html in browser

# Parallel execution (requires pytest-xdist)
pip install pytest-xdist
pytest -n auto
```

### Running Individual Test Files

```bash
# Core equation tests
pytest tests/test_core_equation.py -v

# API tests
pytest tests/test_api.py -v

# TimeSphere simulation tests
pytest tests/test_timesphere.py -v
```

## Code Style

The project follows strict code quality standards enforced by CI/CD.

### Black (Formatting)

```bash
# Format all files
black .

# Check without modifying
black --check .

# Format specific file
black axiom/core_equation.py

# Show what would be changed
black --diff .
```

### Ruff (Linting)

```bash
# Lint all files
ruff check .

# Auto-fix issues
ruff check --fix .

# Check specific file
ruff check web/api.py

# Explain a specific error
ruff rule E501
```

### mypy (Type Checking)

```bash
# Type check core modules
mypy axiom engine

# Strict mode
mypy --strict axiom/core_equation.py

# Generate HTML report
mypy axiom engine --html-report mypy-report

# Check specific file
mypy web/api.py --ignore-missing-imports
```

### Pre-commit Hooks

```bash
# Install pre-commit hooks
pre-commit install

# Run all hooks manually
pre-commit run --all-files

# Run specific hook
pre-commit run black --all-files

# Update hooks to latest versions
pre-commit autoupdate
```

## Debugging

### Using Python Debugger (pdb)

```python
# Add breakpoint in code
import pdb; pdb.set_trace()

# Or use Python 3.7+ built-in
breakpoint()

# Common pdb commands:
# n - next line
# s - step into function
# c - continue execution
# p <var> - print variable
# l - list code around current line
# q - quit debugger
```

### Debugging Tests

```bash
# Run test with pdb on failure
pytest --pdb

# Drop into debugger on first failure
pytest -x --pdb

# Verbose output with print statements
pytest -vv -s
```

### Logging for Debugging

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Or use the project's structured logging
from web.logging_config import setup_logging
logger = setup_logging(log_level="DEBUG")
logger.debug("Debugging information", extra={"context": "value"})
```

## Common Tasks

### Adding a New Example Scenario

1. **Create file** in `examples/` (e.g., `07_my_scenario.py`)

```python
from engine.timesphere import TimeSphere, UpdateRules
from engine.state import AxiomInputs

# Define initial state
initial = AxiomInputs(
    A=0.7, B=0.5, C=0.6,
    X=0.8, Y=0.4, Z=0.6,
    E_n=3.0, F_n=1.0
)

# Create simulation
sphere = TimeSphere(initial_inputs=initial)

# Add update rules
sphere.add_update_rule("A", UpdateRules.linear_growth(rate=0.05))

# Run simulation
result = sphere.simulate(steps=20)
print(f"Final Intelligence: {result.summary['final_intelligence']:.4f}")
```

2. **Add to** `examples/run_all.py`
3. **Create test** in `tests/test_examples.py`
4. **Document** the scenario in a docstring

### Adding a New API Endpoint

1. **Define Pydantic model** in `web/api.py`

```python
class MyNewRequest(BaseModel):
    parameter1: float = Field(..., ge=0.0, le=1.0)
    parameter2: str = Field(..., max_length=100)
```

2. **Add route handler**

```python
@app.post("/api/my-endpoint")
async def my_endpoint(request: MyNewRequest):
    # Implementation
    return {"result": "success"}
```

3. **Add to endpoint list** in `/api/info`
4. **Write tests** in `tests/test_api.py`

```python
def test_my_new_endpoint():
    response = client.post("/api/my-endpoint", json={
        "parameter1": 0.5,
        "parameter2": "test"
    })
    assert response.status_code == 200
```

5. **Update** `docs/API_REFERENCE.md`

### Adding a New Component

1. **Create file** in `axiom/components/` (e.g., `my_component.py`)

```python
from axiom.components.base import BaseComponent

class MyComponent(BaseComponent):
    def __init__(self, value: float):
        super().__init__(name="MyComponent", value=value)

    def validate(self) -> bool:
        return 0.0 <= self.value <= 1.0
```

2. **Add tests** in `tests/test_components.py`
3. **Update documentation**
4. **Import in** `axiom/components/__init__.py`

### Adding a New Update Rule

1. **Add to** `engine/timesphere.py` in the `UpdateRules` class

```python
@staticmethod
def my_rule(param1: float, param2: float):
    def rule(state: SystemState, step: int) -> float:
        # Implementation
        return new_value
    return rule
```

2. **Document** the rule with docstring
3. **Add tests** in `tests/test_timesphere.py`
4. **Add example usage** in docstring or examples/

## Performance Profiling

### Using cProfile

```bash
# Profile a script
python -m cProfile -o profile.stats examples/01_basic_growth.py

# View results
python -m pstats profile.stats
# Then in pstats:
# > sort cumtime
# > stats 20
```

### Using line_profiler

```bash
# Install line_profiler
pip install line_profiler

# Add @profile decorator to function
# Then run:
kernprof -l -v your_script.py
```

### Memory Profiling

```bash
# Install memory_profiler
pip install memory_profiler

# Add @profile decorator
# Run with:
python -m memory_profiler your_script.py
```

## Working with Docker

### Build and Run Locally

```bash
# Build image
docker build -t epiphany-engine:dev .

# Run container
docker run -p 8000:8000 epiphany-engine:dev

# Run with environment variables
docker run -p 8000:8000 \
  -e API_KEY_ENABLED=true \
  -e API_KEY=your-secret-key \
  epiphany-engine:dev

# Access shell in running container
docker exec -it <container-id> /bin/bash
```

### Docker Compose for Development

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Rebuild after changes
docker-compose up -d --build

# Stop services
docker-compose down
```

## Contributing Workflow

1. **Create feature branch**
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Make changes** and test locally
   ```bash
   pytest tests/ -v
   black .
   ruff check .
   mypy axiom engine
   ```

3. **Commit with clear message**
   ```bash
   git commit -m "Add feature: description"
   ```

4. **Push and create PR**
   ```bash
   git push origin feature/my-feature
   ```

5. **Address review comments** and update PR

6. **Merge when approved**

See [CONTRIBUTING.md](CONTRIBUTING.md) for full guidelines.

## Environment Variables

### Development

```bash
# .env file for local development
API_KEY_ENABLED=false
JWT_ENABLED=false
LOG_LEVEL=DEBUG
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
HSTS_ENABLED=false
ENVIRONMENT=development
```

### Production

```bash
API_KEY_ENABLED=true
API_KEY=<secure-random-key>
JWT_ENABLED=true
JWT_SECRET=<secure-random-secret>
LOG_LEVEL=INFO
CORS_ORIGINS=https://yourdomain.com
HSTS_ENABLED=true
HTTPS_ENABLED=true
ENVIRONMENT=production
```

## Useful Commands

### Project Analysis

```bash
# Analyze project with axiom
python axiom_analysis.py

# Count lines of code
find . -name "*.py" -not -path "./venv/*" | xargs wc -l

# Find TODOs
grep -r "TODO\|FIXME" --include="*.py" .
```

### Database/Cache Management

```bash
# Clear pytest cache
rm -rf .pytest_cache

# Clear mypy cache
rm -rf .mypy_cache

# Clear __pycache__ directories
find . -type d -name __pycache__ -exec rm -rf {} +
```

### Generate Documentation

```bash
# Generate API documentation (if using sphinx)
cd docs
make html

# View documentation
open _build/html/index.html
```

## Troubleshooting

### Common Issues

#### Import Errors

**Problem:** `ModuleNotFoundError: No module named 'axiom'`

**Solution:**
```bash
# Ensure you're in project root
cd /path/to/TheEpiphanyEngine

# Activate virtual environment
source venv/bin/activate

# Add to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)
```

#### Test Failures

**Problem:** Tests pass locally but fail in CI

**Solution:**
- Check Python version compatibility (CI tests 3.9-3.12)
- Ensure all dependencies are in requirements.txt
- Check for environment-specific assumptions

#### Docker Build Fails

**Problem:** Docker build fails with permission errors

**Solution:**
```bash
# Clean docker cache
docker builder prune

# Build with no cache
docker build --no-cache -t epiphany-engine:dev .
```

## Additional Resources

- [README.md](README.md) - Quick start guide
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
- [DEPLOYMENT.md](DEPLOYMENT.md) - Production deployment
- [SECURITY.md](SECURITY.md) - Security practices
- [docs/API_REFERENCE.md](docs/API_REFERENCE.md) - API documentation

## Questions?

- Open an issue on GitHub
- Check existing issues and discussions
- Review the substrate/ directory for theoretical background
