# Quick Start Guide / 快速开始指南

[English](#english) | [中文](#中文)

---

## English

### 5-Minute Quick Start

#### 1. Get the Code
```bash
git clone https://github.com/yourusername/cxx_includes_analysis.git
cd cxx_includes_analysis
```

#### 2. Try the Example
```bash
# Analyze the simple example
python3 analyze_includes.py examples/simple/main.cpp -I examples/simple

# Open the generated HTML file
# On macOS:
open dependency_graph.html
# On Linux:
xdg-open dependency_graph.html
# On Windows:
start dependency_graph.html
```

You should see an interactive graph like this:

![Example Output](docs/images/example-simple-dependency-graph.png)

The graph shows dependencies between `main.cpp`, `utils.h`, `config.h` and system headers.

#### 3. Analyze Your Own Code
```bash
# Single file
python3 analyze_includes.py /path/to/your/main.cpp

# Multiple files
python3 analyze_includes.py src/*.cpp -o my_project.html

# With custom include paths
python3 analyze_includes.py src/main.cpp -I ./include -I ./third_party
```

### Common Use Cases

#### Use Case 1: Quick Project Overview
```bash
# Shallow analysis for quick overview
python3 analyze_includes.py src/main.cpp --depth 2
```

#### Use Case 2: Deep Dependency Analysis
```bash
# Deep analysis with system headers
python3 analyze_includes.py src/main.cpp --depth 5 --deep-system
```

#### Use Case 3: Multiple Modules
```bash
# Analyze all service modules
python3 analyze_includes.py \
    service1/main.cpp \
    service2/main.cpp \
    service3/main.cpp \
    -o services.html
```

#### Use Case 4: Generate Static Image
```bash
# Generate DOT file
python3 analyze_includes.py src/main.cpp --format dot

# Convert to PNG (requires Graphviz)
dot -Tpng dependencies.dot -o graph.png
```

### Interactive HTML Features

Once you open the HTML file:

1. **Navigate**: Use Previous/Next buttons or ← → keys
2. **Explore**: Click nodes to highlight dependencies
3. **Search**: Type in the search box to filter
4. **Layout**: Toggle between tree and force-directed layouts
5. **Zoom**: Use mouse wheel to zoom in/out
6. **Pan**: Drag blank area to move around

### Next Steps

- Read the [User Guide](docs/USER_GUIDE.md) for detailed instructions
- Check out more [Examples](examples/)
- Learn about the [API](docs/API.md) for programmatic usage

### Need Help?

- 📖 [Documentation](docs/)
- 🐛 [Report Issues](https://github.com/yourusername/cxx_includes_analysis/issues)
- 💬 [Discussions](https://github.com/yourusername/cxx_includes_analysis/discussions)

---

## 中文

### 5 分钟快速开始

#### 1. 获取代码
```bash
git clone https://github.com/yourusername/cxx_includes_analysis.git
cd cxx_includes_analysis
```

#### 2. 尝试示例
```bash
# 分析简单示例
python3 analyze_includes.py examples/simple/main.cpp -I examples/simple

# 打开生成的 HTML 文件
# macOS:
open dependency_graph.html
# Linux:
xdg-open dependency_graph.html
# Windows:
start dependency_graph.html
```

你会看到这样的交互式图表：

![示例输出](docs/images/example-simple-dependency-graph.png)

图表展示了 `main.cpp`、`utils.h`、`config.h` 与系统头文件之间的依赖关系。

#### 3. 分析你自己的代码
```bash
# 单个文件
python3 analyze_includes.py /path/to/your/main.cpp

# 多个文件
python3 analyze_includes.py src/*.cpp -o my_project.html

# 添加自定义 include 路径
python3 analyze_includes.py src/main.cpp -I ./include -I ./third_party
```

### 常见使用场景

#### 场景 1: 快速项目概览
```bash
# 浅层分析，快速了解项目结构
python3 analyze_includes.py src/main.cpp --depth 2
```

#### 场景 2: 深度依赖分析
```bash
# 深度分析，包含系统头文件
python3 analyze_includes.py src/main.cpp --depth 5 --deep-system
```

#### 场景 3: 多模块分析
```bash
# 分析所有服务模块
python3 analyze_includes.py \
    service1/main.cpp \
    service2/main.cpp \
    service3/main.cpp \
    -o services.html
```

#### 场景 4: 生成静态图片
```bash
# 生成 DOT 文件
python3 analyze_includes.py src/main.cpp --format dot

# 转换为 PNG（需要安装 Graphviz）
dot -Tpng dependencies.dot -o graph.png
```

### 交互式 HTML 功能

打开 HTML 文件后：

1. **导航**: 使用 Previous/Next 按钮或 ← → 键
2. **探索**: 点击节点高亮显示依赖关系
3. **搜索**: 在搜索框中输入以过滤
4. **布局**: 在树状布局和力导向布局间切换
5. **缩放**: 使用鼠标滚轮放大/缩小
6. **平移**: 拖拽空白区域移动

### 下一步

- 阅读[用户指南](docs/USER_GUIDE_zh.md)了解详细说明
- 查看更多[示例](examples/)
- 学习 [API](docs/API.md) 进行编程使用

### 需要帮助？

- 📖 [文档](docs/)
- 🐛 [报告问题](https://github.com/yourusername/cxx_includes_analysis/issues)
- 💬 [讨论区](https://github.com/yourusername/cxx_includes_analysis/discussions)

---

## Tips / 小贴士

### English
- Start with `--depth 2` for quick analysis
- Use `--deep-system` only when needed (it's slow)
- Search is your friend in large graphs
- Try both layout modes to find what works best
- Save frequently used commands as shell scripts

### 中文
- 从 `--depth 2` 开始进行快速分析
- 只在需要时使用 `--deep-system`（会很慢）
- 在大型图表中多使用搜索功能
- 尝试两种布局模式，找到最适合的
- 将常用命令保存为 shell 脚本

---

**Happy Analyzing! / 分析愉快！** 🎉

