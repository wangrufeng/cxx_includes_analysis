# C++ Dependency Analyzer

[中文文档](README_zh.md) | English

A powerful tool for analyzing and visualizing C++ module dependencies with interactive HTML graphs.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)

## ✨ Features

### 📊 Batch Analysis
- Analyze multiple C++ source files simultaneously
- Switch between modules using Previous/Next buttons or arrow keys
- Navigate through complex projects with ease

### 🎯 Smart Library Classification
- **System Libraries**: C/C++ standard library and Linux system headers
  - `System/C++ Standard Library`: C++ standard library
  - `System/Linux Headers`: Linux system headers
  - `System/Other`: Other system libraries

- **Third-Party Libraries**: Common third-party dependencies
  - `Third-Party/Boost`: Boost library
  - `Third-Party/Abseil`: Abseil library
  - `Third-Party/bRPC`: bRPC framework
  - `Third-Party/gflags`: gflags command-line flags
  - `Third-Party/glog`: glog logging library
  - `Third-Party/Protobuf`: Protocol Buffers
  - And more...

- **Project Files**: Your project source files
  - `Project/xxx`: Grouped by directory structure
  - `Generated/Proto Files`: Generated Protobuf files

### 🎨 Interactive Visualization
- **Two Layout Modes**:
  - Tree Layout: Hierarchical dependency view from left to right
  - Force-Directed Layout: Dynamic physics-based layout

- **Interactive Features**:
  - Click nodes to highlight dependencies (red=depends on, green=depended by)
  - Drag nodes to adjust positions
  - Search box to filter files
  - Mouse wheel zoom and drag to pan
  - Keyboard shortcuts for quick navigation

- **Visual Indicators**:
  - Node colors indicate file size (green=small, yellow=medium, orange=large, red=huge)
  - Edge thickness shows dependency importance

## 🚀 Quick Start

> 📖 **New to this tool?** Check out the [Quick Start Guide](QUICK_START.md) for a 5-minute tutorial with common use cases!

### Installation

```bash
git clone https://github.com/yourusername/cxx_includes_analysis.git
cd cxx_includes_analysis
```

No dependencies needed - uses only Python 3.6+ standard library!

### Try the Example

```bash
# Analyze the included example
python3 analyze_includes.py examples/simple/main.cpp -I examples/simple

# Open the generated HTML
open dependency_graph.html  # macOS
# or: xdg-open dependency_graph.html  # Linux
# or: start dependency_graph.html     # Windows
```

### Analyze Your Code

```bash
# Single file
python3 analyze_includes.py src/main.cpp

# Multiple files with custom paths
python3 analyze_includes.py src/*.cpp -I ./include -o project_deps.html
```

**📚 For more examples and detailed usage, see:**
- [Quick Start Guide](QUICK_START.md) - 5-minute tutorial
- [User Guide](docs/USER_GUIDE.md) - Complete documentation
- [Examples](examples/) - Sample projects

## 📖 Documentation

- **[Quick Start Guide](QUICK_START.md)** - 5-minute tutorial with common scenarios
- **[User Guide](docs/USER_GUIDE.md)** - Complete usage instructions and best practices
- **[API Documentation](docs/API.md)** - Library API reference for programmatic usage
- **[Examples](examples/)** - Sample projects and use cases
- **[Contributing Guide](CONTRIBUTING.md)** - How to contribute to this project

## 📋 Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `source_files` | C++ source files to analyze (supports multiple) | Required |
| `-I, --include` | Add include search path (can be used multiple times) | Predefined paths |
| `--depth` | Maximum recursion depth | 3 |
| `--deep-system` | Deep scan system headers | False |
| `--format` | Output format: html/dot/both | html |
| `-o, --output` | Output file name | dependency_graph.html |

> 💡 **Tip**: For detailed usage examples, see the [Quick Start Guide](QUICK_START.md) or [User Guide](docs/USER_GUIDE.md)

## 🎮 Interactive HTML Features

The generated HTML provides an interactive visualization with:

- **🔄 Module Navigation**: Switch between modules using Previous/Next buttons or ← → keys
- **🎯 Click to Explore**: Click nodes to highlight dependencies (red=depends on, green=depended by)
- **🔍 Search & Filter**: Find files quickly with the search box
- **📐 Two Layouts**: Toggle between tree layout and force-directed layout
- **🖱️ Zoom & Pan**: Mouse wheel to zoom, drag to move around
- **✋ Drag Nodes**: Adjust positions manually

> 📖 For detailed controls and tips, see the [User Guide](docs/USER_GUIDE.md#interactive-html-guide)

## 🔧 Configuration

Customize the tool by editing `analyze_includes_lib/config.py`:

- **Include Paths**: Add your project's include directories
- **Third-Party Libraries**: Define custom library classifications
- **Visual Settings**: Adjust colors and size thresholds

> 📖 See [User Guide - Configuration](docs/USER_GUIDE.md#configuration) for details

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [D3.js](https://d3js.org/) - For interactive visualizations
- [Graphviz](https://graphviz.org/) - For DOT format support

## 📮 Contact

If you have any questions or suggestions, please open an issue on GitHub.

## 🗺️ Roadmap

- [ ] Support for CMake project analysis
- [ ] Export to other formats (JSON, CSV)
- [ ] Circular dependency detection
- [ ] Dependency statistics and reports
- [ ] Integration with CI/CD pipelines

## 📊 Screenshots

### Example Output
Here's what the dependency graph looks like for the included example project:

![Example Dependency Graph](docs/images/example-simple-dependency-graph.png)

*Interactive visualization showing dependencies between main.cpp, utils.h, config.h and system headers*

### Features in Action
- 🎯 **Node Colors**: File size visualization (green=small, yellow=medium)
- 🔗 **Edge Connections**: Clear dependency relationships
- 📁 **Smart Grouping**: System libraries, project files organized
- 🎨 **Interactive**: Click, drag, zoom, and explore!

---

**Star ⭐ this repository if you find it helpful!**
