# analyze_includes_lib - C++ 依赖关系分析库

这是一个模块化的 C++ 依赖关系分析库，用于解析和可视化 C++ 项目的 include 依赖关系。

## 目录结构

```
analyze_includes_lib/
├── __init__.py           # 库入口，导出主要类和函数
├── config.py             # 配置文件（默认路径、正则表达式、第三方库列表等）
├── utils.py              # 工具函数（文件操作、路径处理、格式化等）
├── analyzer.py           # 依赖分析器（解析 C++ 文件的 include 关系）
├── dot_visualizer.py     # DOT 格式可视化器（生成 Graphviz 文件）
├── html_visualizer.py    # HTML 可视化器（生成交互式 D3.js 图表）
├── html_template.py      # HTML 模板（CSS、JavaScript 代码）
└── README.md             # 本文件
```

## 模块说明

### 1. config.py - 配置模块
包含所有配置项：
- `DEFAULT_INCLUDE_PATHS`: 默认的 include 搜索路径
- `INCLUDE_PATTERN`: 匹配 `#include` 语句的正则表达式
- `THIRD_PARTY_LIBS`: 第三方库识别配置
- `SIZE_COLOR_MAP`: 文件大小颜色映射

### 2. utils.py - 工具函数模块
提供常用的工具函数：
- `get_file_size(path)`: 获取文件大小
- `format_size(size)`: 格式化文件大小为人类可读格式
- `get_node_color(size)`: 根据文件大小返回颜色
- `simplify_path(path)`: 简化路径（相对路径）
- `get_directory_cluster(path)`: 获取文件所属的集群（分组）
- `get_cluster_priority(cluster_name)`: 获取集群的排序优先级

### 3. analyzer.py - 依赖分析器
核心分析模块：
- `DependencyAnalyzer`: 依赖分析器类
  - `__init__(include_paths, max_depth, deep_system)`: 初始化分析器
  - `find_file(filename, is_system, current_dir)`: 查找头文件
  - `analyze(start_file)`: 分析指定文件的依赖关系

### 4. dot_visualizer.py - DOT 可视化器
生成 Graphviz DOT 格式：
- `DotVisualizer`: DOT 格式可视化器类
  - `__init__(nodes, edges, source_file)`: 初始化
  - `generate(output_file)`: 生成 DOT 文件
  - `_draw_clusters(f, clusters)`: 绘制集群
  - `_draw_edges(f)`: 绘制边

### 5. html_visualizer.py - HTML 可视化器
生成交互式 HTML：
- `HtmlVisualizer`: HTML 可视化器类
  - `__init__(modules_data)`: 初始化（支持多模块）
  - `generate(output_file)`: 生成 HTML 文件
  - `_prepare_module_data(module_info)`: 准备模块数据

### 6. html_template.py - HTML 模板
包含 HTML、CSS 和 JavaScript 代码：
- `get_html_template(modules_json, total_modules)`: 返回完整 HTML
- `get_css_styles()`: 返回 CSS 样式
- `get_html_body()`: 返回 HTML body
- `get_javascript_code(modules_json)`: 返回 JavaScript 代码

## 使用示例

### 基本用法

```python
from analyze_includes_lib import (
    DEFAULT_INCLUDE_PATHS,
    DependencyAnalyzer,
    HtmlVisualizer
)

# 创建分析器
analyzer = DependencyAnalyzer(
    include_paths=DEFAULT_INCLUDE_PATHS,
    max_depth=3,
    deep_system=False
)

# 分析文件
nodes, edges = analyzer.analyze("src/main.cpp")

# 生成 HTML
modules_data = [{
    'source_file': "src/main.cpp",
    'nodes': nodes,
    'edges': edges
}]

visualizer = HtmlVisualizer(modules_data)
visualizer.generate("output.html")
```

### 批量分析

```python
# 分析多个文件
source_files = ["file1.cpp", "file2.cpp", "file3.cpp"]
modules_data = []

for source_file in source_files:
    nodes, edges = analyzer.analyze(source_file)
    modules_data.append({
        'source_file': source_file,
        'nodes': nodes,
        'edges': edges
    })

# 生成支持模块切换的 HTML
visualizer = HtmlVisualizer(modules_data)
visualizer.generate("multi_modules.html")
```

### 生成 DOT 文件

```python
from analyze_includes_lib import DotVisualizer

# 分析文件
nodes, edges = analyzer.analyze("src/main.cpp")

# 生成 DOT
visualizer = DotVisualizer(nodes, edges, "src/main.cpp")
visualizer.generate("dependencies.dot")
```

## 扩展和定制

### 添加新的第三方库识别

编辑 `config.py` 中的 `THIRD_PARTY_LIBS` 字典：

```python
THIRD_PARTY_LIBS = {
    'boost': 'Boost',
    'your_lib': 'YourLib',  # 添加新库
    # ...
}
```

### 修改颜色映射

编辑 `config.py` 中的 `SIZE_COLOR_MAP`：

```python
SIZE_COLOR_MAP = [
    (10 * 1024, "#E8F5E9"),   # < 10KB
    (50 * 1024, "#FFF9C4"),   # < 50KB
    # 添加或修改颜色映射
]
```

### 自定义 HTML 样式

编辑 `html_template.py` 中的 `get_css_styles()` 函数。

### 自定义布局算法

编辑 `html_template.py` 中的 `get_javascript_code()` 函数，修改 `calculateTreeLayout()` 或其他布局相关代码。

## 设计原则

1. **单一职责**：每个模块负责一个特定功能
2. **松耦合**：模块之间通过明确的接口交互
3. **高内聚**：相关功能组织在一起
4. **可扩展**：易于添加新的可视化器或分析功能
5. **可测试**：每个模块都可以独立测试

## 依赖关系

```
config.py (配置)
    ↓
utils.py (工具函数) ← 依赖 config.py
    ↓
analyzer.py (分析器) ← 依赖 config.py
    ↓
dot_visualizer.py (DOT可视化) ← 依赖 utils.py
html_visualizer.py (HTML可视化) ← 依赖 utils.py, html_template.py
    ↓
html_template.py (HTML模板)
```

## 版本历史

### v2.0.0 (当前版本)
- 模块化重构
- 拆分为独立的模块
- 改进代码结构和可维护性

### v1.0.0
- 初始版本（单文件）
- 基本的依赖分析功能
- HTML 和 DOT 可视化

