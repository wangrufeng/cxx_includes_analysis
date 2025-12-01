# Project Structure

This document describes the organization of the C++ Dependency Analyzer project.

## Directory Layout

```
cxx_includes_analysis/
│
├── analyze_includes.py          # Main CLI entry point
├── analyze_i_file.py            # Preprocessed file analyzer
│
├── analyze_includes_lib/        # Core library package
│   ├── __init__.py              # Package initialization and exports
│   ├── analyzer.py              # Dependency analysis engine
│   ├── config.py                # Configuration and constants
│   ├── dot_visualizer.py        # Graphviz DOT format generator
│   ├── html_visualizer.py       # Interactive HTML generator
│   ├── html_template.py         # HTML/CSS/JavaScript templates
│   ├── utils.py                 # Utility functions
│   └── README.md                # Library documentation
│
├── examples/                    # Example projects
│   ├── README.md                # Examples overview
│   └── simple/                  # Simple example project
│       ├── main.cpp
│       ├── utils.h
│       ├── config.h
│       └── README.md
│
├── docs/                        # Documentation
│   ├── USER_GUIDE.md            # Detailed user guide (English)
│   ├── USER_GUIDE_zh.md         # Detailed user guide (Chinese)
│   ├── API.md                   # API documentation (English)
│   └── images/                  # Screenshots and images
│       └── .gitkeep
│
├── .github/                     # GitHub specific files
│   └── workflows/
│       └── ci.yml               # CI/CD pipeline configuration
│
├── README.md                    # Main README (English)
├── README_zh.md                 # Main README (Chinese)
├── LICENSE                      # MIT License
├── CHANGELOG.md                 # Version history and changes
├── CONTRIBUTING.md              # Contribution guidelines
├── setup.py                     # Package installation script
├── requirements.txt             # Python dependencies
├── MANIFEST.in                  # Package manifest
├── .gitignore                   # Git ignore rules
└── PROJECT_STRUCTURE.md         # This file

```

## Module Descriptions

### Core Scripts

#### `analyze_includes.py`
Main command-line interface for analyzing C++ dependencies.

**Usage:**
```bash
python3 analyze_includes.py [source_files...] [options]
```

**Features:**
- Batch analysis of multiple files
- Configurable include paths
- Multiple output formats (HTML, DOT)
- Recursion depth control

#### `analyze_i_file.py`
Analyzes preprocessed C++ files (.i files) to determine which headers contribute the most code.

**Usage:**
```bash
python3 analyze_i_file.py <file.i>
```

### Library Package (`analyze_includes_lib/`)

#### `__init__.py`
Package initialization. Exports main classes and functions for external use.

**Exports:**
- `DependencyAnalyzer`
- `HtmlVisualizer`
- `DotVisualizer`
- `DEFAULT_INCLUDE_PATHS`
- Utility functions

#### `analyzer.py`
Core dependency analysis engine.

**Key Class:**
- `DependencyAnalyzer`: Analyzes C++ file dependencies

**Responsibilities:**
- Parse `#include` statements
- Resolve file paths
- Build dependency graph
- Handle recursion and depth limits

#### `config.py`
Configuration and constants.

**Contains:**
- `DEFAULT_INCLUDE_PATHS`: Default search paths
- `INCLUDE_PATTERN`: Regex for matching includes
- `THIRD_PARTY_LIBS`: Library classification rules
- `SIZE_COLOR_MAP`: Color coding for file sizes

#### `dot_visualizer.py`
Generates Graphviz DOT format output.

**Key Class:**
- `DotVisualizer`: Creates DOT files

**Features:**
- Cluster-based grouping
- Color coding by file size
- Edge weight visualization

#### `html_visualizer.py`
Generates interactive HTML visualization.

**Key Class:**
- `HtmlVisualizer`: Creates HTML files

**Features:**
- Multi-module support
- Interactive D3.js graphs
- Module navigation

#### `html_template.py`
HTML, CSS, and JavaScript templates.

**Contains:**
- HTML structure
- CSS styles
- D3.js visualization code
- Interactive features (zoom, pan, search, etc.)

#### `utils.py`
Utility functions.

**Functions:**
- `get_file_size()`: Get file size
- `format_size()`: Format size for display
- `simplify_path()`: Simplify file paths
- `get_directory_cluster()`: Determine file grouping
- `get_cluster_priority()`: Sort order for clusters

### Documentation (`docs/`)

#### `USER_GUIDE.md` / `USER_GUIDE_zh.md`
Comprehensive user guides in English and Chinese.

**Contents:**
- Installation instructions
- Basic and advanced usage
- Configuration guide
- Interactive HTML controls
- Troubleshooting
- Best practices

