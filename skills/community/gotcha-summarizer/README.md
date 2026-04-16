# Gotcha Summarizer Skill

Automatically summarizes technical lessons learned from Claude Code conversations into structured markdown documentation.

## Overview

This skill analyzes conversation history to extract:

**Frontend Development:**
- Frontend bugs and root causes (hydration errors, memory leaks, rendering issues)
- Framework issues (React, Vue, Next.js, Nuxt, Svelte, Angular)
- Styling problems (CSS, SCSS, Tailwind, UnoCSS)
- Build tool issues (Vite, Webpack, Rollup, esbuild)
- State management (Redux, Pinia, Zustand, Jotai, Vuex)
- UI component library issues (Ant Design, Element Plus, shadcn/ui)

**Backend Development:**
- Backend bugs and root causes (nil pointer, race conditions, database errors)
- Database/ORM issues (SQL, migrations, Bun, GORM, Ent, sqlx)
- API issues (REST, GraphQL, gRPC, endpoints, controllers)
- Concurrency issues (goroutines, mutexes, channels, context)
- Performance issues (caching, Redis, slow queries, indexing)
- Precision issues (decimal vs float, money/amount handling)

**Common Development:**
- Testing problems and solutions (unit tests, integration tests, mocks)
- CI/CD pipeline issues (GitHub Actions, Docker, deployment)
- Git/version control problems (merge conflicts, rebasing, branches)
- Code quality improvements (refactoring, design patterns)
- Any technical lessons worth documenting

## Installation

The skill is installed at `~/.claude/skills/gotcha-summarizer/`.

## Usage

### Basic Usage

```bash
# Run from anywhere to analyze the latest conversation
python3 ~/.claude/skills/gotcha-summarizer/scripts/summarize.py

# Or use the shell wrapper
~/.claude/skills/gotcha-summarizer/scripts/gotcha-summarize.sh
```

### With Claude Code Skill Command

```
skill gotcha-summarizer
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GOTCHAS_DIR` | `./docs/gotchas` | Path to docs/gotchas directory |
| `CLAUDE_HISTORY_PATH` | Auto-detected | Path to conversation history file |
| `DRY_RUN` | `false` | Set to `true` to preview changes without writing |
| `TIMESTAMP_FORMAT` | `%Y-%m-%d %H:%M:%S` | Format for timestamps in generated markdown |
| `LOCALE` | `zh` | Interface language (`zh` for Chinese, `en` for English) |
| `LOG_LEVEL` | `WARNING` | Logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`) |
| `ENABLE_ERROR_TRACKING` | `false` | Enable detailed error tracking and statistics |

### Examples

```bash
# Preview changes without writing
DRY_RUN=true python3 ~/.claude/skills/gotcha-summarizer/scripts/summarize.py

# Specify custom gotchas directory
GOTCHAS_DIR=/path/to/docs/gotchas python3 ~/.claude/skills/gotcha-summarizer/scripts/summarize.py

# Use specific conversation history
CLAUDE_HISTORY_PATH=/path/to/history.jsonl python3 ~/.claude/skills/gotcha-summarizer/scripts/summarize.py
```

## How It Works

### 1. Conversation Analysis

The skill reads the Claude Code conversation history (JSONL format) and analyzes messages for:
- Error messages
- Code blocks (with automatic language detection for 18+ languages)
- Problem/solution patterns
- Root causes
- Best practices
- Technical discussions

### 2. Topic Classification (with Confidence Scores)

Using a three-layer decision tree, the skill classifies each lesson:

**Layer 1: Domain Classification** (Common / Frontend / Backend)
- Minimum text length check (20 characters)
- Weighted keyword scoring
- Confidence score output

**Layer 2: Category Classification** (e.g., Bugs, Framework, Database, API)
- Domain-specific category scoring
- Minimum length check (15 characters)
- Confidence score output

**Layer 3: File Mapping** (Category → markdown file)

```
START: Analyze conversation for technical issues
│
├─ LAYER 1: Domain Classification
│   │
│   ├─ COMMON (Testing, CI/CD, Git) → common/
│   ├─ FRONTEND (React, Vue, CSS, etc.) → frontend/
│   └─ BACKEND (SQL, API, Goroutines, etc.) → backend/
│
├─ LAYER 2: Category Classification
│   │
│   ├─ Bugs (highest priority)
│   ├─ Framework / Database / Testing (domain-specific)
│   └─ Other categories (styling, build tools, state mgmt, etc.)
│
└─ LAYER 3: File Mapping
    └─ frontend/bugs.md, backend/database.md, common/git.md, etc.
