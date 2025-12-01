# Screenshots and Images

This directory contains screenshots and images used in the documentation.

## Current Images

### example-simple-dependency-graph.png
Dependency graph generated from the `examples/simple/` project, showing:
- main.cpp dependencies
- utils.h and config.h relationships
- System header includes
- Interactive visualization features

**Used in:**
- README.md (main screenshot)
- README_zh.md (main screenshot)
- QUICK_START.md (tutorial example)
- examples/simple/README.md (expected output)

## Image Guidelines

### Naming Convention
Use descriptive names that indicate the content:
- `example-{name}-{feature}.png` - For example outputs
- `feature-{name}.png` - For specific features
- `layout-{type}.png` - For different layout modes

### Examples:
- ✅ `example-simple-dependency-graph.png`
- ✅ `feature-tree-layout.png`
- ✅ `feature-force-directed-layout.png`
- ✅ `feature-multi-module-navigation.png`
- ❌ `screenshot-20251201-205239.png` (not descriptive)
- ❌ `image1.png` (not descriptive)

### Image Requirements
- **Format**: PNG (preferred) or JPEG
- **Size**: Keep under 500KB when possible
- **Resolution**: High enough to be readable, but optimized for web
- **Content**: Should clearly show the feature or output being documented

## Planned Images

Future screenshots to add:
- [ ] `layout-tree-view.png` - Tree layout example
- [ ] `layout-force-directed.png` - Force-directed layout example
- [ ] `feature-multi-module.png` - Multiple modules navigation
- [ ] `feature-search-filter.png` - Search and filter in action
- [ ] `feature-node-highlight.png` - Node highlighting feature
- [ ] `example-large-project.png` - Large project analysis

## Taking Screenshots

### For HTML Visualizations
1. Open the generated HTML in a modern browser
2. Zoom to show the full graph clearly
3. Use browser's screenshot tool or:
   - macOS: Cmd+Shift+4
   - Windows: Win+Shift+S
   - Linux: Use screenshot tool

### Best Practices
- Show the full interface (including controls)
- Ensure text is readable
- Capture interesting/representative examples
- Use consistent browser window size
- Optimize images before committing

## Image Optimization

Before committing images, optimize them:

```bash
# Using ImageOptim (macOS)
# Drag and drop images to ImageOptim

# Using pngquant (cross-platform)
pngquant --quality=65-80 input.png -o output.png

# Using online tools
# https://tinypng.com/
# https://squoosh.app/
```

---

**Last Updated**: 2024-12-01

