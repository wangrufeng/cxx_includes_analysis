# GitHub Actions Workflows

## CI Workflow

### What it does

The CI workflow automatically tests the project on every push and pull request to ensure:
- ✅ Code runs on multiple operating systems (Ubuntu, macOS, Windows)
- ✅ Compatible with multiple Python versions (3.8-3.12)
- ✅ Help commands work correctly
- ✅ Example analysis runs successfully
- ✅ Code quality meets standards

### Jobs

#### 1. Test Job
- **Runs on**: Ubuntu, macOS, Windows
- **Python versions**: 3.8, 3.9, 3.10, 3.11, 3.12
- **Tests**:
  - Display Python version
  - Run help commands
  - Analyze example project
  - Verify output file is generated

#### 2. Lint Job
- **Runs on**: Ubuntu only
- **Python version**: 3.11
- **Checks**:
  - Python syntax errors (blocking)
  - Code style issues (non-blocking)

### Optimization

To speed up CI, we:
- Exclude some OS/Python combinations (e.g., macOS + Python 3.8)
- Use `fail-fast: false` to see all failures
- Run lint only on Ubuntu (style is OS-independent)
- Use latest action versions (v4, v5)

### Local Testing

Before pushing, test locally:

```bash
# Test help commands
python analyze_includes.py --help
python analyze_i_file.py

# Test with example
python analyze_includes.py examples/simple/main.cpp -I examples/simple

# Check code quality
pip install flake8
flake8 analyze_includes_lib/ --max-line-length=100
```

### Troubleshooting

If CI fails:

1. **Syntax errors**: Fix immediately (blocking)
2. **Style issues**: Fix when convenient (non-blocking)
3. **Test failures**: Check if example files are correct
4. **OS-specific issues**: Test on that OS locally if possible

### Future Enhancements

Potential additions:
- [ ] Add unit tests with pytest
- [ ] Add coverage reporting
- [ ] Add automatic release workflow
- [ ] Add dependency security scanning
- [ ] Add performance benchmarks

---

**Last Updated**: 2024-12-01

