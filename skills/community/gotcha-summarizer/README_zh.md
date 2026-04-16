# Gotcha Summarizer 技能

自动将 Claude Code 对话中的技术经验总结为结构化的 Markdown 文档。

## 概述

此技能分析对话历史以提取：

**前端开发：**
- 前端 Bug 和根本原因（水合错误、内存泄漏、渲染问题）
- 框架问题（React、Vue、Next.js、Nuxt、Svelte、Angular）
- 样式问题（CSS、SCSS、Tailwind、UnoCSS）
- 构建工具问题（Vite、Webpack、Rollup、esbuild）
- 状态管理（Redux、Pinia、Zustand、Jotai、Vuex）
- UI 组件库问题（Ant Design、Element Plus、shadcn/ui）

**后端开发：**
- 后端 Bug 和根本原因（空指针、竞态条件、数据库错误）
- 数据库/ORM 问题（SQL、迁移、Bun、GORM、Ent、sqlx）
- API 问题（REST、GraphQL、gRPC、端点、控制器）
- 并发问题（goroutines、互斥锁、通道、上下文）
- 性能问题（缓存、Redis、慢查询、索引）
- 精度问题（decimal vs float、金额/数量处理）

**通用开发：**
- 测试问题和解决方案（单元测试、集成测试、mock）
- CI/CD 流水线问题（GitHub Actions、Docker、部署）
- Git/版本控制问题（合并冲突、变基、分支）
- 代码质量改进（重构、设计模式）
- 任何值得记录的技术经验

## 安装

该技能安装在 `~/.claude/skills/gotcha-summarizer/` 目录。

## 使用方法

### 基本用法

```bash
# 从任何位置运行以分析最新对话
python3 ~/.claude/skills/gotcha-summarizer/scripts/summarize.py

# 或使用 shell 包装脚本
~/.claude/skills/gotcha-summarizer/scripts/gotcha-summarize.sh
```

### 使用 Claude Code 技能命令

```
skill gotcha-summarizer
```

### 环境变量

| 变量 | 默认值 | 描述 |
|----------|---------|-------------|
| `GOTCHAS_DIR` | `./docs/gotchas` | docs/gotchas 目录路径 |
| `CLAUDE_HISTORY_PATH` | 自动检测 | 对话历史文件路径 |
| `DRY_RUN` | `false` | 设置为 `true` 可预览更改而不写入 |
| `TIMESTAMP_FORMAT` | `%Y-%m-%d %H:%M:%S` | 生成 markdown 中时间戳的格式 |
| `LOCALE` | `zh` | 界面语言（`zh` 为中文，`en` 为英文） |
| `LOG_LEVEL` | `WARNING` | 日志级别（`DEBUG`、`INFO`、`WARNING`、`ERROR`） |
| `ENABLE_ERROR_TRACKING` | `false` | 启用详细的错误跟踪和统计 |

### 使用示例

```bash
# 预览更改而不写入
DRY_RUN=true python3 ~/.claude/skills/gotcha-summarizer/scripts/summarize.py

# 指定自定义 gotchas 目录
GOTCHAS_DIR=/path/to/docs/gotchas python3 ~/.claude/skills/gotcha-summarizer/scripts/summarize.py

# 使用特定的对话历史
CLAUDE_HISTORY_PATH=/path/to/history.jsonl python3 ~/.claude/skills/gotcha-summarizer/scripts/summarize.py
```

## 工作原理

### 1. 对话分析

该技能读取 Claude Code 对话历史（JSONL 格式）并分析消息中的：
- 错误信息
- 代码块（支持 18+ 编程语言的自动语言检测）
- 问题/解决方案模式
- 根本原因
- 最佳实践
- 技术讨论

### 2. 主题分类（带置信度评分）

使用三层决策树，该技能对每个经验进行分类：

**第一层：领域分类**（Common / Frontend / Backend）
- 最小文本长度检查（20 字符）
- 加权关键词评分
- 置信度分数输出

**第二层：类别分类**（例如：Bugs、Framework、Database、API）
- 特定领域的类别评分
- 最小长度检查（15 字符）
- 置信度分数输出

**第三层：文件映射**（Category → markdown 文件）

```
START: 分析对话中的技术问题
│
├─ 第一层：领域分类
│   │
│   ├─ COMMON（Testing、CI/CD、Git）→ common/
│   ├─ FRONTEND（React、Vue、CSS 等）→ frontend/
│   └─ BACKEND（SQL、API、Goroutines 等）→ backend/
│
├─ 第二层：类别分类
│   │
│   ├─ Bugs（最高优先级）
│   ├─ Framework / Database / Testing（特定领域）
│   └─ 其他类别（styling、build tools、state mgmt 等）
│
└─ 第三层：文件映射
    └─ frontend/bugs.md、backend/database.md、common/git.md 等
```

### 3. 重复检测

在添加新内容之前，该技能会：
- 读取所有现有的 gotcha 文件
- 检查相似的标题（模糊匹配）
- 检查相似的错误信息
- 如果检测到重复则跳过添加（并显示警告）

### 4. Markdown 生成

该技能生成遵循以下格式的 markdown 部分：

```markdown
## 问题：[简短标题]

> **自动生成时间**: 2026-02-02 12:00:00

### 错误信息
```
错误信息内容
```

### 相关代码
```go
// ❌ 错误用法
[代码示例]
```

### 问题描述
[解释为什么会发生这个问题]

---
```

## 输出文件

该技能更新 `docs/gotchas/` 目录中的文件：

