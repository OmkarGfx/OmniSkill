#!/usr/bin/env python3
"""
Keyword configuration for Gotcha Summarizer.

Centralizes all keyword definitions organized by domain → category → keywords.
Supports both English and Chinese keywords with weights for better classification.
"""

from typing import Dict, List, Tuple, Union

# Keyword configuration for three-layer decision tree
# Structure: domain → category → {keywords, filename, weights}
# Keywords can be:
#   - str: keyword with default weight (1.0)
#   - Tuple[str, float]: (keyword, weight) for custom weight
# Weights range from 0.1 to 3.0, where:
#   - 0.1-0.5: Weak indicator (context-dependent)
#   - 1.0: Normal weight (default)
#   - 1.5-2.0: Strong indicator
#   - 2.5-3.0: Very strong indicator (almost definitive)
KEYWORD_CONFIG: Dict[str, Dict[str, Dict[str, Union[List[Union[str, Tuple[str, float]]], str]]]] = {
    "frontend": {
        # Bug detection keywords - highest priority
        "bugs": {
            "keywords": [
                # High-weight indicators (definitive frontend bugs)
                ("hydration error", 2.5), ("hydration failed", 2.5), ("hydration mismatch", 2.5),
                ("cannot read property", 2.0), ("cannot read properties", 2.0),
                ("undefined is not", 2.0), ("null is not", 2.0),
                ("memory leak", 2.0), ("re-render", 1.5), ("rerender", 1.5),
                ("infinite loop", 2.0), ("infinite loop", 2.0),
                # React hooks issues
                ("useeffect dependency", 2.0), ("usememo", 1.5), ("usecallback", 1.5),
                # Chinese indicators
                ("组件", 1.0), ("渲染", 1.0), ("内存泄漏", 2.0), ("内存溢出", 1.5), ("死循环", 2.0),
                ("hook", 1.5), ("hooks", 1.5), ("lifecycle", 1.5), ("生命周期", 1.5),
                # Frontend-specific error indicators
                ("react error", 2.0), ("vue error", 2.0), ("next error", 2.0), ("nuxt error", 2.0),
                ("component error", 1.8), ("props error", 1.8), ("state error", 1.5),
                ("frontend bug", 2.5), ("frontend error", 2.5), ("ui bug", 2.0), ("ui error", 2.0),
                # Lower weight indicators (need context)
                ("typeerror", 1.0), ("referenceerror", 1.0), ("syntaxerror", 1.0),
                ("virtual dom", 1.0), ("virtualdom", 1.0),
                ("api route", 0.8), ("api route error", 1.5), ("next.js api", 1.2),
                ("cannot read", 1.2),
            ],
            "filename": "frontend/bugs.md",
        },

        # Framework keywords
        "frameworks": {
            "keywords": [
                # React
                "react", "react ", "jsx", "tsx", "usestate", "useeffect",
                "useref", "usecontext", "usereducer", "usecallback", "usememo",
                "next.js", "nextjs", "next.config", "app router", "pages router",
                "server component", "client component", "rsc", "react server",
                # Vue
                "vue", "vue3", "vue 3", "vue2", "vue 2",
                "composition api", "options api", "<script setup",
                "v-model", "v-if", "v-for", "v-bind", "v-on", "computed", "watch",
                "nuxt", "nuxt3", "nuxt 3", "nuxt.config",
                # Other frameworks
                "svelte", "sveltekit", "angular", "angular ",
                "solid", "solidjs", "preact", "qwik",
                # Component patterns
                "hoc", "higher order component", "render prop",
                "compound component", "controlled component",
            ],
            "filename": "frontend/frameworks.md",
        },

        # Styling keywords
        "styling": {
            "keywords": [
                "css", "css ", "css3", "scss", "sass", "less", "stylus",
                "tailwind", "tailwindcss", "unocss", "windicss",
                "styled-components", "styled components", "emotion", "@emotion",
                "css-in-js", "css modules", "css module",
                "flexbox", "flex ", "grid", "css grid",
                "z-index", "zindex", "z index", "position", "absolute", "relative",
                "responsive", "media query", "breakpoint", "media screen",
                "样式", "响应式", "断点", "布局",
                # CSS properties
                "display", "flex-direction", "justify-content", "align-items",
                "margin", "padding", "border", "background", "color",
                "font", "text-align", "line-height", "box-shadow",
                # CSS issues
                "css not working", "style not applied", "selector specificity",
                "!important", "css override", "css priority",
            ],
            "filename": "frontend/styling.md",
        },

        # Build tools keywords
        "build-tools": {
            "keywords": [
                "vite", "vite.config", "vite-plugin",
                "webpack", "webpack.config", "webpack plugin", "webpack loader",
                "rollup", "rollup.config", "rollup-plugin",
                "esbuild", "esbuild.config",
                "bundler", "bundling", "bundle size",
                "hmr", "hot module replacement", "hot reload",
                "tree-shaking", "tree shaking", "treeshake",
                "chunk", "code splitting", "split chunks",
                "minify", "minification", "uglify",
                "构建", "打包", "热更新", "分包",
            ],
            "filename": "frontend/build-tools.md",
        },

        # State management keywords
        "state-mgmt": {
            "keywords": [
                "redux", "redux toolkit", "rtk", "react-redux",
                "pinia", "vuex", "vue store", "vue store",
                "zustand", "jotai", "recoil", "mobx",
                "store", "state management", "状态管理",
                "dispatch", "action", "reducer", "selector",
                "usestore", "definestore", "createslice",
            ],
            "filename": "frontend/state-mgmt.md",
        },

        # UI component libraries keywords
        "ui-components": {
            "keywords": [
                "ant design", "antd", "ant-design",
                "element plus", "element-plus", "element-ui",
                "shadcn/ui", "shadcn ui", "shadcn",
                "material-ui", "material ui", "mui", "@mui",
                "chakra ui", "chakra-ui", "@chakra-ui",
                "arco design", "arco-design",
                "naive ui", "naive-ui",
                "vuetify", "primevue", "quasar",
                "radix", "radix-ui", "@radix-ui",
                "headless ui", "headless-ui",
                "组件库", "ui 组件",
            ],
            "filename": "frontend/ui-components.md",
        },
    },

    "backend": {
        # Bug detection keywords - highest priority
        "bugs": {
            "keywords": [
                "nil pointer", "null pointer", "segmentation fault",
                "index out of range", "out of bounds",
                "panic", "backend panic", "server panic",
                "sql error", "query error", "database error",
                "api error", "500 error", "404 error", "502 error",
                "backend error", "server error", "service error",
                "超时", "空指针", "内存溢出", "死锁",
                "stack overflow", "heap overflow", "out of memory",
                "segmentation fault", "core dump",
                # Note: race condition and deadlock are in concurrency category
            ],
            "filename": "backend/bugs.md",
        },

        # Database keywords
        "database": {
            "keywords": [
                "bun", "orm", "sql ", "sql(", "query", "group(", "column(",
                "order(", "join(", "relation", "scan(", "select(", "update(",
                "delete(", "cross-database", "pgx", "postgres", "postgresql",
                "migration", "database", "db.", "dao.", "model.", "schema",
                "gorm", "ent", "sqlx", "sqlc", "pg", "mysql", "sqlite",
                "数据库", "迁移", "表结构",
            ],
            "filename": "backend/database.md",
        },

        # API keywords
        "api": {
            "keywords": [
                "rest", "restful", "rest api", "restful api",
                "graphql", "gql", "apollo", "graphql ",
                "grpc", "gRPC", "protobuf", "protocol buffer",
                "endpoint", "api endpoint", "/api/", "/v1/",
                "controller", "handler", "router", "routing",
                "middleware", "interceptor",
                "request", "response", "payload",
                "openapi", "swagger", "api gateway",
                "接口", "路由", "中间件",
            ],
            "filename": "backend/api.md",
        },

        # Concurrency keywords
        "concurrency": {
            "keywords": [
                "goroutine", "go routine", "mutex", "lock", "unlock",
                "waitgroup", "errgroup", "sync.", "sync mutex",
                "channel", "chan ", "buffered channel", "unbuffered",
                "race", "race condition", "data race", "race detector",
                "deadlock", "context", "ctx ", "cancel", "timeout",
                "withtimeout", "withdeadline", "withcancel",
                "concurrent", "parallel", "async", "await",
                "goroutine leak", "channel leak",
                "并发", "锁", "竞态", "死锁", "协程",
            ],
            "filename": "backend/concurrency.md",
        },

        # Performance keywords
        "performance": {
            "keywords": [
                "cache", "redis", "memcached", "caching",
                "singleflight", "singleflight", "ttl", "invalidate",
                "缓存", "击穿", "雪崩", "穿透",
                "performance", "optimize", "optimization",
                "slow query", "slowlog", "index", "索引",
                "n+1", "n+1 query", "n+1 problem",
                "prefetch", "eager load", "lazy load",
                "connection pool", "pool", "连接池",
                "benchmark", "profiling", "pprof",
                "性能", "优化", "慢查询",
            ],
            "filename": "backend/performance.md",
        },

        # Precision keywords
        "precision": {
            "keywords": [
                "decimal", "decimal(", "float64", "float32", "precision",
                "money", "amount", "price", "cost", "fee",
                "numeric", "bigdecimal", "bigint",
                "shopspring", "shopspring/decimal",
                "财务", "金额", "精度", "精度丢失",
            ],
            "filename": "backend/precision.md",
        },
    },

    "common": {
        # Testing keywords
        "testing": {
            "keywords": [
                "test", "testing", "test(", "it(", "describe(",
                "table driven test", "table-driven test", "tdd",
                "mock", "mock(", "stub", "spy", "fake",
                "assert", "assert.", "assert(", "expect(", "should(",
                "testify", "go test", "jest", "vitest", "pytest",
                "integration test", "unit test", "e2e test",
                "coverage", "test coverage",
                "测试", "单元测试", "集成测试", "mock", "断言", "覆盖率",
            ],
            "filename": "common/testing.md",
        },

        # CI/CD keywords
        "cicd": {
            "keywords": [
                "ci/cd", "cicd", "ci/cd",
                "pipeline", "workflow", "github action", "github-action",
                "githubactions", "github actions",
                "jenkins", "jenkinsfile", "gitlab-ci", "gitlab-ci.yml",
                ".gitlab-ci.yml", "deploy ", "deployment ", "deployments",
                "docker build", "dockerfile", "docker-compose",
                "kubernetes", "k8s", "helm chart", "kustomize",
                "terraform ", "ansible ", "pulumi ",
                "持续集成", "持续部署", "流水线",
                # More specific build/deploy keywords to avoid false positives
                "build pipeline", "deploy pipeline", "release pipeline",
                "docker image", "container registry",
            ],
            "filename": "common/cicd.md",
        },

        # Git keywords
        "git": {
            "keywords": [
                "git ", "git commit", "git add", "git push",
                "commit", "branch", "merge", "merge conflict",
                "rebase", "cherry-pick", "cherry pick",
                "pull request", "pr ", "merge request",
                "push", "fetch", "clone", "remote",
                "conflict", "checkout", "stash", "reset",
                "gitignore", ".gitignore",
                "提交", "分支", "合并", "冲突", "变基",
            ],
            "filename": "common/git.md",
        },

        # Code quality keywords (catch-all for general development issues)
        "code-quality": {
            "keywords": [
                "refactor", "code smell", "anti-pattern", "antipattern",
                "clean code", "solid", "dry", "kiss", "yagni",
                "code review", "lint", "linter", "formatting",
                "type safety", "type hint", "type annotation",
                "error handling", "exception handling",
                "logging", "log level", "monitoring",
                "代码质量", "重构", "代码审查", "类型安全",
            ],
            "filename": "common/code-quality.md",
        },
    },
}

