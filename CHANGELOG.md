# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- CMake project analysis support
- Circular dependency detection
- Export to JSON/CSV formats
- Dependency statistics and reports
- CI/CD pipeline integration
- Unit tests and test coverage
- Performance optimizations

## [2.0.0] - 2024-12-01

### Added
- **Batch Analysis**: Support for analyzing multiple C++ source files simultaneously
- **Module Navigation**: Previous/Next buttons and keyboard shortcuts (←/→) to switch between modules
- **Enhanced Library Classification**: Improved recognition and categorization of third-party libraries
- **System Library Categorization**: Separate categories for C++ standard library and Linux system headers
- **Modular Architecture**: Refactored codebase into separate modules for better maintainability
  - `config.py`: Configuration management
  - `analyzer.py`: Core dependency analysis
  - `dot_visualizer.py`: DOT format generation
  - `html_visualizer.py`: HTML visualization
  - `html_template.py`: HTML templates
  - `utils.py`: Utility functions
- **Comprehensive Documentation**: 
  - Dual-language README (English and Chinese)
  - User Guide with detailed instructions
  - API documentation for library usage
  - Example projects and use cases
- **Project Structure**: Organized examples and documentation directories
- **Package Support**: Added `setup.py` for pip installation
- **Development Tools**: Added `requirements.txt` and `.gitignore`

### Changed
- Improved tree layout algorithm with better node grouping
- Enhanced visual hierarchy in dependency graphs
- Better handling of large projects with many dependencies
- Optimized file path simplification logic

### Fixed
- Fixed style conflicts with heavyweight dependency indicators
- Corrected edge weight calculations
- Improved system header detection accuracy
- Fixed path handling on different operating systems

### Documentation
- Added comprehensive README in English and Chinese
- Created detailed User Guide
- Added API documentation for programmatic usage
- Included example projects with explanations
- Added CONTRIBUTING.md for contributors
- Created this CHANGELOG.md

## [1.0.0] - 2024-01-01

### Added
- Initial release
- Basic dependency analysis for C++ files
- Interactive D3.js visualization
- Two layout modes: tree layout and force-directed layout
- DOT format output for Graphviz
- Node color coding by file size
- Edge thickness by dependency weight
- Search and filter functionality
- Click-to-highlight dependencies
- Drag-and-drop node positioning
- Zoom and pan controls
- Configurable include paths
- Recursion depth control
- System header scanning options

### Features
- Command-line interface
- Single file analysis
- HTML output with interactive visualization
- DOT output for static graph generation
- Automatic library classification (basic)
- File size visualization
- Dependency relationship highlighting

## Version History Summary

- **v2.0.0**: Major refactoring, batch analysis, modular architecture, comprehensive documentation
- **v1.0.0**: Initial release with core functionality

## Migration Guide

### From v1.0 to v2.0

The v2.0 API is backward compatible with v1.0 for basic usage. However, if you were using the tool programmatically, note these changes:

**Old way (v1.0):**
```python
# Everything was in a single file
from analyze_includes import DependencyAnalyzer
```

**New way (v2.0):**
```python
# Now modular
from analyze_includes_lib import DependencyAnalyzer
```

**Command-line usage remains the same:**
```bash
# Works in both v1.0 and v2.0
python3 analyze_includes.py src/main.cpp
```

**New features in v2.0:**
```bash
# Batch analysis (new in v2.0)
python3 analyze_includes.py file1.cpp file2.cpp file3.cpp
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute to this project.

## Links

- [GitHub Repository](https://github.com/yourusername/cxx_includes_analysis)
- [Issue Tracker](https://github.com/yourusername/cxx_includes_analysis/issues)
- [Documentation](docs/)

---

**Note**: This project follows [Semantic Versioning](https://semver.org/):
- **MAJOR** version for incompatible API changes
- **MINOR** version for new functionality in a backward compatible manner
- **PATCH** version for backward compatible bug fixes

