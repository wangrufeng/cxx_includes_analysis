# Blade 依赖分析工具

## 快速开始

分析 Blade 构建系统中 target 的依赖关系：

```bash
./analyze_deps.py ads/serving/show:brpc_ranking_server
```

## 功能说明

`analyze_deps.py` 是一个专门用于分析 Blade 构建系统库依赖关系的工具：

- 📦 **库级别分析**：分析 BUILD 文件中定义的 target 依赖关系
- 🔍 **递归解析**：自动追踪所有直接和间接依赖
- 🎨 **可视化展示**：生成交互式 HTML 依赖关系图
- 🏷️ **智能分类**：按模块自动分组，区分内部库和外部依赖

## 与 analyze_includes.py 的区别

| 工具 | 分析对象 | 粒度 | 使用场景 |
|------|---------|------|---------|
| `analyze_includes.py` | C++ 源文件的 #include 依赖 | 文件级别 | 分析代码文件依赖 |
| `analyze_deps.py` | Blade target 的库依赖 | 库/target 级别 | 分析构建系统依赖 |

## 示例

### 分析服务器依赖

```bash
./analyze_deps.py ads/serving/show:brpc_ranking_server
```

输出：
```
BLADE_ROOT: /path/to/project
分析 Target: ads/serving/show:brpc_ranking_server
最大深度: 10

正在分析依赖关系...
✓ 发现 45 个 target 和 67 个依赖关系

Target 类型统计：
  cc_binary: 1
  cc_library: 32
  external: 8
  proto_library: 4
  外部依赖: 8

✓ 交互式 HTML 已生成：blade_dependency_graph.html
```

### 自定义输出

```bash
./analyze_deps.py ads/serving/show:brpc_ranking_server -o server_deps.html --depth 5
```

## 支持的 Target 类型

- `cc_library` - C++ 库
- `cc_binary` - C++ 可执行文件
- `cc_test` - C++ 测试
- `proto_library` - Protocol Buffers 库
- 以及其他 Blade target 类型

## 依赖路径格式

BUILD 文件中支持的依赖格式：

```python
deps = [
    ':local_target',           # 相对依赖：同目录下的 target
    '//ads/proto:proto_name',  # 绝对依赖：完整路径
    '#glog',                   # 外部依赖：系统库或第三方库
]
```

## 详细文档

查看完整使用指南：[BLADE_DEPS_GUIDE.md](BLADE_DEPS_GUIDE.md)

## 示例项目

在 `test_blade_project/` 目录下有一个示例项目，可以用来测试工具：

```bash
cd test_blade_project
python3 ../analyze_deps.py ads/serving/show:brpc_ranking_server
```