# Classification priority order for each domain
# Higher priority categories are checked first
DOMAIN_PRIORITIES: Dict[str, List[str]] = {
    "frontend": ["bugs", "state-mgmt", "frameworks", "styling", "build-tools", "ui-components"],
    "backend": ["bugs", "database", "concurrency", "api", "performance", "precision"],
    "common": ["testing", "cicd", "git", "code-quality"],
}

# Domain priority order (higher priority = checked first)
DOMAIN_ORDER: List[str] = ["common", "frontend", "backend"]


def get_all_keywords() -> Dict[str, List[str]]:
    """Get all keywords flattened by filename for backward compatibility."""
    result = {}
    for domain, categories in KEYWORD_CONFIG.items():
        for category, config in categories.items():
            filename = config["filename"]
            if filename not in result:
                result[filename] = []
            result[filename].extend(config["keywords"])
    return result


def get_keywords_for_domain(domain: str) -> Dict[str, List[str]]:
    """Get keywords for a specific domain."""
    return KEYWORD_CONFIG.get(domain, {})


def get_keywords_for_category(domain: str, category: str) -> List[Tuple[str, float]]:
    """
    Get keywords with weights for a specific category within a domain.

    Returns:
        List of (keyword, weight) tuples. Unweighted keywords default to 1.0.
    """
    raw_keywords = KEYWORD_CONFIG.get(domain, {}).get(category, {}).get("keywords", [])
    result = []
    for kw in raw_keywords:
        if isinstance(kw, tuple):
            result.append(kw)
        else:
            result.append((kw, 1.0))  # Default weight
    return result


def get_filename_for_category(domain: str, category: str) -> str:
    """Get the filename for a specific category within a domain."""
    return KEYWORD_CONFIG.get(domain, {}).get(category, {}).get("filename", "")


def get_categories_for_domain(domain: str) -> List[str]:
    """Get all categories for a specific domain in priority order."""
    return DOMAIN_PRIORITIES.get(domain, list(KEYWORD_CONFIG.get(domain, {}).keys()))
