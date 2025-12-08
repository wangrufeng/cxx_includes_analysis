# Blade 依赖分析工具 - 快速开始

## 5 分钟上手指南

### 第一步：确认环境

确保你在一个 Blade 项目目录中（包含 BLADE_ROOT 文件）：

```bash
# 检查是否有 BLADE_ROOT 文件
ls BLADE_ROOT

# 或者查看项目结构
tree -L 2
```

### 第二步：运行分析

```bash
./analyze_deps.py path/to/dir:target_name
```

**示例：**

```bash
./analyze_deps.py ads/serving/show:brpc_ranking_server
```

### 第三步：查看结果

```bash
# macOS
open blade_dependency_graph.html

# Linux
xdg-open blade_dependency_graph.html

# Windows
start blade_dependency_graph.html
```

## 常见使用场景

### 场景 1：分析服务器依赖

**目标**：了解 brpc_ranking_server 依赖了哪些库

```bash
./analyze_deps.py ads/serving/show:brpc_ranking_server
```

**结果**：生成依赖关系图，显示所有直接和间接依赖

### 场景 2：检查库的影响范围

**目标**：修改某个库前，查看有多少 target 依赖它

```bash
./analyze_deps.py ads/common:utility --depth 3
```

**结果**：显示所有依赖 utility 库的 target

### 场景 3：优化构建依赖

**目标**：发现不必要的依赖关系

```bash
./analyze_deps.py your_module:your_target --depth 10
```

**结果**：完整的依赖树，可以发现循环依赖或冗余依赖

## 命令参数速查

| 参数 | 说明 | 示例 |
|------|------|------|
| `target` | 要分析的 target | `ads/serving/show:server` |
| `--blade-root` | 指定项目根目录 | `--blade-root /path/to/project` |
| `--depth` | 最大递归深度 | `--depth 5` |
| `-o` | 输出文件名 | `-o deps.html` |

## 交互式 HTML 功能

### 基本操作

1. **查看依赖关系**
   - 点击任意节点
   - 红色线：该节点依赖的 target
   - 绿色线：依赖该节点的 target

2. **搜索 Target**
   - 在搜索框输入关键词
   - 自动过滤和高亮匹配的节点

3. **调整视图**
   - 鼠标滚轮：缩放
   - 拖拽画布：移动
   - 拖拽节点：调整位置

4. **切换布局**
   - 树状布局：按层级排列
   - 力导向布局：动态布局

5. **收起控制面板**
   - 点击左上角 ◀ 按钮
   - 获得更大的可视区域

### 查看详细信息

点击节点后，控制面板显示：

- **Target 名称**：完整的 target 路径
- **类型**：cc_library、cc_binary 等
- **模块**：所属模块分类
- **源文件数**：srcs 列表中的文件数
- **头文件数**：hdrs 列表中的文件数
- **依赖数**：该 target 依赖的其他 target 数量
- **被依赖数**：有多少 target 依赖该 target

## 理解依赖路径

BUILD 文件中的三种依赖格式：

### 1. 相对依赖（:name）

```python
deps = [
    ':cpc_util',  # 同目录下的 cpc_util target
]
```

### 2. 绝对依赖（//path:name）

```python
deps = [
    '//ads/proto:ranking_cpc_proto',  # 完整路径
]
```

### 3. 外部依赖（#name）

```python
deps = [
    '#glog',      # 外部库
    '#gflags',
    '#tcmalloc_and_profiler',
]
```

## 实用技巧

### 技巧 1：从小范围开始

第一次分析时，使用较小的深度：

```bash
./analyze_deps.py your_target --depth 2
```

然后根据需要逐步增加深度。

### 技巧 2：自定义输出文件名

为不同的分析保存不同的文件：

```bash
./analyze_deps.py module_a:target -o module_a_deps.html
./analyze_deps.py module_b:target -o module_b_deps.html
```

### 技巧 3：在非项目目录运行

如果不在项目根目录，指定 BLADE_ROOT：

```bash
./analyze_deps.py ads/serving/show:server --blade-root /path/to/project
```

## 故障排除

### 问题 1：找不到 BLADE_ROOT

**错误信息：**
```
✗ 错误：找不到 BLADE_ROOT 文件。
```

**解决方法：**
- 确保在 Blade 项目目录中运行
- 或使用 `--blade-root` 参数指定项目根目录

### 问题 2：找不到 target

**错误信息：**
```
⚠ 警告：找不到 target ads/serving/show:brpc_ranking_server
```

**解决方法：**
- 检查 target 路径是否正确
- 确认 BUILD 文件存在
- 确认 target 名称拼写正确

### 问题 3：BUILD 文件解析失败

**错误信息：**
```
⚠ 警告：解析 BUILD 文件时出错
```

**解决方法：**
- 检查 BUILD 文件语法是否正确
- 确保使用标准的 Blade 语法

## 下一步

- 📖 查看详细文档：[BLADE_DEPS_GUIDE.md](BLADE_DEPS_GUIDE.md)
- 🎯 查看示例：[examples/blade_example.md](examples/blade_example.md)
- 🧪 试用测试项目：`cd test_blade_project && python3 ../analyze_deps.py ads/serving/show:brpc_ranking_server`

## 获取帮助

查看完整的命令行帮助：

```bash
./analyze_deps.py --help
```

---

**开始分析你的项目依赖吧！** 🚀

