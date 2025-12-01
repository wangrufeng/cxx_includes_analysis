# API Documentation

This document describes the API for using the C++ Dependency Analyzer as a Python library.

## Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Core Classes](#core-classes)
4. [Configuration](#configuration)
5. [Utilities](#utilities)
6. [Examples](#examples)

## Installation

```bash
pip install -e .
```

Or use directly without installation:

```python
import sys
sys.path.insert(0, '/path/to/cxx_includes_analysis')
```

## Quick Start

```python
from analyze_includes_lib import (
    DEFAULT_INCLUDE_PATHS,
    DependencyAnalyzer,
    HtmlVisualizer
)

# Create analyzer
analyzer = DependencyAnalyzer(
    include_paths=DEFAULT_INCLUDE_PATHS,
    max_depth=3,
    deep_system=False
)

# Analyze a file
nodes, edges = analyzer.analyze("src/main.cpp")

# Generate HTML
modules_data = [{
    'source_file': "src/main.cpp",
    'nodes': nodes,
    'edges': edges
}]

visualizer = HtmlVisualizer(modules_data)
visualizer.generate("output.html")
```

## Core Classes

### DependencyAnalyzer

Analyzes C++ file dependencies.

#### Constructor

```python
DependencyAnalyzer(include_paths, max_depth=3, deep_system=False)
```

**Parameters:**
- `include_paths` (list): List of directories to search for include files
- `max_depth` (int): Maximum recursion depth (default: 3)
- `deep_system` (bool): Whether to deeply analyze system headers (default: False)

#### Methods

##### analyze(start_file)

Analyzes dependencies starting from a source file.

```python
nodes, edges = analyzer.analyze("src/main.cpp")
```

**Parameters:**
- `start_file` (str): Path to the C++ source file

**Returns:**
- `nodes` (dict): Dictionary of nodes, keyed by file path
  ```python
  {
    'path/to/file.h': {
      'label': 'file.h',
      'size': 1024,
      'cluster': 'Project/path/to',
      'full_path': '/abs/path/to/file.h'
    },
    ...
  }
  ```
- `edges` (list): List of dependency edges
  ```python
  [
    {
      'from': 'src/main.cpp',
      'to': 'include/utils.h',
      'weight': 1024
    },
    ...
  ]
  ```

##### find_file(filename, is_system, current_dir)

Finds a header file in the include paths.

```python
full_path = analyzer.find_file("utils.h", False, "/path/to/current")
```

**Parameters:**
- `filename` (str): Name of the file to find
- `is_system` (bool): Whether this is a system include (angle brackets)
- `current_dir` (str): Directory of the file doing the including

**Returns:**
- `str`: Full path to the file, or None if not found

### HtmlVisualizer

Generates interactive HTML visualization.

#### Constructor

```python
HtmlVisualizer(modules_data)
```

**Parameters:**
- `modules_data` (list): List of module dictionaries
  ```python
  [
    {
      'source_file': 'src/main.cpp',
      'nodes': {...},
      'edges': [...]
    },
    ...
  ]
  ```

#### Methods

##### generate(output_file)

Generates the HTML file.

```python
visualizer.generate("dependency_graph.html")
```

**Parameters:**
- `output_file` (str): Path to the output HTML file

### DotVisualizer

Generates Graphviz DOT format.

#### Constructor

```python
DotVisualizer(nodes, edges, source_file)
```

**Parameters:**
- `nodes` (dict): Dictionary of nodes from analyzer
- `edges` (list): List of edges from analyzer
- `source_file` (str): Name of the source file being analyzed

#### Methods

##### generate(output_file)

Generates the DOT file.

```python
visualizer.generate("dependencies.dot")
```

**Parameters:**
- `output_file` (str): Path to the output DOT file

## Configuration

### DEFAULT_INCLUDE_PATHS

Default list of include search paths.

```python
from analyze_includes_lib import DEFAULT_INCLUDE_PATHS

# Use as-is
analyzer = DependencyAnalyzer(include_paths=DEFAULT_INCLUDE_PATHS)

# Extend with custom paths
custom_paths = DEFAULT_INCLUDE_PATHS + ['/opt/mylib/include']
analyzer = DependencyAnalyzer(include_paths=custom_paths)
```

### INCLUDE_PATTERN

Regular expression for matching `#include` statements.

```python
from analyze_includes_lib import INCLUDE_PATTERN
import re

match = INCLUDE_PATTERN.match('#include <iostream>')
if match:
    is_system = match.group(1) == '<'
    filename = match.group(2)
```

### THIRD_PARTY_LIBS

Dictionary of recognized third-party libraries.

```python
from analyze_includes_lib.config import THIRD_PARTY_LIBS

# Check if a library is recognized
if 'boost' in THIRD_PARTY_LIBS:
    print(f"Boost is recognized as: {THIRD_PARTY_LIBS['boost']}")
```

## Utilities

### get_file_size(path)

Gets the size of a file in bytes.

```python
from analyze_includes_lib import get_file_size

size = get_file_size("src/main.cpp")
print(f"File size: {size} bytes")
```

### format_size(size)

Formats a file size in human-readable format.

```python
from analyze_includes_lib import format_size

print(format_size(1024))        # "1.0 KB"
print(format_size(1048576))     # "1.0 MB"
print(format_size(1073741824))  # "1.0 GB"
```

### simplify_path(path)

Simplifies a file path by removing common prefixes.

```python
from analyze_includes_lib import simplify_path

simplified = simplify_path("/usr/include/c++/8/iostream")
print(simplified)  # "iostream"
```

### get_directory_cluster(path)

Gets the cluster name for a file (for grouping in visualization).

```python
from analyze_includes_lib.utils import get_directory_cluster

cluster = get_directory_cluster("src/utils/helper.h")
print(cluster)  # "Project/src/utils"

cluster = get_directory_cluster("/usr/include/iostream")
print(cluster)  # "System/C++ Standard Library"
```

### get_cluster_priority(cluster_name)

Gets the sort priority for a cluster (lower = higher priority).

```python
from analyze_includes_lib.utils import get_cluster_priority

priority = get_cluster_priority("Project/src")
print(priority)  # 0 (highest priority)

priority = get_cluster_priority("System/C++ Standard Library")
print(priority)  # 3 (lowest priority)
```

## Examples

### Example 1: Analyze Multiple Files

```python
from analyze_includes_lib import DependencyAnalyzer, HtmlVisualizer, DEFAULT_INCLUDE_PATHS

source_files = ["file1.cpp", "file2.cpp", "file3.cpp"]
analyzer = DependencyAnalyzer(DEFAULT_INCLUDE_PATHS, max_depth=3)

modules_data = []
for source_file in source_files:
    nodes, edges = analyzer.analyze(source_file)
    modules_data.append({
        'source_file': source_file,
        'nodes': nodes,
        'edges': edges
    })

visualizer = HtmlVisualizer(modules_data)
visualizer.generate("multi_module.html")
```

### Example 2: Custom Include Paths

```python
from analyze_includes_lib import DependencyAnalyzer, DEFAULT_INCLUDE_PATHS

custom_paths = DEFAULT_INCLUDE_PATHS + [
    "./include",
    "./third_party/boost",
    "/opt/local/include"
]

analyzer = DependencyAnalyzer(custom_paths, max_depth=5, deep_system=True)
nodes, edges = analyzer.analyze("src/main.cpp")
```

### Example 3: Generate Both HTML and DOT

```python
from analyze_includes_lib import (
    DependencyAnalyzer,
    HtmlVisualizer,
    DotVisualizer,
    DEFAULT_INCLUDE_PATHS
)

# Analyze
analyzer = DependencyAnalyzer(DEFAULT_INCLUDE_PATHS)
nodes, edges = analyzer.analyze("src/main.cpp")

# Generate HTML
html_viz = HtmlVisualizer([{
    'source_file': 'src/main.cpp',
    'nodes': nodes,
    'edges': edges
}])
html_viz.generate("output.html")

# Generate DOT
dot_viz = DotVisualizer(nodes, edges, "src/main.cpp")
dot_viz.generate("output.dot")
```

### Example 4: Filter Results

```python
from analyze_includes_lib import DependencyAnalyzer, DEFAULT_INCLUDE_PATHS

analyzer = DependencyAnalyzer(DEFAULT_INCLUDE_PATHS)
nodes, edges = analyzer.analyze("src/main.cpp")

# Filter to only project files
project_nodes = {
    path: info for path, info in nodes.items()
    if info['cluster'].startswith('Project/')
}

# Filter edges to only those between project files
project_edges = [
    edge for edge in edges
    if edge['from'] in project_nodes and edge['to'] in project_nodes
]

print(f"Found {len(project_nodes)} project files")
print(f"Found {len(project_edges)} internal dependencies")
```

### Example 5: Dependency Statistics

```python
from analyze_includes_lib import DependencyAnalyzer, DEFAULT_INCLUDE_PATHS
from collections import Counter

analyzer = DependencyAnalyzer(DEFAULT_INCLUDE_PATHS)
nodes, edges = analyzer.analyze("src/main.cpp")

# Count dependencies per file
dep_count = Counter(edge['from'] for edge in edges)

print("Files with most dependencies:")
for file, count in dep_count.most_common(10):
    print(f"  {file}: {count} dependencies")

# Count by cluster
cluster_count = Counter(nodes[path]['cluster'] for path in nodes)

print("\nFiles by cluster:")
for cluster, count in cluster_count.most_common():
    print(f"  {cluster}: {count} files")
```

## Error Handling

```python
from analyze_includes_lib import DependencyAnalyzer, DEFAULT_INCLUDE_PATHS
import os

analyzer = DependencyAnalyzer(DEFAULT_INCLUDE_PATHS)

source_file = "src/main.cpp"

# Check if file exists
if not os.path.exists(source_file):
    print(f"Error: {source_file} not found")
    exit(1)

try:
    nodes, edges = analyzer.analyze(source_file)
    print(f"Analysis successful: {len(nodes)} nodes, {len(edges)} edges")
except Exception as e:
    print(f"Error during analysis: {e}")
    exit(1)
```

## Thread Safety

The analyzer is **not thread-safe**. If you need to analyze multiple files in parallel, create a separate analyzer instance for each thread:

```python
from concurrent.futures import ThreadPoolExecutor
from analyze_includes_lib import DependencyAnalyzer, DEFAULT_INCLUDE_PATHS

def analyze_file(source_file):
    # Create a new analyzer for each thread
    analyzer = DependencyAnalyzer(DEFAULT_INCLUDE_PATHS)
    return analyzer.analyze(source_file)

source_files = ["file1.cpp", "file2.cpp", "file3.cpp"]

with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(analyze_file, source_files))
```

## Performance Tips

1. **Limit Depth**: Use smaller `max_depth` values for faster analysis
2. **Avoid Deep System**: Don't use `deep_system=True` unless necessary
3. **Cache Results**: Store analysis results to avoid re-analyzing
4. **Filter Early**: Remove unwanted files before visualization
5. **Batch Wisely**: Analyze related files together for better context

## See Also

- [User Guide](USER_GUIDE.md) - Detailed usage instructions
- [Examples](../examples/) - Example code and projects
- [Source Code](../analyze_includes_lib/) - Library source code

