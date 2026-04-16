#!/usr/bin/env python3
"""
Configuration constants for Gotcha Summarizer.

Defines path configurations, templates, and other constants.
"""

import os
from typing import Dict, Optional

# Timestamp format configuration
# Can be overridden by environment variable TIMESTAMP_FORMAT
DEFAULT_TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"
TIMESTAMP_FORMAT = os.environ.get("TIMESTAMP_FORMAT", DEFAULT_TIMESTAMP_FORMAT)

# Locale/language configuration
# Can be overridden by environment variable LOCALE (zh, en, etc.)
DEFAULT_LOCALE = "zh"
LOCALE = os.environ.get("LOCALE", DEFAULT_LOCALE)

# Logging configuration
# Can be overridden by environment variable LOG_LEVEL (DEBUG, INFO, WARNING, ERROR)
DEFAULT_LOG_LEVEL = "WARNING"
LOG_LEVEL = os.environ.get("LOG_LEVEL", DEFAULT_LOG_LEVEL)

# Error tracking configuration
# Enable detailed error logging when true
ENABLE_ERROR_TRACKING = os.environ.get("ENABLE_ERROR_TRACKING", "false").lower() == "true"

# Template definitions for markdown files
MARKDOWN_TEMPLATES: Dict[str, str] = {
    # Frontend templates
    "frontend/bugs.md": """# 前端 Bug 记录

> 记录前端开发中的 Bug 和解决方案，包括 React/Vue/Next.js/Nuxt 等框架问题。

## 问题示例
""",
    "frontend/frameworks.md": """# 前端框架踩坑经验记录

> 记录前端框架相关问题和解决方案，包括 React/Vue/Next.js/Nuxt/Svelte/Angular 等。

## 问题示例
""",
    "frontend/styling.md": """# 前端样式踩坑经验记录

> 记录 CSS/SCSS/Tailwind/UnoCSS 等样式相关问题和解决方案。

## 问题示例
""",
    "frontend/build-tools.md": """# 前端构建工具踩坑经验记录

> 记录 Vite/Webpack/Rollup/esbuild 等构建工具相关问题和解决方案。

## 问题示例
""",
    "frontend/state-mgmt.md": """# 前端状态管理踩坑经验记录

> 记录 Redux/Pinia/Zustand/Jotai/Vuex 等状态管理相关问题和解决方案。

## 问题示例
""",
    "frontend/ui-components.md": """# UI 组件库踩坑经验记录

> 记录 Ant Design/Element Plus/shadcn/ui/Material-UI 等组件库相关问题和解决方案。

## 问题示例
""",

    # Backend templates
    "backend/bugs.md": """# 后端 Bug 记录

> 记录后端开发中的 Bug 和解决方案。

## 问题示例
""",
    "backend/database.md": """# 数据库踩坑经验记录

> 记录数据库 ORM、SQL 查询、迁移等相关问题和解决方案。

## 问题示例
""",
    "backend/api.md": """# API 踩坑经验记录

> 记录 REST/GraphQL/gRPC 等 API 相关问题和解决方案。

## 问题示例
""",
    "backend/concurrency.md": """# 并发踩坑经验记录

> 记录 goroutine/mutex/channel/context 等并发相关问题和解决方案。

## 问题示例
""",
    "backend/performance.md": """# 性能踩坑经验记录

> 记录缓存、索引、优化等性能相关问题和解决方案。

## 问题示例
""",
    "backend/precision.md": """# 精度踩坑经验记录

> 记录 decimal/float64 等数据类型精度相关问题和解决方案。

## 问题示例
""",

    # Common templates
    "common/testing.md": """# 测试踩坑经验记录

> 记录单元测试、集成测试、TDD 等测试相关的问题和解决方案。

## 问题示例
""",
    "common/cicd.md": """# CI/CD 踩坑经验记录

> 记录持续集成、持续部署、流水线配置等问题和解决方案。

## 问题示例
""",
    "common/git.md": """# Git 踩坑经验记录

> 记录 Git 版本控制、分支管理、合并冲突等问题和解决方案。

## 问题示例
""",
    "common/code-quality.md": """# 代码质量踩坑经验记录

> 记录代码审查和重构过程中发现的通用问题及解决方案。

## 问题示例
""",
}

# Default template for unknown files
DEFAULT_TEMPLATE = """# {title}

> 自动生成的技术问题记录。

## 问题示例
"""


def get_template(filename: str) -> str:
    """Get template content for a given filename."""
    template = MARKDOWN_TEMPLATES.get(filename)
    if template:
        return template

    # Generate default template
    title = filename.replace("-", " ").replace(".md", "").title()
    return DEFAULT_TEMPLATE.format(title=title)


# Internationalization labels
I18N_LABELS: Dict[str, Dict[str, str]] = {
    "zh": {
        "problem_title": "问题",
        "auto_generated_time": "自动生成时间",
        "error_info": "错误信息",
        "related_code": "相关代码",
        "problem_description": "问题描述",
        "root_cause": "根本原因",
        "solution": "解决方案",
        "best_practices": "最佳实践清单",
        "problem_example": "问题示例",
    },
    "en": {
        "problem_title": "Issue",
        "auto_generated_time": "Auto-generated time",
        "error_info": "Error Information",
        "related_code": "Related Code",
        "problem_description": "Problem Description",
        "root_cause": "Root Cause",
        "solution": "Solution",
        "best_practices": "Best Practices Checklist",
        "problem_example": "Problem Examples",
    },
}


def get_label(key: str, locale: Optional[str] = None) -> str:
    """Get a localized label by key."""
    loc = locale or LOCALE
    labels = I18N_LABELS.get(loc, I18N_LABELS[DEFAULT_LOCALE])
    return labels.get(key, key)