#### `API.md`
API documentation for programmatic usage.

**Contents:**
- Installation
- Quick start
- Class and method references
- Code examples
- Error handling
- Performance tips

#### `images/`
Directory for screenshots and diagrams used in documentation.

### Examples (`examples/`)

#### `simple/`
Basic example project demonstrating core functionality.

**Files:**
- `main.cpp`: Main entry point
- `utils.h`: Utility header
- `config.h`: Configuration header
- `README.md`: Example documentation

**Purpose:**
- Demonstrate basic usage
- Test the tool
- Provide a template for users

### Configuration Files

#### `setup.py`
Python package setup script for pip installation.

**Features:**
- Package metadata
- Dependencies
- Entry points for CLI commands
- Installation configuration

#### `requirements.txt`
Python dependencies (currently empty as the tool uses only standard library).

#### `MANIFEST.in`
Specifies which files to include in the package distribution.

#### `.gitignore`
Git ignore rules for:
- Python bytecode
- Build artifacts
- Generated outputs
- IDE files
- OS-specific files

#### `.github/workflows/ci.yml`
GitHub Actions CI/CD pipeline.

**Features:**
- Multi-OS testing (Ubuntu, macOS, Windows)
- Multi-Python version testing (3.6-3.11)
- Linting and formatting checks
- Example analysis tests

### Documentation Files

#### `README.md` / `README_zh.md`
Main project documentation in English and Chinese.

**Contents:**
- Project overview
- Features
- Quick start guide
- Usage examples
- Configuration
- Screenshots

#### `LICENSE`
MIT License file.

#### `CHANGELOG.md`
Version history and change log following Keep a Changelog format.

#### `CONTRIBUTING.md`
Guidelines for contributing to the project.

**Contents:**
- Code of conduct
- Development setup
- Coding standards
- Testing guidelines
- Pull request process

## Design Principles

### 1. Modularity
Each module has a single, well-defined responsibility:
- `analyzer.py`: Analysis logic
- `html_visualizer.py`: HTML generation
- `dot_visualizer.py`: DOT generation
- `config.py`: Configuration
- `utils.py`: Shared utilities

### 2. Separation of Concerns
- Core logic separated from visualization
- Configuration separated from implementation
- CLI separated from library

### 3. Extensibility
Easy to add new features:
- New visualizers (JSON, CSV, etc.)
- New library classifications
- New analysis algorithms

### 4. Reusability
Library can be used:
- As a command-line tool
- As a Python library
- In CI/CD pipelines
- In custom scripts

### 5. Documentation
Comprehensive documentation:
- Code comments and docstrings
- User guides
- API documentation
- Examples

## Dependencies

### Runtime Dependencies
- **Python 3.6+**: Core requirement
- **Standard Library Only**: No external dependencies

### Development Dependencies (Optional)
- `pytest`: Testing framework
- `pytest-cov`: Coverage reporting
- `black`: Code formatting
- `flake8`: Linting
- `mypy`: Type checking

## File Naming Conventions

- **Python files**: `snake_case.py`
- **Documentation**: `UPPERCASE.md` for root-level, `Title_Case.md` for docs/
- **Examples**: Descriptive names matching their purpose

## Code Organization

### Import Order
1. Standard library imports
2. Third-party imports (if any)
3. Local imports

### Class Organization
1. Class docstring
2. Class variables
3. `__init__` method
4. Public methods
5. Private methods (prefixed with `_`)

## Testing Strategy (Future)

```
tests/
├── test_analyzer.py          # Analyzer tests
├── test_visualizers.py       # Visualizer tests
├── test_utils.py             # Utility tests
├── fixtures/                 # Test fixtures
│   ├── sample.cpp
│   └── sample.h
└── README.md                 # Testing documentation
```

## Release Process

1. Update version in `analyze_includes_lib/__init__.py`
2. Update `CHANGELOG.md`
3. Create git tag
4. Build package: `python setup.py sdist bdist_wheel`
5. Upload to PyPI: `twine upload dist/*`

## Maintenance

### Regular Tasks
- Update dependencies
- Review and merge PRs
- Respond to issues
- Update documentation
- Add new examples

### Version Numbering
Follow Semantic Versioning (semver):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

## Future Enhancements

Potential additions to project structure:
- `tests/`: Unit and integration tests
- `benchmarks/`: Performance benchmarks
- `scripts/`: Utility scripts
- `docker/`: Docker configuration
- `.readthedocs.yml`: ReadTheDocs configuration
- `pyproject.toml`: Modern Python project configuration

---

**Last Updated**: 2024-12-01
**Version**: 2.0.0

