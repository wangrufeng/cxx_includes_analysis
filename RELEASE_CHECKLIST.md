# Release Checklist / 发布检查清单

## Pre-Release Checklist / 发布前检查

### ✅ Documentation / 文档
- [x] README.md (English) - Complete and up-to-date
- [x] README_zh.md (Chinese) - Complete and up-to-date
- [x] CHANGELOG.md - Version history documented
- [x] CONTRIBUTING.md - Contribution guidelines
- [x] LICENSE - MIT License included
- [x] USER_GUIDE.md - Detailed user guide (English)
- [x] USER_GUIDE_zh.md - Detailed user guide (Chinese)
- [x] API.md - API documentation
- [x] QUICK_START.md - Quick start guide
- [x] PROJECT_STRUCTURE.md - Project structure documentation

### ✅ Code Quality / 代码质量
- [x] Code is modular and well-organized
- [x] All functions have docstrings
- [x] Code follows PEP 8 style guide
- [x] No obvious bugs or issues
- [ ] Unit tests written (TODO)
- [ ] All tests passing (TODO)

### ✅ Configuration Files / 配置文件
- [x] setup.py - Package configuration
- [x] requirements.txt - Dependencies listed
- [x] MANIFEST.in - Package manifest
- [x] .gitignore - Ignore rules configured
- [x] .github/workflows/ci.yml - CI/CD pipeline

### ✅ Examples / 示例
- [x] examples/simple/ - Basic example included
- [x] Example README files
- [x] Example can be run successfully

### ✅ GitHub Templates / GitHub 模板
- [x] .github/ISSUE_TEMPLATE/bug_report.md
- [x] .github/ISSUE_TEMPLATE/feature_request.md
- [x] .github/PULL_REQUEST_TEMPLATE.md

### 📸 Visual Assets / 视觉资源
- [ ] docs/images/tree_layout.png - Tree layout screenshot (TODO)
- [ ] docs/images/force_layout.png - Force layout screenshot (TODO)
- [ ] docs/images/multiple_modules.png - Multiple modules screenshot (TODO)

### 🔧 Final Touches / 最后润色
- [ ] Update GitHub repository URL in all files
- [ ] Update author information in setup.py
- [ ] Test installation with `pip install -e .`
- [ ] Test all examples
- [ ] Run linting: `flake8 analyze_includes_lib/`
- [ ] Run formatting: `black analyze_includes_lib/`

## Release Steps / 发布步骤

### 1. Prepare Repository / 准备仓库

```bash
# Ensure all changes are committed
git status

# Update version if needed
# Edit: analyze_includes_lib/__init__.py
# __version__ = "2.0.0"

# Commit final changes
git add .
git commit -m "chore: prepare for v2.0.0 release"
```

### 2. Create GitHub Repository / 创建 GitHub 仓库

1. Go to https://github.com/new
2. Repository name: `cxx_includes_analysis`
3. Description: "A tool for analyzing and visualizing C++ module dependencies"
4. Public repository
5. Do NOT initialize with README (we already have one)

### 3. Push to GitHub / 推送到 GitHub

```bash
# Add remote
git remote add origin https://github.com/yourusername/cxx_includes_analysis.git

# Push
git branch -M main
git push -u origin main

# Create and push tags
git tag -a v2.0.0 -m "Release version 2.0.0"
git push origin v2.0.0
```

### 4. Create GitHub Release / 创建 GitHub Release

1. Go to repository → Releases → Create a new release
2. Choose tag: v2.0.0
3. Release title: "C++ Dependency Analyzer v2.0.0"
4. Description: Copy from CHANGELOG.md
5. Attach any additional files if needed
6. Publish release

### 5. Update Repository Settings / 更新仓库设置

#### Topics / 主题标签
Add these topics to your repository:
- `cpp`
- `c-plus-plus`
- `dependency-analysis`
- `visualization`
- `static-analysis`
- `include-analysis`
- `dependency-graph`
- `d3js`
- `graphviz`

#### About Section / 关于部分
- Description: "A tool for analyzing and visualizing C++ module dependencies"
- Website: (if you have one)
- Topics: (as listed above)

#### Features / 功能
Enable:
- [x] Issues
- [x] Discussions (optional)
- [x] Projects (optional)
- [x] Wiki (optional)

### 6. Optional: Publish to PyPI / 可选：发布到 PyPI

```bash
# Install build tools
pip install build twine

# Build package
python -m build

# Check package
twine check dist/*

# Upload to TestPyPI first (recommended)
twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ cxx-dependency-analyzer

# If everything works, upload to PyPI
twine upload dist/*
```

### 7. Announce / 宣布发布

Consider announcing on:
- [ ] GitHub Discussions
- [ ] Reddit (r/cpp, r/programming)
- [ ] Twitter/X
- [ ] LinkedIn
- [ ] Your blog or website
- [ ] Relevant forums or communities

## Post-Release / 发布后

### Immediate / 立即
- [ ] Verify GitHub release is visible
- [ ] Test cloning and running from GitHub
- [ ] Check that all links in README work
- [ ] Monitor for initial issues

### Short-term (1 week) / 短期（1周）
- [ ] Respond to issues and questions
- [ ] Fix any critical bugs
- [ ] Update documentation based on feedback
- [ ] Thank contributors and users

### Medium-term (1 month) / 中期（1月）
- [ ] Gather feature requests
- [ ] Plan next version
- [ ] Add more examples
- [ ] Improve documentation

## Version Numbering / 版本号规则

Follow Semantic Versioning (semver.org):

- **MAJOR** (x.0.0): Breaking changes
  - Incompatible API changes
  - Major feature additions that change behavior

- **MINOR** (2.x.0): New features
  - New functionality (backward compatible)
  - Significant improvements

- **PATCH** (2.0.x): Bug fixes
  - Bug fixes (backward compatible)
  - Minor improvements
  - Documentation updates

## Rollback Plan / 回滚计划

If critical issues are found after release:

1. **Immediate**: Add warning to README
2. **Quick fix**: Release patch version (2.0.1)
3. **Major issue**: 
   - Yank release from PyPI (if published)
   - Add notice to GitHub release
   - Release fixed version ASAP

## Success Metrics / 成功指标

Track these metrics after release:

- [ ] GitHub stars
- [ ] Issues opened/closed
- [ ] Pull requests
- [ ] Downloads (if on PyPI)
- [ ] User feedback
- [ ] Community engagement

## Notes / 注意事项

### Before Publishing / 发布前注意
1. Double-check all URLs point to correct repository
2. Ensure author email is correct
3. Verify license is appropriate
4. Test on different platforms if possible
5. Have someone else review if possible

### Security / 安全
- Don't commit sensitive information
- Don't include API keys or passwords
- Review .gitignore carefully
- Check for hardcoded paths

### Legal / 法律
- Ensure you have rights to all code
- Verify third-party code licenses
- Include proper attributions
- Check trademark issues

---

## Current Status / 当前状态

**Version**: 2.0.0
**Status**: ✅ Ready for release (pending screenshots and final testing)
**Date**: 2024-12-01

### Completed / 已完成
- ✅ All documentation
- ✅ Code organization
- ✅ Examples
- ✅ Configuration files
- ✅ GitHub templates
- ✅ CI/CD setup

### Pending / 待完成
- ⏳ Add screenshots to docs/images/
- ⏳ Update GitHub URLs in all files
- ⏳ Final testing
- ⏳ Create GitHub repository
- ⏳ First release

---

**Good luck with your release! / 祝发布顺利！** 🚀

