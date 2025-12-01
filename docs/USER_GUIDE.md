# User Guide - C++ Dependency Analyzer

## Table of Contents

1. [Installation](#installation)
2. [Basic Usage](#basic-usage)
3. [Advanced Features](#advanced-features)
4. [Configuration](#configuration)
5. [Troubleshooting](#troubleshooting)
6. [Best Practices](#best-practices)

## Installation

### Requirements

- Python 3.6 or higher
- No external dependencies (uses only Python standard library)

### Quick Install

```bash
# Clone the repository
git clone https://github.com/yourusername/cxx_includes_analysis.git
cd cxx_includes_analysis

# Optional: Install as a package
pip install -e .
```

### Verify Installation

```bash
python3 analyze_includes.py --help
```

## Basic Usage

### Analyzing a Single File

The simplest way to use the tool:

```bash
python3 analyze_includes.py src/main.cpp
```

This will:
- Analyze `src/main.cpp` and all its dependencies
- Generate `dependency_graph.html` in the current directory
- Use default include paths and settings

### Analyzing Multiple Files

Analyze several modules at once:

```bash
python3 analyze_includes.py file1.cpp file2.cpp file3.cpp
```

The generated HTML will include navigation buttons to switch between modules.

### Specifying Output File

```bash
python3 analyze_includes.py src/main.cpp -o my_analysis.html
```

### Adding Include Paths

If your project has custom include directories:

```bash
python3 analyze_includes.py src/main.cpp \
    -I ./include \
    -I ./third_party/boost \
    -I /opt/local/include
```

## Advanced Features

### Controlling Recursion Depth

Limit how deep the analyzer follows dependencies:

```bash
# Analyze only 2 levels deep
python3 analyze_includes.py src/main.cpp --depth 2

# Deep analysis (5 levels)
python3 analyze_includes.py src/main.cpp --depth 5
```

**When to use:**
- `--depth 1`: Only direct includes
- `--depth 2-3`: Standard analysis (default: 3)
- `--depth 4-5`: Deep analysis for complex projects
- `--depth 10+`: Complete dependency tree (may be slow)

### Deep System Header Analysis

By default, system headers are not deeply analyzed. Enable deep scanning:

```bash
python3 analyze_includes.py src/main.cpp --deep-system
```

**Warning:** This can significantly increase analysis time and graph complexity.

### Output Formats

#### HTML Format (Interactive)

```bash
python3 analyze_includes.py src/main.cpp --format html
```

Features:
- Interactive D3.js visualization
- Two layout modes (tree and force-directed)
- Search and filter capabilities
- Node highlighting and navigation

#### DOT Format (Graphviz)

```bash
python3 analyze_includes.py src/main.cpp --format dot
```

Generate images from DOT files:

```bash
# PNG image
dot -Tpng dependencies.dot -o graph.png

# SVG image
dot -Tsvg dependencies.dot -o graph.svg

# PDF document
dot -Tpdf dependencies.dot -o graph.pdf
```

#### Both Formats

```bash
python3 analyze_includes.py src/main.cpp --format both
```

### Batch Analysis Examples

#### Analyze All Service Files

```bash
python3 analyze_includes.py src/*_service.cpp -o services.html
```

#### Analyze Specific Modules

```bash
python3 analyze_includes.py \
    ad_server/ad_server.cpp \
    recall_server/recall_server.cpp \
    rank_server/rank_server.cpp \
    -I ./common/include \
    -o backend_services.html
```

#### Using find Command

```bash
# Analyze all .cpp files in src directory
python3 analyze_includes.py $(find src -name "*.cpp") -o project_deps.html

# Analyze only test files
python3 analyze_includes.py $(find tests -name "*_test.cpp") -o tests_deps.html
```

## Configuration

### Default Include Paths

Edit `analyze_includes_lib/config.py` to modify default paths:

```python
DEFAULT_INCLUDE_PATHS = [
    ".",
    "build64_release",
    "/usr/include",
    "/usr/local/include",
    # Add your custom paths here
    "/opt/myproject/include",
]
```

### Adding Third-Party Libraries

To recognize new third-party libraries, edit `THIRD_PARTY_LIBS` in `config.py`:

```python
THIRD_PARTY_LIBS = {
    'boost': 'Boost',
    'absl': 'Abseil',
    'mylib': 'MyCustomLib',  # Add your library
}
```

### Customizing Colors

Modify `SIZE_COLOR_MAP` in `config.py`:

```python
SIZE_COLOR_MAP = [
    (10 * 1024, "#E8F5E9"),   # < 10KB: light green
    (50 * 1024, "#FFF9C4"),   # < 50KB: light yellow
    (200 * 1024, "#FFE0B2"),  # < 200KB: light orange
    (float('inf'), "#FFCDD2"), # >= 200KB: light red
]
```

## Interactive HTML Guide

### Navigation

**Module Switching:**
- Click "Previous" / "Next" buttons
- Use keyboard: `←` (previous) / `→` (next)

**Canvas Movement:**
- Drag blank area to pan
- Mouse wheel to zoom in/out
- Double-click blank area to reset view

### Node Interaction

**Click a Node:**
- Red edges: Files this node depends on
- Green edges: Files that depend on this node
- Other nodes/edges are dimmed

**Drag a Node:**
- Adjust position manually
- Works in both tree and force layouts

**Double-Click a Node:**
- Reset to default position (force layout only)

### Search and Filter

Type in the search box to filter:
- Matches file names (case-insensitive)
- Highlights matching nodes
- Shows only relevant edges

Clear search to restore full graph.

### Layout Modes

**Tree Layout:**
- Hierarchical left-to-right arrangement
- Grouped by directory/library type
- Best for understanding dependency levels
- Order within each level:
  1. Project files
  2. Third-party libraries
  3. Generated files (Protobuf)
  4. System libraries

**Force-Directed Layout:**
- Physics-based dynamic layout
- Nodes repel each other
- Edges act as springs
- Best for exploring complex relationships

## Troubleshooting

### Problem: Missing Dependencies

**Symptoms:** Some expected files don't appear in the graph.

**Solutions:**
1. Add missing include paths with `-I`
2. Increase recursion depth with `--depth`
3. Check if files are conditionally included (`#ifdef`)
4. Verify file paths are correct

### Problem: Graph Too Large

**Symptoms:** HTML file is huge, browser is slow.

**Solutions:**
1. Reduce depth: `--depth 2`
2. Analyze fewer files at once
3. Don't use `--deep-system` unless necessary
4. Use search to focus on specific files

### Problem: File Not Found

**Symptoms:** "Warning: File xxx not found"

**Solutions:**
1. Check file path is correct
2. Use absolute paths if relative paths fail
3. Ensure file exists and is readable

### Problem: System Headers Not Showing

**Symptoms:** System includes like `<iostream>` don't appear.

**Solutions:**
1. This is normal - system headers are shown but not deeply analyzed
2. Use `--deep-system` to analyze system headers in detail
3. Check if system include paths are in `DEFAULT_INCLUDE_PATHS`

## Best Practices

### For Small Projects (< 50 files)

```bash
python3 analyze_includes.py src/*.cpp --depth 5 -o project.html
```

### For Medium Projects (50-200 files)

```bash
# Analyze by module
python3 analyze_includes.py module1/*.cpp -o module1.html
python3 analyze_includes.py module2/*.cpp -o module2.html

# Or analyze key files only
python3 analyze_includes.py src/main.cpp src/server.cpp --depth 3
```

### For Large Projects (> 200 files)

```bash
# Analyze specific subsystems
python3 analyze_includes.py backend/*.cpp --depth 2 -o backend.html

# Use shallow depth
python3 analyze_includes.py src/*.cpp --depth 2

# Focus on entry points
python3 analyze_includes.py src/main.cpp src/server_main.cpp --depth 3
```

### CI/CD Integration

```bash
# Generate dependency report in CI
python3 analyze_includes.py src/main.cpp -o deps.html --depth 3

# Archive as build artifact
# (depends on your CI system)
```

### Regular Dependency Audits

```bash
# Weekly dependency analysis
python3 analyze_includes.py $(find src -name "*.cpp") \
    -o weekly_deps_$(date +%Y%m%d).html
```

## Tips and Tricks

1. **Start Shallow:** Begin with `--depth 2`, increase if needed
2. **Use Search:** In large graphs, search is your friend
3. **Batch Wisely:** Group related files for batch analysis
4. **Save Configurations:** Create shell scripts for common analyses
5. **Compare Over Time:** Generate periodic reports to track changes
6. **Focus on Entry Points:** Analyze main files and key modules
7. **Exclude Build Artifacts:** Don't analyze generated files directly

## Next Steps

- Check out [API Documentation](API.md) for library usage
- See [Examples](../examples/) for more use cases
- Read [CONTRIBUTING.md](../CONTRIBUTING.md) to contribute

