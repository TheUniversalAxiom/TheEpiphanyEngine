# Contributing to The EPIPHANY Engine

Thank you for your interest in contributing to The EPIPHANY Engine! This document provides guidelines and information for contributors.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [How to Contribute](#how-to-contribute)
5. [Coding Standards](#coding-standards)
6. [Testing Guidelines](#testing-guidelines)
7. [Documentation](#documentation)
8. [Pull Request Process](#pull-request-process)
9. [Community](#community)

---

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors, regardless of background or experience level.

### Expected Behavior

- Be respectful and constructive in discussions
- Welcome newcomers and help them get started
- Focus on what is best for the community and the project
- Show empathy towards other community members

### Unacceptable Behavior

- Harassment, discrimination, or offensive comments
- Trolling or insulting/derogatory comments
- Publishing others' private information
- Other conduct which could reasonably be considered inappropriate

---

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Git
- Basic understanding of intelligence models and simulations (helpful but not required)

### First Steps

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/TheEpiphanyEngine.git
   cd TheEpiphanyEngine
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/TheUniversalAxiom/TheEpiphanyEngine.git
   ```

---

## Development Setup

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
# Core dependencies
pip install -r requirements.txt

# Development dependencies (optional)
pip install pytest pytest-cov black ruff mypy
```

### 3. Verify Installation

```bash
# Run tests
pytest tests/ -v

# Run examples
python examples/run_all.py

# Run benchmarks
python benchmarks/performance.py
```

---

## How to Contribute

### Areas Where We Need Help

1. **Core Engine**
   - Performance optimizations
   - New update rule implementations
   - Mathematical extensions

2. **Examples & Documentation**
   - Real-world use cases
   - Tutorial notebooks
   - API documentation improvements

3. **Visualization**
   - New plot types
   - Interactive visualizations
   - Dashboard enhancements

4. **Extensions**
   - Domain-specific models
   - Integration adapters
   - Custom analysis tools

5. **Testing**
   - Edge case coverage
   - Performance benchmarks
   - Integration tests

### Finding Issues to Work On

- Check [GitHub Issues](https://github.com/TheUniversalAxiom/TheEpiphanyEngine/issues)
- Look for `good-first-issue` labels
- Look for `help-wanted` labels
- Propose new features in discussions

---

## Coding Standards

### Python Style

We follow **PEP 8** with some modifications:

- **Line length**: 100 characters (not 79)
- **Indentation**: 4 spaces
- **Quotes**: Double quotes for strings
- **Imports**: Grouped (stdlib, third-party, local)

### Code Formatting

We use **Black** for code formatting:

```bash
black axiom/ engine/ examples/ tests/ viz/ extensions/
```

### Linting

We use **Ruff** for linting:

```bash
ruff check axiom/ engine/ examples/ tests/ viz/ extensions/
```

### Type Hints

- Use type hints for all public APIs
- Use type hints for complex internal functions
- Run mypy for type checking:
  ```bash
  mypy axiom/ engine/
  ```

### Documentation Standards

#### Docstrings

Use Google-style docstrings:

```python
def compute_intelligence(
    A: float,
    B: float,
    C: float,
    **kwargs
) -> float:
    """
    Compute intelligence score using the Universal Axiom.

    The intelligence equation is:
        Intelligence = E_n * (1 + F_n) * X * Y * Z * (A * B * C)

    Args:
        A: Alignment/Accuracy parameter [0, 1]
        B: Broadness/Behavior parameter [0, 1]
        C: Capacity parameter [0, 1]
        **kwargs: Additional parameters (X, Y, Z, E_n, F_n)

    Returns:
        Intelligence score as float

    Raises:
        ValueError: If parameters are out of bounds and strict_bounds=True

    Example:
        >>> score = compute_intelligence(A=0.7, B=0.7, C=0.7,
        ...                               X=0.7, Y=0.7, Z=0.7,
        ...                               E_n=5.0, F_n=3.0)
        >>> print(f"Intelligence: {score:.2f}")
    """
    # Implementation here
```

#### Comments

- Use comments to explain "why", not "what"
- Keep comments up-to-date with code changes
- Avoid obvious comments

---

## Testing Guidelines

### Writing Tests

1. **Test file naming**: `test_<module_name>.py`
2. **Test class naming**: `Test<FeatureName>`
3. **Test function naming**: `test_<behavior_being_tested>`

### Test Structure

```python
def test_feature_behavior():
    """Test that feature behaves correctly under normal conditions."""
    # Arrange
    input_data = create_test_input()

    # Act
    result = feature_function(input_data)

    # Assert
    assert result == expected_output
    assert result.property > threshold
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_core_equation.py -v

# Run with coverage
pytest tests/ --cov=axiom --cov=engine --cov-report=html
```

### Test Coverage Goals

- **Core modules** (axiom, engine): 90%+ coverage
- **Application modules** (web, mcp): 80%+ coverage
- **Utilities** (viz, extensions): 70%+ coverage

---

## Documentation

### Types of Documentation

1. **Code Documentation**
   - Docstrings for all public APIs
   - Inline comments for complex logic
   - Type hints

2. **API Reference**
   - Located in `docs/API_REFERENCE.md`
   - Auto-generated from docstrings (future)

3. **User Guides**
   - Tutorials in `notebooks/`
   - Examples in `examples/`
   - README.md for quick start

4. **Research Documentation**
   - Mathematical derivations in `substrate/`
   - AGENTS.md and SKILLS.md for frameworks

### Adding Documentation

When adding new features:

1. Add docstrings to all public functions/classes
2. Create an example in `examples/` if applicable
3. Update `docs/API_REFERENCE.md`
4. Update README.md if it's a major feature
5. Consider adding a Jupyter notebook tutorial

---

## Pull Request Process

### Before Submitting

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**:
   - Follow coding standards
   - Add tests
   - Update documentation

3. **Run quality checks**:
   ```bash
   # Format code
   black axiom/ engine/ examples/ tests/

   # Run linter
   ruff check .

   # Run tests
   pytest tests/ -v

   # Type checking
   mypy axiom/ engine/
   ```

4. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: add new update rule for exponential growth"
   ```

### Commit Message Format

We follow **Conventional Commits**:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Adding or updating tests
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `chore`: Maintenance tasks

**Example:**
```
feat(engine): add exponential growth update rule

Implemented new update rule for exponential growth with
configurable base and rate parameters. Includes comprehensive
tests and documentation.

Closes #42
```

### Submitting Pull Request

1. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Open Pull Request** on GitHub

3. **Fill out PR template**:
   - Describe what changes you made
   - Reference related issues
   - Add screenshots if applicable
   - Check all boxes in the checklist

4. **Respond to review feedback**:
   - Address all comments
   - Make requested changes
   - Push updates to the same branch

### PR Review Process

1. Automated checks run (tests, linting, etc.)
2. Maintainer reviews code
3. Feedback provided (if needed)
4. Changes approved
5. PR merged to main branch

---

## Community

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and ideas
- **Pull Requests**: Code contributions

### Getting Help

- Check existing documentation first
- Search GitHub issues for similar questions
- Ask in GitHub Discussions
- Reference the API documentation

### Recognition

Contributors are recognized in:
- GitHub contributors page
- CONTRIBUTORS.md file (future)
- Release notes for significant contributions

---

## Development Workflow

### Typical Workflow

1. Check for existing issues or create new one
2. Discuss approach in issue comments
3. Fork repository and create feature branch
4. Implement changes with tests
5. Run quality checks locally
6. Submit pull request
7. Respond to review feedback
8. Merge once approved

### Branching Strategy

- `main`: Stable release branch
- `develop`: Integration branch (if used)
- `feature/*`: Feature branches
- `fix/*`: Bug fix branches
- `docs/*`: Documentation branches

### Release Process

1. Version bump in relevant files
2. Update CHANGELOG.md
3. Tag release
4. Create GitHub release
5. Publish to PyPI (future)

---

## Extension Development

### Creating Extensions

1. Subclass `BaseExtension` or specific extension type
2. Implement required abstract methods
3. Add tests
4. Document in docstrings
5. Create example usage

**Example:**
```python
from extensions.base import UpdateRuleExtension

class MyCustomRulesExtension(UpdateRuleExtension):
    def __init__(self):
        super().__init__("my-custom-rules", "1.0.0")

    def initialize(self):
        print("Initializing custom rules extension")

    def get_metadata(self):
        return {
            "author": "Your Name",
            "description": "Custom update rules for specific domain",
            "license": "MIT"
        }

    def get_update_rules(self):
        return {
            "custom_growth": self._custom_growth_rule
        }

    def get_rule_descriptions(self):
        return {
            "custom_growth": "Custom growth pattern for domain X"
        }

    def _custom_growth_rule(self, inputs, step):
        # Custom logic here
        return min(1.0, inputs.A + 0.01 * step)
```

---

## Questions?

If you have questions not covered in this guide:

1. Check the [API Reference](docs/API_REFERENCE.md)
2. Look at existing examples in `examples/`
3. Search GitHub Issues
4. Create a new Discussion on GitHub

**Thank you for contributing to The EPIPHANY Engine!** 🚀
