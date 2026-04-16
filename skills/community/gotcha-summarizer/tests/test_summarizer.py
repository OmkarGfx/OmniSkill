#!/usr/bin/env python3
"""
Unit tests for Gotcha Summarizer.

Test suite covering:
- Structured extraction
- Language detection (18 languages)
- Fuzzy matching
- Markdown formatting
- Classification accuracy
- Error handling
- Edge cases
"""

import os
import re
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.classifier import (
    DomainClassifier,
    CategoryClassifier,
    FileMapper,
    ThreeLayerTopicClassifier,
    TopicClassifier,
)
from scripts.config import (
    get_template,
    get_label,
    TIMESTAMP_FORMAT,
    LOCALE,
)
from scripts.summarize import (
    GotchaExtractor,
    MarkdownFormatter,
    GotchaFileManager,
    find_conversation_history,
    load_conversation_history,
)


# ============ Test Data ============

SAMPLE_CONVERSATION = [
    {
        "role": "assistant",
        "content": """
Error: hydration failed because the server-rendered HTML doesn't match the client-side render.

Problem: React hydration mismatch when using useEffect
Cause: Missing dependency array in useEffect hook
Solution: Add proper dependencies to useEffect array

Best practices:
- Always include all dependencies in useEffect
- Use ESLint react-hooks plugin to catch missing dependencies

```go
// Error example
func main() {
    var data []string
    // Missing nil check
    for _, item := range data {
        fmt.Println(item)
    }
}
```

```javascript
const App = () => {
    return <div className="app">Hello</div>;
};
```
        """
    },
    {
        "role": "user",
        "content": "I'm getting a TypeError: Cannot read property of undefined"
    }
]


# ============ Test: Structured Extraction ============

class TestStructuredExtraction:
    """Test structured field extraction from conversation content."""

    def test_extract_errors(self):
        """Test error message extraction."""
        extractor = GotchaExtractor(SAMPLE_CONVERSATION)
        lessons = extractor.extract_lessons()
        assert len(lessons) > 0
        assert "hydration failed" in lessons[0]["errors"][0].lower()

    def test_extract_problems(self):
        """Test problem description extraction."""
        extractor = GotchaExtractor(SAMPLE_CONVERSATION)
        lessons = extractor.extract_lessons()
        assert len(lessons) > 0
        assert len(lessons[0]["problems"]) > 0
        assert "react" in lessons[0]["problems"][0].lower()

    def test_extract_causes(self):
        """Test root cause extraction."""
        extractor = GotchaExtractor(SAMPLE_CONVERSATION)
        lessons = extractor.extract_lessons()
        assert len(lessons) > 0
        assert len(lessons[0]["causes"]) > 0
        assert "dependency" in lessons[0]["causes"][0].lower()

    def test_extract_solutions(self):
        """Test solution extraction."""
        extractor = GotchaExtractor(SAMPLE_CONVERSATION)
        lessons = extractor.extract_lessons()
        assert len(lessons) > 0
        assert len(lessons[0]["solutions"]) > 0

    def test_extract_code_blocks(self):
        """Test code block extraction."""
        extractor = GotchaExtractor(SAMPLE_CONVERSATION)
        lessons = extractor.extract_lessons()
        assert len(lessons) > 0
        code_blocks = lessons[0]["code_blocks"]
        assert len(code_blocks) >= 2  # Go and JavaScript

    def test_extract_practices(self):
        """Test best practices extraction."""
        extractor = GotchaExtractor(SAMPLE_CONVERSATION)
        lessons = extractor.extract_lessons()
        assert len(lessons) > 0
        assert len(lessons[0]["practices"]) > 0

    def test_empty_conversation(self):
        """Test handling of empty conversation."""
        extractor = GotchaExtractor([])
        lessons = extractor.extract_lessons()
        assert len(lessons) == 0


# ============ Test: Language Detection (18 Languages) ============

