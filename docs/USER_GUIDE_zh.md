# 用户指南 - C++ 依赖关系分析工具

## 目录

1. [安装](#安装)
2. [基本用法](#基本用法)
3. [高级功能](#高级功能)
4. [配置](#配置)
5. [故障排除](#故障排除)
6. [最佳实践](#最佳实践)

## 安装

### 系统要求

- Python 3.6 或更高版本
- 无需外部依赖（仅使用 Python 标准库）

### 快速安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/cxx_includes_analysis.git
cd cxx_includes_analysis

# 可选：作为包安装
pip install -e .
```

### 验证安装

```bash
python3 analyze_includes.py --help
```

## 基本用法

### 分析单个文件

最简单的使用方式：

```bash
python3 analyze_includes.py src/main.cpp
```

这将：
- 分析 `src/main.cpp` 及其所有依赖
- 在当前目录生成 `dependency_graph.html`
- 使用默认的 include 路径和设置

### 分析多个文件

一次分析多个模块：

```bash
python3 analyze_includes.py file1.cpp file2.cpp file3.cpp
```

生成的 HTML 将包含导航按钮，可在模块间切换。

### 指定输出文件

```bash
python3 analyze_includes.py src/main.cpp -o my_analysis.html
```

### 添加 Include 路径

如果项目有自定义的 include 目录：

```bash
python3 analyze_includes.py src/main.cpp \
    -I ./include \
    -I ./third_party/boost \
    -I /opt/local/include
```

## 高级功能

### 控制递归深度

限制分析器追踪依赖的深度：

```bash
# 只分析 2 层深度
python3 analyze_includes.py src/main.cpp --depth 2

# 深度分析（5 层）
python3 analyze_includes.py src/main.cpp --depth 5
```

**使用场景：**
- `--depth 1`: 仅直接包含的文件
- `--depth 2-3`: 标准分析（默认：3）
- `--depth 4-5`: 复杂项目的深度分析
- `--depth 10+`: 完整依赖树（可能较慢）

### 深度系统头文件分析

默认情况下，系统头文件不会被深度分析。启用深度扫描：

```bash
python3 analyze_includes.py src/main.cpp --deep-system
```

**警告：** 这会显著增加分析时间和图表复杂度。

### 输出格式

#### HTML 格式（交互式）

```bash
python3 analyze_includes.py src/main.cpp --format html
```

特性：
- 交互式 D3.js 可视化
- 两种布局模式（树状和力导向）
- 搜索和过滤功能
- 节点高亮和导航

#### DOT 格式（Graphviz）

```bash
python3 analyze_includes.py src/main.cpp --format dot
```

从 DOT 文件生成图片：

```bash
# PNG 图片
dot -Tpng dependencies.dot -o graph.png

# SVG 图片
dot -Tsvg dependencies.dot -o graph.svg

# PDF 文档
dot -Tpdf dependencies.dot -o graph.pdf
```

#### 两种格式

```bash
python3 analyze_includes.py src/main.cpp --format both
```

### 批量分析示例

#### 分析所有服务文件

```bash
python3 analyze_includes.py src/*_service.cpp -o services.html
```

#### 分析特定模块

```bash
python3 analyze_includes.py \
    ad_server/ad_server.cpp \
    recall_server/recall_server.cpp \
    rank_server/rank_server.cpp \
    -I ./common/include \
    -o backend_services.html
```

#### 使用 find 命令

```bash
# 分析 src 目录下所有 .cpp 文件
python3 analyze_includes.py $(find src -name "*.cpp") -o project_deps.html

# 只分析测试文件
python3 analyze_includes.py $(find tests -name "*_test.cpp") -o tests_deps.html
```

## 配置

### 默认 Include 路径

编辑 `analyze_includes_lib/config.py` 修改默认路径：

```python
DEFAULT_INCLUDE_PATHS = [
    ".",
    "build64_release",
    "/usr/include",
    "/usr/local/include",
    # 在这里添加自定义路径
    "/opt/myproject/include",
]
```

### 添加第三方库

要识别新的第三方库，编辑 `config.py` 中的 `THIRD_PARTY_LIBS`：

```python
THIRD_PARTY_LIBS = {
    'boost': 'Boost',
    'absl': 'Abseil',
    'mylib': 'MyCustomLib',  # 添加你的库
}
```

### 自定义颜色

修改 `config.py` 中的 `SIZE_COLOR_MAP`：

```python
SIZE_COLOR_MAP = [
    (10 * 1024, "#E8F5E9"),   # < 10KB: 浅绿色
    (50 * 1024, "#FFF9C4"),   # < 50KB: 浅黄色
    (200 * 1024, "#FFE0B2"),  # < 200KB: 浅橙色
    (float('inf'), "#FFCDD2"), # >= 200KB: 浅红色
]
```

## 交互式 HTML 指南

### 导航

**模块切换：**
- 点击 "Previous" / "Next" 按钮
- 使用键盘：`←`（上一个）/ `→`（下一个）

**画布移动：**
- 拖拽空白区域平移
- 鼠标滚轮缩放
- 双击空白区域重置视图

### 节点交互

**点击节点：**
- 红色边：该节点依赖的文件
- 绿色边：依赖该节点的文件
- 其他节点/边变暗

**拖拽节点：**
- 手动调整位置
- 在树状和力导向布局中都可用

**双击节点：**
- 重置到默认位置（仅力导向布局）

### 搜索和过滤

在搜索框中输入以过滤：
- 匹配文件名（不区分大小写）
- 高亮匹配的节点
- 只显示相关的边

清空搜索恢复完整图表。

### 布局模式

**树状布局：**
- 从左到右的层级排列
- 按目录/库类型分组
- 适合理解依赖层级
- 每层内的顺序：
  1. 项目文件
  2. 第三方库
  3. 生成的文件（Protobuf）
  4. 系统库

**力导向布局：**
- 基于物理的动态布局
- 节点互相排斥
- 边充当弹簧
- 适合探索复杂关系

## 故障排除

### 问题：缺少依赖

**症状：** 某些预期的文件没有出现在图表中。

**解决方案：**
1. 使用 `-I` 添加缺失的 include 路径
2. 使用 `--depth` 增加递归深度
3. 检查文件是否条件包含（`#ifdef`）
4. 验证文件路径是否正确

### 问题：图表太大

**症状：** HTML 文件很大，浏览器很慢。

**解决方案：**
1. 减少深度：`--depth 2`
2. 一次分析更少的文件
3. 除非必要，不使用 `--deep-system`
4. 使用搜索聚焦特定文件

### 问题：找不到文件

**症状：** "Warning: File xxx not found"

**解决方案：**
1. 检查文件路径是否正确
2. 如果相对路径失败，使用绝对路径
3. 确保文件存在且可读

### 问题：系统头文件未显示

**症状：** 像 `<iostream>` 这样的系统包含没有出现。

**解决方案：**
1. 这是正常的 - 系统头文件会显示但不会深度分析
2. 使用 `--deep-system` 详细分析系统头文件
3. 检查系统 include 路径是否在 `DEFAULT_INCLUDE_PATHS` 中

## 最佳实践

### 小型项目（< 50 个文件）

```bash
python3 analyze_includes.py src/*.cpp --depth 5 -o project.html
```

### 中型项目（50-200 个文件）

```bash
# 按模块分析
python3 analyze_includes.py module1/*.cpp -o module1.html
python3 analyze_includes.py module2/*.cpp -o module2.html

# 或只分析关键文件
python3 analyze_includes.py src/main.cpp src/server.cpp --depth 3
```

### 大型项目（> 200 个文件）

```bash
# 分析特定子系统
python3 analyze_includes.py backend/*.cpp --depth 2 -o backend.html

# 使用较浅的深度
python3 analyze_includes.py src/*.cpp --depth 2

# 关注入口点
python3 analyze_includes.py src/main.cpp src/server_main.cpp --depth 3
```

### CI/CD 集成

```bash
# 在 CI 中生成依赖报告
python3 analyze_includes.py src/main.cpp -o deps.html --depth 3

# 归档为构建产物
# (取决于你的 CI 系统)
```

### 定期依赖审计

```bash
# 每周依赖分析
python3 analyze_includes.py $(find src -name "*.cpp") \
    -o weekly_deps_$(date +%Y%m%d).html
```

## 技巧和窍门

1. **从浅层开始：** 从 `--depth 2` 开始，需要时再增加
2. **使用搜索：** 在大图表中，搜索是你的好帮手
3. **明智批量：** 将相关文件分组进行批量分析
4. **保存配置：** 为常见分析创建 shell 脚本
5. **随时间比较：** 生成定期报告以跟踪变化
6. **关注入口点：** 分析主文件和关键模块
7. **排除构建产物：** 不要直接分析生成的文件

## 下一步

- 查看 [API 文档](API_zh.md) 了解库的使用
- 参考 [示例](../examples/) 了解更多用例
- 阅读 [CONTRIBUTING.md](../CONTRIBUTING.md) 参与贡献

