# Simple Example

This is a basic example demonstrating dependency analysis for a simple C++ project.

## Files

- `main.cpp` - Main entry point
- `utils.h` - Utility functions
- `config.h` - Configuration management

## Dependency Structure

```
main.cpp
  ├── iostream (system)
  ├── vector (system)
  ├── string (system)
  ├── utils.h
  │   ├── string (system)
  │   └── iostream (system)
  └── config.h
      ├── string (system)
      ├── map (system)
      ├── fstream (system)
      └── utils.h
```

## Running the Analysis

```bash
# From the simple directory
python3 ../../analyze_includes.py main.cpp

# Or from the project root
python3 analyze_includes.py examples/simple/main.cpp -I examples/simple
```

## Expected Output

The analyzer will:
1. Find 3 project files (main.cpp, utils.h, config.h)
2. Identify several system headers (iostream, vector, string, map, fstream)
3. Show the dependency relationships in an interactive HTML graph

### Visualization

The generated HTML will look like this:

![Simple Example Output](../../docs/images/example-simple-dependency-graph.png)

**What you see:**
- **Green nodes**: Small files (project headers)
- **Yellow nodes**: Medium-sized files
- **Arrows**: Dependency relationships (A → B means A includes B)
- **Grouped layout**: System libraries on the right, project files on the left
- **Interactive**: Click nodes to highlight their dependencies!

