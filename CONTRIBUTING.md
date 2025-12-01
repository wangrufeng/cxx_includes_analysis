# Contributing to C++ Dependency Analyzer

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [How to Contribute](#how-to-contribute)
4. [Development Setup](#development-setup)
5. [Coding Standards](#coding-standards)
6. [Testing](#testing)
7. [Pull Request Process](#pull-request-process)
8. [Reporting Bugs](#reporting-bugs)
9. [Suggesting Features](#suggesting-features)

## Code of Conduct

This project follows a simple code of conduct:

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Respect differing viewpoints and experiences

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/cxx_includes_analysis.git
   cd cxx_includes_analysis
   ```
3. Add the upstream repository:
   ```bash
   git remote add upstream https://github.com/ORIGINAL_OWNER/cxx_includes_analysis.git
   ```
4. Create a branch for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## How to Contribute

### Types of Contributions

We welcome various types of contributions:

- **Bug fixes**: Fix issues reported in the issue tracker
- **Features**: Add new functionality
- **Documentation**: Improve or add documentation
- **Examples**: Add example use cases
- **Tests**: Add or improve test coverage
- **Performance**: Optimize existing code
- **Refactoring**: Improve code structure

### Before You Start

1. Check existing issues to avoid duplicate work
2. For major changes, open an issue first to discuss
3. Make sure your idea aligns with project goals
4. Review the coding standards below

## Development Setup

### Prerequisites

- Python 3.6 or higher
- Git

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/cxx_includes_analysis.git
cd cxx_includes_analysis

# Create a virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Install development dependencies (optional)
pip install pytest pytest-cov black flake8 mypy
```

### Project Structure

```
cxx_includes_analysis/
├── analyze_includes.py          # Main CLI script
├── analyze_i_file.py            # Preprocessed file analyzer
├── analyze_includes_lib/        # Core library
│   ├── __init__.py
│   ├── analyzer.py              # Dependency analyzer
│   ├── config.py                # Configuration
│   ├── dot_visualizer.py        # DOT format generator
│   ├── html_visualizer.py       # HTML generator
│   ├── html_template.py         # HTML templates
│   └── utils.py                 # Utility functions
├── examples/                    # Example projects
├── docs/                        # Documentation
├── tests/                       # Test suite (to be added)
├── README.md                    # English README
├── README_zh.md                 # Chinese README
├── setup.py                     # Package setup
└── requirements.txt             # Dependencies
```

## Coding Standards

### Python Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use 4 spaces for indentation (no tabs)
- Maximum line length: 100 characters
- Use meaningful variable and function names

### Code Formatting

We recommend using `black` for code formatting:

```bash
black analyze_includes_lib/
```

### Linting

Check your code with `flake8`:

```bash
flake8 analyze_includes_lib/ --max-line-length=100
```

### Type Hints

Use type hints where appropriate:

```python
def analyze_file(path: str, depth: int = 3) -> tuple[dict, list]:
    """Analyze a C++ file."""
    ...
```

### Documentation

- Add docstrings to all public functions and classes
- Use clear, concise language
- Include examples where helpful

Example:

```python
def get_file_size(path: str) -> int:
    """
    Get the size of a file in bytes.
    
    Args:
        path: Path to the file
        
    Returns:
        File size in bytes, or 0 if file doesn't exist
        
    Example:
        >>> get_file_size("main.cpp")
        1024
    """
    ...
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=analyze_includes_lib

# Run specific test file
pytest tests/test_analyzer.py
```

### Writing Tests

- Add tests for new features
- Ensure existing tests pass
- Aim for good test coverage
- Use descriptive test names

Example:

```python
def test_analyzer_finds_direct_includes():
    """Test that analyzer finds direct #include statements."""
    analyzer = DependencyAnalyzer(["."])
    nodes, edges = analyzer.analyze("test_file.cpp")
    assert len(nodes) > 0
    assert len(edges) > 0
```

## Pull Request Process

### Before Submitting

1. Update your branch with the latest upstream changes:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. Ensure your code follows the coding standards

3. Add or update tests as needed

4. Update documentation if you changed functionality

5. Test your changes thoroughly

### Submitting a Pull Request

1. Push your branch to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. Go to GitHub and create a Pull Request

3. Fill out the PR template with:
   - Clear description of changes
   - Related issue numbers (if any)
   - Testing performed
   - Screenshots (for UI changes)

4. Wait for review and address feedback

### PR Title Format

Use clear, descriptive titles:

- `feat: Add support for CMake projects`
- `fix: Correct path handling on Windows`
- `docs: Update API documentation`
- `refactor: Simplify analyzer logic`
- `test: Add tests for visualizer`

### Review Process

- Maintainers will review your PR
- Address feedback promptly
- Be open to suggestions
- Once approved, your PR will be merged

## Reporting Bugs

### Before Reporting

1. Check if the bug is already reported
2. Verify it's reproducible
3. Test with the latest version

### Bug Report Template

```markdown
**Description**
A clear description of the bug.

**To Reproduce**
Steps to reproduce:
1. Run command '...'
2. See error

**Expected Behavior**
What you expected to happen.

**Actual Behavior**
What actually happened.

**Environment**
- OS: [e.g., Ubuntu 20.04]
- Python version: [e.g., 3.8.5]
- Tool version: [e.g., 2.0.0]

**Additional Context**
Any other relevant information.
```

## Suggesting Features

### Feature Request Template

```markdown
**Feature Description**
Clear description of the feature.

**Use Case**
Why is this feature needed? What problem does it solve?

**Proposed Solution**
How you think it should work.

**Alternatives Considered**
Other approaches you've thought about.

**Additional Context**
Any other relevant information, mockups, or examples.
```

## Development Tips

### Testing Locally

```bash
# Test with example files
python3 analyze_includes.py examples/simple/main.cpp -I examples/simple

# Test batch analysis
python3 analyze_includes.py examples/simple/*.cpp
```

### Debugging

Add debug prints or use Python debugger:

```python
import pdb; pdb.set_trace()
```

### Performance Profiling

```python
import cProfile
cProfile.run('analyzer.analyze("main.cpp")')
```

## Questions?

If you have questions:

1. Check the [documentation](docs/)
2. Search existing issues
3. Open a new issue with the "question" label

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

## Recognition

Contributors will be recognized in:
- The project README
- Release notes
- GitHub contributors page

Thank you for contributing! 🎉