class TestLanguageDetection:
    """Test programming language detection for 18+ languages."""

    @pytest.fixture
    def test_cases(self):
        """Comprehensive test cases for language detection."""
        return [
            # Original 9 languages
            ('func main() { fmt.Println("hello") }', 'go'),
            ('def hello(): print("world")', 'python'),
            ('const x = () => { return 1; }', 'javascript'),
            ('interface User { name: string; }', 'typescript'),
            ('SELECT * FROM users WHERE id = 1', 'sql'),
            ('#!/bin/bash\necho "test"', 'bash'),
            ('<template><div>{{ message }}</div></template>', 'vue'),
            ('function App() { return <div className="app">Hello</div>; }', 'jsx'),
            ('import React from "react"; function App() { return <div>Hello</div>; }', 'jsx'),
            # New languages
            ('<?php\necho "Hello World";', 'php'),
            ('def hello\n  puts "world"\nend', 'ruby'),
            ('func greet() -> String { return "Hello" }', 'swift'),
            ('fun greet(): String = "Hello"', 'kotlin'),
            ('public class Program { public static void Main() {} }', 'csharp'),
            ('void main() { print("Hello"); }', 'dart'),
            ('SELECT * FROM table', 'sql'),  # SQL still works
            ('import SwiftUI\nstruct ContentView: View {}', 'swift'),
            ('@Composable fun App() {}', 'kotlin'),
            ('using System;\nclass Program {}', 'csharp'),
            ('// Dart code\nmain() { print("Hi"); }', 'dart'),
            ('#[derive(Debug)]\nstruct Point;', 'rust'),
            ('use std::collections::HashMap;', 'rust'),
            ('#include <iostream>\nint main() {}', 'cpp'),
            ('#include <stdio.h>\nint main() { return 0; }', 'c'),
            ('$ErrorActionPreference = "Stop"', 'powershell'),
            ('Write-Host "Hello"', 'powershell'),
        ]

    @pytest.fixture
    def formatter(self):
        return MarkdownFormatter()

    def test_all_languages(self, formatter, test_cases):
        """Test all 18+ programming languages."""
        passed = 0
        failed = []
        for code, expected in test_cases:
            detected = formatter._detect_code_language([{"lang": "", "code": code}])
            if detected == expected:
                passed += 1
            else:
                failed.append((code[:30], expected, detected))

        print(f"\nLanguage Detection: {passed}/{len(test_cases)} passed")
        if failed:
            print("Failed cases:")
            for code, expected, detected in failed:
                print(f"  '{code}...' -> expected {expected}, got {detected}")

        # At least 90% pass rate
        assert passed / len(test_cases) >= 0.9

    def test_jsx_before_sql_priority(self, formatter):
        """Test JSX patterns are checked before SQL to avoid 'from' confusion."""
        # This should be detected as JSX, not SQL (due to "from")
        code = 'import React from "react"; function App() { return <div>Hello</div>; }'
        detected = formatter._detect_code_language([{"lang": "", "code": code}])
        assert detected == "jsx"

    def test_sql_detection(self, formatter):
        """Test SQL detection still works correctly."""
        code = 'SELECT id, name FROM users WHERE active = true'
        detected = formatter._detect_code_language([{"lang": "", "code": code}])
        assert detected == "sql"

    def test_unknown_language(self, formatter):
        """Test unknown language defaults to 'text'."""
        code = 'This is just plain text without code'
        detected = formatter._detect_code_language([{"lang": "", "code": code}])
        assert detected == "text"


# ============ Test: Fuzzy Matching ============