```

### 3. Duplicate Detection

Before adding new content, the skill:
- Reads all existing gotcha files
- Checks for similar titles (fuzzy matching)
- Checks for similar error messages
- Skips adding if a duplicate is detected (with warning)

### 4. Markdown Generation

The skill generates markdown sections following this format:

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

## Output Files

The skill updates files in the `docs/gotchas/` directory:

| Domain | File | Category | Examples |
|--------|------|----------|----------|
| **Frontend** | `frontend/bugs.md` | Frontend Bugs | Hydration errors, memory leaks, re-render issues |
| | `frontend/frameworks.md` | Frameworks | React, Vue, Next.js, Nuxt, Svelte, Angular |
| | `frontend/styling.md` | Styling | CSS, SCSS, Tailwind, UnoCSS, styled-components |
| | `frontend/build-tools.md` | Build Tools | Vite, Webpack, Rollup, esbuild, HMR |
| | `frontend/state-mgmt.md` | State Mgmt | Redux, Pinia, Zustand, Jotai, Vuex |
| | `frontend/ui-components.md` | UI Components | Ant Design, Element Plus, shadcn/ui, MUI |
| **Backend** | `backend/bugs.md` | Backend Bugs | Nil pointer, race conditions, SQL errors |
| | `backend/database.md` | Database | SQL, ORM (Bun, GORM, Ent), migrations |
| | `backend/api.md` | API | REST, GraphQL, gRPC, endpoints, controllers |
| | `backend/concurrency.md` | Concurrency | Goroutines, mutexes, channels, context |
| | `backend/performance.md` | Performance | Caching (Redis), slow queries, indexing, n+1 |
| | `backend/precision.md` | Precision | Decimal vs float, money/amount handling |
| **Common** | `common/testing.md` | Testing | Unit tests, integration tests, mocks, TDD |
| | `common/cicd.md` | CI/CD | GitHub Actions, Docker, Kubernetes, deployment |
| | `common/git.md` | Git | Merge conflicts, rebasing, branch management |
| | `common/code-quality.md` | Code Quality | Refactoring, design patterns, linting |

## Integration with Session End

To automatically run this skill at the end of conversations, you can set up a session-end hook in your Claude Code configuration (if supported).

## Troubleshooting

### No technical issues found

If the skill doesn't detect any technical issues:
- Ensure the conversation contains error messages, code examples, or problem-solving discussions
- Try manually triggering the skill with explicit instructions about what to document

### Duplicate entries

The skill attempts to detect duplicates, but may occasionally create similar entries. Review the generated content and merge or remove duplicates as needed.

### File permission errors

Ensure the `docs/gotchas/` directory is writable:
```bash
chmod +w docs/gotchas/*.md
```

## Development

### Script Structure

```
gotcha-summarizer/
├── SKILL.md                    # Skill definition and frontmatter
├── README.md                   # This file
├── pytest.ini                  # Pytest configuration
├── test_features.py            # Quick inline test script
└── scripts/
    ├── __init__.py             # Package initialization
    ├── summarize.py            # Main Python script
    ├── classifier.py           # Three-layer topic classifier
    ├── keywords.py             # Keyword configuration (weighted)
    └── config.py               # Configuration constants & templates
└── tests/
    ├── __init__.py             # Test package
    └── test_summarizer.py      # Pytest test suite
```

### Python Script Components

- `GotchaExtractor` - Extracts lessons from conversation history with structured field extraction
- `ThreeLayerTopicClassifier` - Three-layer classification with confidence scores
- `TopicClassifier` - Backward-compatible wrapper for ThreeLayerTopicClassifier
- `DomainClassifier` - Layer 1: Domain classification with weighted scoring
- `CategoryClassifier` - Layer 2: Category classification with weighted scoring
- `FileMapper` - Layer 3: Maps categories to file paths
- `MarkdownFormatter` - Formats lessons as markdown with i18n support
- `GotchaFileManager` - Manages reading/writing markdown files with error tracking

### Running Tests

```bash
# Quick inline test (no dependencies)
python3 test_features.py

# Full pytest suite (requires pytest)
pip install pytest
pytest tests/test_summarizer.py -v

# With coverage
pip install pytest-cov
pytest tests/test_summarizer.py --cov=scripts --cov-report=html
```

### New Features (Latest Version)

1. **Structured Extraction** - Extracts problems, causes, solutions, and best practices
2. **Multi-Language Code Detection** - Supports 18+ programming languages:
   - JSX/TSX, SQL, Vue, Bash, PowerShell, PHP, Ruby, Swift, Kotlin, C#, Dart, Rust, Go, Python, TypeScript, Java, JavaScript, C, C++
3. **Multi-Code Block Support** - Groups and displays code blocks by language
4. **Confidence Scores** - Classification returns confidence metrics
5. **Error Tracking** - Tracks JSON parse errors, file I/O errors, classification errors
6. **Configurable Timestamp Format** - Customize via `TIMESTAMP_FORMAT` env var
7. **Internationalization** - Chinese/English labels, configurable via `LOCALE` env var
8. **Improved Fuzzy Matching** - Lowered threshold (0.75) for better duplicate detection

## Contributing

To extend the skill with new categories:

1. Add keywords to `TopicClassifier` for the new category
2. Create a new markdown file in `docs/gotchas/`
3. Update the decision tree in `SKILL.md`
4. Add template content in `GotchaFileManager._get_template()`

## License

This skill is part of the skinsrv project documentation system.

## See Also

- [docs/gotchas/README.md](../../README.md) - Gotchas documentation index
- [docs/gotchas/bun-orm.md](../../bun-orm.md) - Bun ORM issues and solutions
- [docs/gotchas/code-quality.md](../../code-quality.md) - Code quality issues and solutions
