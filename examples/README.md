# Examples

This directory contains example C++ files and usage scenarios for the C++ Dependency Analyzer.

## Example Files

### 1. Simple Example (`simple/`)
A basic C++ project with a few files to demonstrate basic dependency analysis.

```bash
cd simple
python3 ../../analyze_includes.py main.cpp -o simple_deps.html
```

### 2. Multi-Module Example (`multi_module/`)
Multiple service modules to demonstrate batch analysis.

```bash
cd multi_module
python3 ../../analyze_includes.py service1.cpp service2.cpp service3.cpp -o multi_deps.html
```

### 3. Third-Party Libraries Example (`third_party/`)
Example showing how the tool handles third-party library dependencies.

```bash
cd third_party
python3 ../../analyze_includes.py app.cpp -I ./include -o third_party_deps.html
```

## Creating Your Own Examples

1. Create a new directory for your example
2. Add your C++ source files
3. Run the analyzer with appropriate options
4. Document your example in this README

## Tips

- Use `-I` to add custom include paths
- Use `--depth` to control recursion depth
- Use `--deep-system` to analyze system headers in detail
- Use `--format both` to generate both HTML and DOT outputs