class TestFuzzyMatching:
    """Test fuzzy duplicate detection."""

    @pytest.fixture
    def file_manager(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            return GotchaFileManager(Path(tmpdir))

    def test_similar_content_detected(self, file_manager):
        """Test similar content is detected as duplicate."""
        existing = "hydration failed because the server-rendered html doesn't match"
        new_text = "Hydration failed - server HTML mismatch issue"

        assert file_manager._fuzzy_match(
            file_manager._normalize_text(new_text),
            file_manager._normalize_text(existing),
            threshold=0.75
        )

    def test_different_content_not_duplicate(self, file_manager):
        """Test different content is not detected as duplicate."""
        existing = "hydration failed because the server-rendered html doesn't match"
        different = "TypeError: Cannot read property of undefined in React component"

        assert not file_manager._fuzzy_match(
            file_manager._normalize_text(different),
            file_manager._normalize_text(existing),
            threshold=0.75
        )

    def test_normalize_text(self, file_manager):
        """Test text normalization removes formatting."""
        text = "```python\ncode here\n```\n\n  Extra  spaces\n2024-01-01"
        normalized = file_manager._normalize_text(text)
        assert "```" not in normalized
        assert "extra spaces" in normalized
        assert "2024" not in normalized  # Dates removed

    def test_normalize_code(self, file_manager):
        """Test code normalization removes comments."""
        code = "const x = 1; // inline comment\n/* block comment */"
        normalized = file_manager._normalize_code(code)
        assert "//" not in normalized
        assert "/*" not in normalized
        assert "const x = 1" in normalized.lower()


# ============ Test: Markdown Formatting ============

class TestMarkdownFormatting:
    """Test markdown output formatting."""

    @pytest.fixture
    def sample_lesson(self):
        return {
            "errors": ["Hydration failed: server HTML mismatch"],
            "problems": ["React hydration error in useEffect"],
            "causes": ["Missing dependency in useEffect causes stale closure"],
            "solutions": ["Add all dependencies to useEffect array"],
            "practices": ["Use ESLint react-hooks plugin", "Always include dependencies"],
            "code_blocks": [
                {"lang": "jsx", "code": "const App = () => { return <div>Hello</div>; };"}
            ],
            "content_preview": "Test content",
        }

    def test_format_lesson_sections(self, sample_lesson):
        """Test all required sections are present."""
        formatter = MarkdownFormatter()
        md = formatter.format_lesson(sample_lesson, "Frontend Bugs")

        required_sections = [
            "## 问题：",
            "> **自动生成时间**",
            "### 错误信息",
            "### 相关代码",
            "### 问题描述",
            "### 根本原因",
            "### 解决方案",
            "### 最佳实践清单",
            "---",
        ]
        for section in required_sections:
            assert section in md, f"Missing section: {section}"

    def test_format_lesson_with_locale(self, sample_lesson):
        """Test formatting with English locale."""
        formatter = MarkdownFormatter()
        md = formatter.format_lesson(sample_lesson, "Frontend Bugs", locale="en")

        # Should use English labels
        assert "## Issue:" in md
        assert "Auto-generated time" in md
        assert "Error Information" in md

    def test_format_lesson_multiple_code_blocks(self):
        """Test formatting multiple code blocks in different languages."""
        lesson = {
            "code_blocks": [
                {"lang": "jsx", "code": "const App = () => <div />;"},
                {"lang": "go", "code": "func main() {}"},
            ],
            "errors": ["Test error"],
        }
        formatter = MarkdownFormatter()
        md = formatter.format_lesson(lesson, "Test")

        # Should have language headers for multiple languages
        assert "#### JSX" in md or "#### GO" in md or "####" in md

    def test_format_lesson_fallback_content(self):
        """Test fallback to content_preview when no structured data."""
        lesson = {
            "content_preview": "This is a test problem that needs documentation.",
        }
        formatter = MarkdownFormatter()
        md = formatter.format_lesson(lesson, "Test")

        assert "### 问题描述" in md
        assert "test problem" in md.lower()


# ============ Test: Classification ============

class TestClassification:
    """Test three-layer classification system."""

    @pytest.fixture
    def classifier(self):
        return ThreeLayerTopicClassifier(enable_logging=False)

    def test_frontend_classification(self, classifier):
        """Test frontend domain classification."""
        lesson = {
            "errors": ["React hydration error"],
            "content_preview": "The React component has a hydration mismatch issue.",
        }
        category, filename, domain, confidence = classifier.classify(lesson)
        assert domain == "frontend"
        assert "frontend" in filename.lower()

    def test_backend_classification(self, classifier):
        """Test backend domain classification."""
        lesson = {
            "errors": ["SQL query timeout"],
            "content_preview": "The database query is timing out.",
        }
        category, filename, domain, confidence = classifier.classify(lesson)
        assert domain == "backend"
        assert "backend" in filename.lower()

    def test_common_classification(self, classifier):
        """Test common domain classification."""
        lesson = {
            "errors": ["Git merge conflict"],
            "content_preview": "Having issues with git merge.",
        }
        category, filename, domain, confidence = classifier.classify(lesson)
        assert domain == "common"

    def test_confidence_scores(self, classifier):
        """Test classification returns confidence scores."""
        lesson = {
            "errors": ["React error"],
            "content_preview": "React hydration failed",
        }
        category, filename, domain, confidence = classifier.classify(lesson)

        assert "domain" in confidence
        assert "category" in confidence
        assert "max_score" in confidence["domain"]
        assert "max_score" in confidence["category"]


# ============ Test: Configuration ============

class TestConfiguration:
    """Test configuration and internationalization."""

    def test_get_template(self):
        """Test template retrieval."""
        template = get_template("frontend/bugs.md")
        assert "前端 Bug 记录" in template
        assert "问题示例" in template

    def test_get_template_unknown_file(self):
        """Test template for unknown file generates default."""
        template = get_template("unknown/test.md")
        assert "# Test" in template

    def test_get_label_chinese(self):
        """Test Chinese label retrieval."""
        label = get_label("problem_title", "zh")
        assert label == "问题"

    def test_get_label_english(self):
        """Test English label retrieval."""
        label = get_label("problem_title", "en")
        assert label == "Issue"

    def test_get_label_fallback(self):
        """Test fallback to default locale."""
        label = get_label("problem_title", "fr")  # French not supported
        # Should fall back to default (zh)
        assert label == "问题"


# ============ Test: Error Handling ============

class TestErrorHandling:
    """Test error handling and edge cases."""

    def test_empty_conversation_history(self):
        """Test handling empty conversation history."""
        history = load_conversation_history(None)
        assert history == []

    def test_nonexistent_file(self):
        """Test handling of nonexistent file."""
        history = load_conversation_history(Path("/nonexistent/file.jsonl"))
        assert history == []

    def test_minimal_length_check(self):
        """Test minimum length check for classification."""
        classifier = ThreeLayerTopicClassifier()
        # Very short content should still classify (to common)
        lesson = {"content_preview": "bug", "errors": []}
        category, filename, domain, _ = classifier.classify(lesson)
        assert domain  # Should not crash


# ============ Test: Edge Cases ============

class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_very_long_title(self):
        """Test handling of very long titles."""
        long_problem = "x" * 100
        lesson = {
            "problems": [long_problem],
            "errors": [],
        }
        formatter = MarkdownFormatter()
        md = formatter.format_lesson(lesson, "Test")
        # Title should be truncated
        assert "..." in md

    def test_special_characters_in_content(self):
        """Test handling special characters."""
        lesson = {
            "errors": ["Error: <script>alert('xss')</script>"],
            "problems": ["Issue with & < > characters"],
            "content_preview": "Test <>&\"'",
        }
        extractor = GotchaExtractor([])
        # Should not crash
        assert extractor._extract_lesson_from_content(lesson["content_preview"]) is None

    def test_unicode_content(self):
        """Test handling of Unicode content."""
        lesson = {
            "errors": ["错误：中文错误信息"],
            "problems": ["问题描述"],
            "content_preview": "测试中文内容",
        }
        formatter = MarkdownFormatter()
        md = formatter.format_lesson(lesson, "Test")
        assert "错误" in md or "问题" in md


# ============ Run Tests ============

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
