# Documentation Structure / 文档结构说明

## 文档分层策略 / Documentation Hierarchy

本项目采用分层文档策略，避免内容重复，让用户能快速找到所需信息。

### 📄 文档层级 / Document Levels

```
README.md (概览层)
    ↓
QUICK_START.md (入门层)
    ↓
USER_GUIDE.md (详细层)
    ↓
API.md (技术层)
```

---

## 各文档的定位 / Document Positioning

### 1️⃣ README.md / README_zh.md
**定位**: 项目概览和快速索引

**目标读者**: 所有访问者（首次访问者、潜在用户、贡献者）

**内容原则**:
- ✅ 简洁明了，快速了解项目
- ✅ 突出核心特性
- ✅ 提供最基本的使用示例（2-3 个命令）
- ✅ 链接到详细文档
- ❌ 避免详细的使用说明
- ❌ 避免重复其他文档的内容

**包含内容**:
- 项目简介和徽章
- 核心功能特性（简要列表）
- 最简单的安装和使用（3-5 行命令）
- 文档索引（链接到其他文档）
- 命令行参数表格（快速参考）
- 交互功能概述（简要列表）
- 配置说明（简要，链接到详细文档）
- 贡献指南（简要步骤）
- 许可证、致谢、联系方式
- 路线图和截图

**长度**: 约 150-200 行

---

### 2️⃣ QUICK_START.md
**定位**: 5 分钟快速上手教程

**目标读者**: 新用户，想快速试用工具

**内容原则**:
- ✅ 场景化的使用示例
- ✅ 实用的常见用例
- ✅ 一步步的操作指导
- ✅ 包含如何打开结果的说明
- ❌ 不深入技术细节
- ❌ 不解释原理

**包含内容**:
- 3 步快速开始（获取代码、试用示例、分析自己的代码）
- 常见使用场景（4-6 个实际场景）
  - 快速项目概览
  - 深度依赖分析
  - 多模块分析
  - 生成静态图片
- 交互式 HTML 功能简介
- 下一步指引（链接到详细文档）
- 实用小贴士

**长度**: 约 150-250 行

**与 README 的区别**:
- README: "这是什么" + "能做什么"
- QUICK_START: "怎么用" + "常见场景"

---

### 3️⃣ USER_GUIDE.md / USER_GUIDE_zh.md
**定位**: 完整的用户手册

**目标读者**: 需要深入使用工具的用户

**内容原则**:
- ✅ 详尽的使用说明
- ✅ 所有功能的完整介绍
- ✅ 最佳实践和技巧
- ✅ 故障排除指南
- ✅ 高级配置选项

**包含内容**:
- 详细的安装说明
- 基本和高级用法
- 所有命令行参数的详细说明
- 输出格式详解
- 批量分析详细示例
- 交互式 HTML 完整操作指南
- 配置文件详解
- 故障排除（FAQ）
- 不同规模项目的最佳实践
- CI/CD 集成示例
- 性能优化建议

**长度**: 约 300-400 行

**与 QUICK_START 的区别**:
- QUICK_START: 快速上手，常见场景
- USER_GUIDE: 深入理解，所有功能

---

### 4️⃣ API.md
**定位**: 编程接口文档

**目标读者**: 需要在代码中调用工具的开发者

**内容原则**:
- ✅ 完整的 API 参考
- ✅ 类和方法的详细说明
- ✅ 参数和返回值文档
- ✅ 代码示例
- ❌ 不包含命令行使用说明

**包含内容**:
- 安装和导入
- 核心类详解
  - DependencyAnalyzer
  - HtmlVisualizer
  - DotVisualizer
- 配置选项
- 工具函数
- 完整的代码示例
- 错误处理
- 线程安全说明
- 性能建议

**长度**: 约 400-500 行

---

### 5️⃣ CONTRIBUTING.md
**定位**: 贡献者指南