| 领域 | 文件 | 类别 | 示例 |
|--------|------|----------|----------|
| **Frontend** | `frontend/bugs.md` | 前端 Bug | 水合错误、内存泄漏、重渲染问题 |
| | `frontend/frameworks.md` | 框架 | React、Vue、Next.js、Nuxt、Svelte、Angular |
| | `frontend/styling.md` | 样式 | CSS、SCSS、Tailwind、UnoCSS、styled-components |
| | `frontend/build-tools.md` | 构建工具 | Vite、Webpack、Rollup、esbuild、HMR |
| | `frontend/state-mgmt.md` | 状态管理 | Redux、Pinia、Zustand、Jotai、Vuex |
| | `frontend/ui-components.md` | UI 组件 | Ant Design、Element Plus、shadcn/ui、MUI |
| **Backend** | `backend/bugs.md` | 后端 Bug | 空指针、竞态条件、SQL 错误 |
| | `backend/database.md` | 数据库 | SQL、ORM（Bun、GORM、Ent）、迁移 |
| | `backend/api.md` | API | REST、GraphQL、gRPC、端点、控制器 |
| | `backend/concurrency.md` | 并发 | Goroutines、互斥锁、通道、上下文 |
| | `backend/performance.md` | 性能 | 缓存（Redis）、慢查询、索引、n+1 |
| | `backend/precision.md` | 精度 | Decimal vs float、金额/数量处理 |
| **Common** | `common/testing.md` | 测试 | 单元测试、集成测试、mock、TDD |
| | `common/cicd.md` | CI/CD | GitHub Actions、Docker、Kubernetes、部署 |
| | `common/git.md` | Git | 合并冲突、变基、分支管理 |
| | `common/code-quality.md` | 代码质量 | 重构、设计模式、linting |

## 与会话结束集成

要在对话结束时自动运行此技能，您可以在 Claude Code 配置中设置会话结束 hook（如果支持）。

## 故障排除

### 未发现技术问题

如果该技能未检测到任何技术问题：
- 确保对话包含错误信息、代码示例或问题解决讨论
- 尝试使用明确的说明手动触发该技能，说明要记录什么内容

### 重复条目

该技能尝试检测重复项，但偶尔可能创建相似的条目。审查生成的内容并根据需要合并或删除重复项。

### 文件权限错误

确保 `docs/gotchas/` 目录可写：
```bash
chmod +w docs/gotchas/*.md
```

## 开发

### 脚本结构

```
gotcha-summarizer/
├── SKILL.md                    # 技能定义和前言
├── README.md                   # 英文文档
├── README_zh.md                # 中文文档（本文件）
├── pytest.ini                  # Pytest 配置
├── test_features.py            # 快速内联测试脚本
└── scripts/
    ├── __init__.py             # 包初始化
    ├── summarize.py            # 主 Python 脚本
    ├── classifier.py           # 三层主题分类器
    ├── keywords.py             # 关键词配置（加权）
    └── config.py               # 配置常量和模板
└── tests/
    ├── __init__.py             # 测试包
    └── test_summarizer.py      # Pytest 测试套件
```

### Python 脚本组件

- `GotchaExtractor` - 从对话历史中提取经验，具有结构化字段提取
- `ThreeLayerTopicClassifier` - 三层分类，带置信度评分
- `TopicClassifier` - ThreeLayerTopicClassifier 的向后兼容包装器
- `DomainClassifier` - 第一层：带加权评分的领域分类
- `CategoryClassifier` - 第二层：带加权评分的类别分类
- `FileMapper` - 第三层：将类别映射到文件路径
- `MarkdownFormatter` - 格式化为 markdown，支持 i18n
- `GotchaFileManager` - 管理读/写 markdown 文件，带错误跟踪

### 运行测试

```bash
# 快速内联测试（无依赖）
python3 test_features.py

# 完整 pytest 套件（需要 pytest）
pip install pytest
pytest tests/test_summarizer.py -v

# 带覆盖率
pip install pytest-cov
pytest tests/test_summarizer.py --cov=scripts --cov-report=html
```

### 新功能（最新版本）

1. **结构化提取** - 提取问题、原因、解决方案和最佳实践
2. **多语言代码检测** - 支持 18+ 编程语言：
   - JSX/TSX、SQL、Vue、Bash、PowerShell、PHP、Ruby、Swift、Kotlin、C#、Dart、Rust、Go、Python、TypeScript、Java、JavaScript、C、C++
3. **多代码块支持** - 按语言分组和显示代码块
4. **置信度评分** - 分类返回置信度指标
5. **错误跟踪** - 跟踪 JSON 解析错误、文件 I/O 错误、分类错误
6. **可配置时间戳格式** - 通过 `TIMESTAMP_FORMAT` 环境变量自定义
7. **国际化** - 中文/英文标签，通过 `LOCALE` 环境变量配置
8. **改进的模糊匹配** - 降低阈值（0.75）以更好地检测重复项

## 贡献

要使用新类别扩展该技能：

1. 在 `TopicClassifier` 中为新类别添加关键词
2. 在 `docs/gotchas/` 中创建新的 markdown 文件
3. 更新 `SKILL.md` 中的决策树
4. 在 `GotchaFileManager._get_template()` 中添加模板内容

## 许可证

此技能是 skinsrv 项目文档系统的一部分。

## 另请参阅

- [docs/gotchas/README.md](../../README.md) - Gotchas 文档索引
- [docs/gotchas/bun-orm.md](../../bun-orm.md) - Bun ORM 问题和解决方案
- [docs/gotchas/code-quality.md](../../code-quality.md) - 代码质量问题和解决方案