**目标读者**: 想要为项目做贡献的开发者

**包含内容**:
- 行为准则
- 开发环境设置
- 项目结构说明
- 编码规范
- 测试指南
- PR 流程
- Bug 报告和功能请求指南

---

### 6️⃣ PROJECT_STRUCTURE.md
**定位**: 项目架构文档

**目标读者**: 贡献者、维护者

**包含内容**:
- 完整的目录结构
- 各模块职责说明
- 设计原则
- 依赖关系
- 扩展指南

---

### 7️⃣ CHANGELOG.md
**定位**: 版本历史

**目标读者**: 所有用户

**包含内容**:
- 版本号和发布日期
- 新增功能
- 修复的 Bug
- 破坏性变更
- 迁移指南

---

## 文档间的链接关系 / Document Links

```
README.md
├─→ QUICK_START.md (快速开始)
├─→ USER_GUIDE.md (详细文档)
├─→ API.md (API 参考)
├─→ CONTRIBUTING.md (贡献指南)
├─→ examples/ (示例)
└─→ CHANGELOG.md (变更日志)

QUICK_START.md
├─→ USER_GUIDE.md (更多细节)
├─→ API.md (编程使用)
└─→ examples/ (示例代码)

USER_GUIDE.md
├─→ API.md (编程接口)
├─→ CONTRIBUTING.md (参与贡献)
└─→ examples/ (示例)

API.md
├─→ USER_GUIDE.md (命令行使用)
└─→ examples/ (示例代码)
```

---

## 用户旅程 / User Journey

### 新用户 (New User)
1. **README.md** - 了解项目是什么
2. **QUICK_START.md** - 5 分钟试用
3. **USER_GUIDE.md** - 深入学习
4. **examples/** - 查看更多示例

### 开发者 (Developer)
1. **README.md** - 了解项目
2. **API.md** - 学习 API
3. **examples/** - 参考示例代码
4. **CONTRIBUTING.md** - 准备贡献

### 贡献者 (Contributor)
1. **CONTRIBUTING.md** - 了解贡献流程
2. **PROJECT_STRUCTURE.md** - 理解项目结构
3. **USER_GUIDE.md** - 了解功能
4. **API.md** - 理解实现

---

## 维护原则 / Maintenance Principles

### 避免重复 / Avoid Duplication
- 每个信息只在最合适的地方详细说明
- 其他地方通过链接引用
- 保持文档间的一致性

### 分层清晰 / Clear Hierarchy
- README: 概览 (Overview)
- QUICK_START: 入门 (Getting Started)
- USER_GUIDE: 详解 (Deep Dive)
- API: 技术 (Technical Reference)

### 更新策略 / Update Strategy
1. 功能变更时，先更新 API.md
2. 然后更新 USER_GUIDE.md
3. 如果影响基本用法，更新 QUICK_START.md
4. 最后更新 README.md 中的简要说明
5. 在 CHANGELOG.md 中记录变更

---

## 检查清单 / Checklist

添加新功能时，检查是否需要更新：

- [ ] README.md - 如果是核心功能
- [ ] QUICK_START.md - 如果是常用场景
- [ ] USER_GUIDE.md - 详细说明
- [ ] API.md - 如果有 API 变更
- [ ] examples/ - 添加示例
- [ ] CHANGELOG.md - 记录变更

---

## 文档质量标准 / Quality Standards

### 所有文档应该：
- ✅ 使用清晰的标题层级
- ✅ 包含代码示例
- ✅ 使用表情符号增强可读性（适度）
- ✅ 提供中英双语版本（主要文档）
- ✅ 包含"下一步"指引
- ✅ 链接到相关文档

### 避免：
- ❌ 过长的段落
- ❌ 重复其他文档的内容
- ❌ 缺少示例的抽象说明
- ❌ 过时的信息
- ❌ 死链接

---

**最后更新**: 2024-12-01
**版本**: 2.0.0

