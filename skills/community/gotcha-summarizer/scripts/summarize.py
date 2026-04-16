#!/usr/bin/env python3
"""
Gotcha Summarizer Script

Analyzes Claude Code conversation history to extract technical lessons learned
and updates the appropriate markdown files in docs/gotchas/.
"""

import argparse
import difflib
import json
import logging
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Import the new three-layer classifier
from .classifier import ThreeLayerTopicClassifier
from .config import (
    get_template,
    get_label,
    TIMESTAMP_FORMAT,
    LOCALE,
    LOG_LEVEL,
    ENABLE_ERROR_TRACKING,
)

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Error tracking statistics
error_stats = {
    "json_parse_errors": 0,
    "file_read_errors": 0,
    "file_write_errors": 0,
    "classification_errors": 0,
    "total_entries_processed": 0,
}


class GotchaExtractor:
    """Extracts technical lessons from conversation history."""

    def __init__(self, conversation_history: List[Dict]):
        self.history = conversation_history

    def extract_lessons(self) -> List[Dict]:
        """Extract all technical lessons from the conversation."""
        lessons = []

        for entry in self.history:
            role = entry.get("role", "")
            content = entry.get("content", "")

            # Focus on assistant responses and tool results
            if role in ["assistant", "user"]:
                lesson = self._extract_lesson_from_content(content)
                if lesson:
                    lessons.append(lesson)

        return lessons

    def _extract_lesson_from_content(self, content: str) -> Optional[Dict]:
        """Extract a single lesson from content with structured fields."""
        # Look for error messages - more specific pattern
        error_pattern = r'(?:ERROR|Error|error|❌)[:\s]+([^\n`]+)'
        errors = re.findall(error_pattern, content)

        # Look for code blocks with language detection
        code_blocks = re.findall(r'```(\w*)\n(.*?)```', content, re.DOTALL)

        # Look for problem patterns - more specific, avoid matching code blocks
        problem_patterns = [
            r'(?m)^(?:问题|Problem|Issue)[:\s]+([^\n]+)',  # Line start, more specific
            r'(?i)(?:(?:问题|Problem|Issue)[:\s]\s*)([A-Z][^.!?]*(?:error|issue|bug|problem))',
        ]
        problems = []
        for pattern in problem_patterns:
            problems.extend(re.findall(pattern, content))

        # Look for root cause patterns - more specific
        cause_patterns = [
            r'(?m)^(?:原因|Cause|Reason|根本原因)[:\s]+([^\n]+)',  # Line start only
            r'(?i)(?:because|due to|caused by)[:\s]+([^\n.]+)',  # Standalone phrases
        ]
        causes = []
        for pattern in cause_patterns:
            causes.extend(re.findall(pattern, content))

        # Look for solution patterns - more specific
        solution_patterns = [
            r'(?m)^(?:解决|Solution|Fix|解决方案)[:\s]+([^\n]+)',  # Line start
            r'(?i)(?:the\s+)?(?:solution|fix|answer)[:\s]+(?:is\s+)?([^\n.]+)',  # More specific
        ]
        solutions = []
        for pattern in solution_patterns:
            solutions.extend(re.findall(pattern, content))

        # Look for best practice patterns - more specific
        practice_patterns = [
            r'(?:最佳实践|Best Practice|Checklist|清单)[:\s]+([^\n]+(?:\n\s*[-–•]\s*[^\n]+)*)',  # Include list items
        ]
        practices = []
        for pattern in practice_patterns:
            practices.extend(re.findall(pattern, content, re.IGNORECASE))

        # Only return if we found something meaningful
        if errors or code_blocks or problems or solutions or causes:
            return {
                "errors": errors,
                "code_blocks": [{"lang": lang or "text", "code": code} for lang, code in code_blocks],
                "problems": problems,
                "causes": causes,
                "solutions": solutions,
                "practices": practices,
                "content_preview": content[:500] if len(content) > 500 else content,
            }

        return None


class TopicClassifier(ThreeLayerTopicClassifier):
    """
    Wrapper for ThreeLayerTopicClassifier for backward compatibility.

    The old TopicClassifier has been replaced with a three-layer decision tree:
    Layer 1: Domain (Frontend/Backend/Common)
    Layer 2: Category (e.g., Bugs/Framework/Database)
    Layer 3: File Path

    This class maintains the same interface as the old TopicClassifier.
    """


class MarkdownFormatter:
    """Formats lessons into markdown following the gotchas template."""

    @staticmethod
    def _detect_code_language(code_blocks: List[Dict]) -> str:
        """
        Detect programming language from code blocks.

        Returns the most common language across all code blocks.
        """
        if not code_blocks:
            return "text"

        # Count language occurrences
        lang_counts: Dict[str, int] = {}
        total_code = ""

        for code_block in code_blocks:
            # Use the language from code block if available
            lang = code_block.get("lang", "text")
            if lang and lang != "text":
                lang_counts[lang] = lang_counts.get(lang, 0) + 1

            # Accumulate code for detection
            code = code_block.get("code", "")
            total_code += " " + code

        # If we have detected languages, return the most common
        if lang_counts:
            return max(lang_counts, key=lang_counts.get)

        # Try to detect from accumulated content
        if not total_code:
            return "text"

        code_lower = total_code.lower()

        # Language-specific patterns - ORDER MATTERS! More specific patterns first.
        # List of (language, patterns) tuples in priority order
        patterns = [
            # High-specificity patterns (check FIRST) - JSX before SQL to avoid "from" confusion
            ("jsx", ["jsx", "react.dom", "react.createelement", " from \"react\"", " from 'react'", " classname=", "<div ", "<span ", "<button "]),
            ("tsx", ["tsx", "react.fc", ": react.", "react.reactelement", "<>"]),
            ("sql", ["select ", " from ", " where ", " insert into", " update ", " delete ", " join ", " group by"]),
            ("vue", ["<template>", "<script ", "<style ", "v-model", "v-if", "v-for", "v-bind", "v-on"]),
            ("php", ["<?php", "$_get", "$_post", "public function", "private function", "->", "namespace ", "use "]),
            ("ruby", ["def ", "class ", "module ", "attr_accessor", "require '", "include ", "puts ", "each do"]),
            ("swift", ["func ", "var ", "let ", "struct ", "class ", "protocol ", "extension ", "@escaping", "import uikit"]),
            ("kotlin", ["fun ", "val ", "var ", "class ", "interface ", "object :", "import ", "println("]),
            ("csharp", ["public class", "private ", "public ", "namespace ", "using ", "string ", "int ", "var ", ".select("]),
            ("dart", ["import 'dart:", "class ", "extends ", "implements ", "final ", "const ", "void main(", "print("]),
            ("bash", ["#!/bin/bash", "#!/bin/sh", "echo ", "export ", "sudo ", "apt-get", "yum install", "pip3 ", "npm "]),
            ("powershell", ["param(", "write-host", "get-command", "$", "$true", "$false", "function "]),
            ("rust", ["fn ", "let mut", "impl ", "use ", "&str", "vec!", "pub fn", "match "]),
            ("go", ["func ", "package ", "import ", "var ", "type ", "struct ", "interface ", ":=", "go func"]),
            ("python", ["def ", "import ", "from ", "class ", "self.", "if __name__", "print(", "pandas.", "numpy."]),
            ("typescript", ["interface ", "type ", "enum ", ": string", ": number", ": boolean", " as ", "readonly "]),
            ("java", ["public class", "private ", "public ", "System.out", "import java", "@Override"]),
            ("javascript", ["const ", "let ", "=>", "function(", "async ", "await ", ".then(", ".catch("]),
            ("cpp", ["#include", "std::", "cout <<", "cin >>", "namespace ", "public:", "private:", "class "]),
            ("c", ["#include", "printf(", "scanf(", "int main", "struct ", "typedef ", "return 0;"]),
        ]

        # Check patterns in priority order (most specific first)
        for lang, keywords in patterns:
            # Check more keywords for JSX (it has many patterns)
            check_limit = 6 if lang == "jsx" else 4
            if any(keyword in code_lower for keyword in keywords[:check_limit]) and len(total_code) > 15:
                # For ambiguous cases (like "const" appearing in both TS and JS), check more keywords
                if lang in ["typescript", "javascript"]:
                    ts_specific = [": string", ": number", ": boolean", "interface ", "type ", "enum "]
                    if any(kw in code_lower for kw in ts_specific):
                        return "typescript"
                return lang

        return "text"

    @staticmethod
    def _group_code_blocks_by_language(code_blocks: List[Dict]) -> Dict[str, List[str]]:
        """
        Group code blocks by their programming language.

        Returns:
            Dictionary mapping language names to lists of code snippets.
        """
        if not code_blocks:
            return {}

        grouped: Dict[str, List[str]] = {}

        for code_block in code_blocks:
            code = code_block.get("code", "")
            if not code:
                continue

            # Detect language for this specific code block
            lang = code_block.get("lang", "text")
            if lang == "text" or not lang:
                # Try to detect from content
                temp_blocks = [{"code": code}]
                lang = MarkdownFormatter._detect_code_language(temp_blocks)

            if lang not in grouped:
                grouped[lang] = []
            grouped[lang].append(code)

        return grouped

    @staticmethod
    def format_lesson(lesson: Dict, category: str, locale: Optional[str] = None) -> str:
        """
        Format a lesson as markdown with structured sections.

        Args:
            lesson: Dictionary with lesson data
            category: Category name for the lesson
            locale: Optional locale override (uses config default if not provided)
        """
        loc = locale or LOCALE
        timestamp = datetime.now().strftime(TIMESTAMP_FORMAT)

        # Get localized labels
        problem_title_label = get_label("problem_title", loc)
        auto_time_label = get_label("auto_generated_time", loc)
        error_info_label = get_label("error_info", loc)
        related_code_label = get_label("related_code", loc)
        problem_desc_label = get_label("problem_description", loc)
        root_cause_label = get_label("root_cause", loc)
        solution_label = get_label("solution", loc)
        best_practices_label = get_label("best_practices", loc)

        # Generate title from problems, errors, or content
        problems = lesson.get("problems", [])
        errors = lesson.get("errors", [])

        if problems:
            title = problems[0][:50] + "..." if len(problems[0]) > 50 else problems[0]
        elif errors:
            title = errors[0][:50] + "..." if len(errors[0]) > 50 else errors[0]
        else:
            title = get_label("problem_example", loc)

        md = f"\n## {problem_title_label}：{title}\n\n"
        md += f"> **{auto_time_label}**: {timestamp}\n\n"

        # Add error messages
        if errors:
            md += f"### {error_info_label}\n```\n"
            for error in errors[:3]:  # Limit to first 3 errors
                md += f"{error}\n"
            md += "```\n\n"

        # Add code examples with language detection - grouped by language
        code_blocks = lesson.get("code_blocks", [])
        if code_blocks:
            grouped_code = MarkdownFormatter._group_code_blocks_by_language(code_blocks)

            if len(grouped_code) == 1:
                # Single language - simple display
                lang = list(grouped_code.keys())[0]
                md += f"### {related_code_label}\n```{lang}\n"
                # Show all code blocks for this language
                for code in grouped_code[lang][:3]:  # Limit to 3 blocks
                    md += code[:500] if len(code) > 500 else code
                    md += "\n\n"
                md = md.rstrip() + "\n```\n\n"
            else:
                # Multiple languages - grouped display
                md += f"### {related_code_label}\n\n"
                for lang, codes in sorted(grouped_code.items()):
                    md += f"#### {lang.upper()}\n```{lang}\n"
                    for code in codes[:2]:  # Limit to 2 blocks per language
                        md += code[:300] if len(code) > 300 else code
                        md += "\n\n"
                    md = md.rstrip() + "\n```\n\n"

        # Add problem description
        if problems:
            md += f"### {problem_desc_label}\n"
            for problem in problems[:2]:
                md += f"{problem}\n"
            md += "\n"

        # Add root cause
        causes = lesson.get("causes", [])
        if causes:
            md += f"### {root_cause_label}\n"
            for cause in causes[:2]:
                md += f"{cause}\n"
            md += "\n"

        # Add solution
        solutions = lesson.get("solutions", [])
        if solutions:
            md += f"### {solution_label}\n"
            for solution in solutions[:2]:
                md += f"{solution}\n"
            md += "\n"

        # Add best practices checklist
        practices = lesson.get("practices", [])
        if practices:
            md += f"### {best_practices_label}\n"
            for practice in practices:
                # Split by common delimiters to create checklist items
                items = re.split(r'[,;、\n]', practice)
                for item in items:
                    item = item.strip()
                    if item:
                        md += f"- [ ] {item}\n"
            md += "\n"

        # Fallback: add content preview if no structured content
        if not (problems or causes or solutions or practices):
            content = lesson.get("content_preview", "")
            if content:
                md += f"### {problem_desc_label}\n"
                md += content[:300]
                if len(content) > 300:
                    md += "..."
                md += "\n\n"

        md += "---\n"

        return md


class GotchaFileManager:
    """Manages reading and writing gotcha markdown files."""

    def __init__(self, gotchas_dir: Path):
        self.gotchas_dir = Path(gotchas_dir)
        self.gotchas_dir.mkdir(parents=True, exist_ok=True)

    def read_file(self, filename: str) -> str:
        """Read existing gotcha file content."""
        file_path = self.gotchas_dir / filename
        if file_path.exists():
            return file_path.read_text(encoding="utf-8")

        # Create parent directories if they don't exist
        file_path.parent.mkdir(parents=True, exist_ok=True)
        return get_template(filename)

    def write_file(self, filename: str, content: str, dry_run: bool = False) -> bool:
        """
        Write content to gotcha file with error tracking.

        Returns:
            True if write succeeded, False otherwise
        """
        file_path = self.gotchas_dir / filename

        if dry_run:
            print(f"[DRY RUN] Would update: {file_path}")
            print(f"[DRY RUN] Content preview:\n{content[:500]}...")
            return True

        try:
            file_path.write_text(content, encoding="utf-8")
            logger.info(f"Updated: {file_path}")
            return True
        except IOError as e:
            error_stats["file_write_errors"] += 1
            logger.error(f"Error writing file {file_path}: {e}")
            return False
        except Exception as e:
            error_stats["file_write_errors"] += 1
            logger.error(f"Unexpected error writing file {file_path}: {e}")
            return False

    def check_duplicate(self, filename: str, lesson: Dict, similarity_threshold: float = 0.75) -> bool:
        """
        Check if lesson already exists in file using fuzzy matching.

        Args:
            filename: The markdown file to check
            lesson: The lesson data to check for duplicates
            similarity_threshold: Minimum similarity ratio (0-1) to consider as duplicate

        Returns:
            True if a duplicate is detected, False otherwise
        """
        content = self.read_file(filename)

        # Normalize content for comparison (remove markdown formatting, extra whitespace)
        normalized_content = self._normalize_text(content)

        # Check for duplicate error messages
        errors = lesson.get("errors", [])
        for error in errors:
            normalized_error = self._normalize_text(error)
            if self._fuzzy_match(normalized_error, normalized_content, similarity_threshold):
                return True

        # Check for duplicate problems
        problems = lesson.get("problems", [])
        for problem in problems:
            normalized_problem = self._normalize_text(problem)
            if self._fuzzy_match(normalized_problem, normalized_content, similarity_threshold):
                return True

        # Check for duplicate code patterns (with higher threshold for code)
        code_blocks = lesson.get("code_blocks", [])
        for code_block in code_blocks:
            code = code_block.get("code", "") if isinstance(code_block, dict) else code_block
            # Normalize code: remove whitespace, comments
            normalized_code = self._normalize_code(code)
            if normalized_code and len(normalized_code) > 30:
                # Use higher threshold for code matching
                if self._fuzzy_match(normalized_code, normalized_content, similarity_threshold + 0.05):
                    return True

        return False

    @staticmethod
    def _normalize_text(text: str) -> str:
        """Normalize text for comparison by removing formatting and extra whitespace."""
        # Remove markdown code blocks
        text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
        # Remove inline code
        text = re.sub(r'`([^`]+)`', r'\1', text)
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove timestamps and IDs (common sources of false differences)
        text = re.sub(r'\d{4}-\d{2}-\d{2}[\s\d:]*', '', text)
        text = re.sub(r'0x[0-9a-f]+', '', text, flags=re.IGNORECASE)
        return text.strip().lower()

    @staticmethod
    def _normalize_code(code: str) -> str:
        """Normalize code for comparison."""
        if not code:
            return ""
        # Remove comments
        code = re.sub(r'//.*?\n', '\n', code)
        code = re.sub(r'#.*?\n', '\n', code)
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
        # Remove extra whitespace
        code = re.sub(r'\s+', ' ', code)
        return code.strip().lower()

    @staticmethod
    def _fuzzy_match(pattern: str, content: str, threshold: float) -> bool:
        """
        Use fuzzy matching to check if pattern exists in content.

        Uses SequenceMatcher for similarity comparison.
        """
        if not pattern or len(pattern) < 10:
            return False

        # For short patterns, check direct substring first
        if len(pattern) < 50 and pattern in content:
            return True

        # For longer patterns, use similarity matching
        # Split content into chunks for efficient matching
        chunk_size = len(pattern) + 200
        for i in range(0, len(content), chunk_size // 2):
            chunk = content[i:i + chunk_size]
            similarity = difflib.SequenceMatcher(None, pattern, chunk).ratio()
            if similarity >= threshold:
                return True

        return False


def find_conversation_history() -> Optional[Path]:
    """Auto-detect conversation history file path."""
    # Check environment variable first
    env_path = os.environ.get("CLAUDE_HISTORY_PATH")
    if env_path:
        return Path(env_path)

    # Try common Claude Code history locations
    home = Path.home()
    possible_paths = [
        home / ".claude" / "history.jsonl",
        home / ".claude" / "transcripts" / "latest.jsonl",
        Path.cwd() / ".claude" / "history.jsonl",
    ]

    for path in possible_paths:
        if path.exists():
            return path

    return None


def load_conversation_history(path: Optional[Path]) -> List[Dict]:
    """
    Load conversation history from JSONL file with error tracking.

    Returns a list of conversation entries. JSON parse errors are tracked
    but don't stop processing - valid entries are still returned.
    """
    if not path or not path.exists():
        logger.warning(f"Conversation history not found: {path}")
        return []

    history = []
    error_stats["total_entries_processed"] = 0

    try:
        with open(path, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                if not line.strip():
                    continue

                error_stats["total_entries_processed"] += 1

                try:
                    history.append(json.loads(line))
                except json.JSONDecodeError as e:
                    error_stats["json_parse_errors"] += 1
                    if ENABLE_ERROR_TRACKING:
                        logger.error(f"JSON parse error at line {line_num}: {e}")
                    continue
                except Exception as e:
                    error_stats["json_parse_errors"] += 1
                    if ENABLE_ERROR_TRACKING:
                        logger.error(f"Unexpected error parsing line {line_num}: {e}")
                    continue

    except IOError as e:
        error_stats["file_read_errors"] += 1
        logger.error(f"Error reading history file: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error reading history: {e}")
        return []

    logger.info(f"Loaded {len(history)} valid entries from {error_stats['total_entries_processed']} total lines")

    if error_stats["json_parse_errors"] > 0:
        logger.warning(f"Skipped {error_stats['json_parse_errors']} entries due to parse errors")

    return history


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Summarize technical lessons from Claude Code conversations"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without writing files"
    )
    parser.add_argument(
        "--gotchas-dir",
        type=str,
        default=os.environ.get("GOTCHAS_DIR", "./docs/gotchas"),
        help="Path to docs/gotchas directory"
    )
    parser.add_argument(
        "--history",
        type=str,
        default=None,
        help="Path to conversation history file"
    )

    args = parser.parse_args()

    # Find and load conversation history
    history_path = Path(args.history) if args.history else find_conversation_history()
    if not history_path:
        print("❌ Could not find conversation history")
        print("   Set CLAUDE_HISTORY_PATH or run from a project directory")
        sys.exit(1)

    print(f"📖 Loading conversation history from: {history_path}")
    history = load_conversation_history(history_path)
    print(f"   Found {len(history)} messages")

    if not history:
        print("⚠️  No conversation history found")
        sys.exit(0)

    # Extract lessons
    print("\n🔍 Extracting technical lessons...")
    extractor = GotchaExtractor(history)
    lessons = extractor.extract_lessons()
    print(f"   Found {len(lessons)} potential lessons")

    if not lessons:
        print("⚠️  No technical lessons found in conversation")
        sys.exit(0)

    # Classify and format lessons
    print("\n🏷️  Classifying lessons by topic...")
    classifier = TopicClassifier()
    formatter = MarkdownFormatter()
    file_manager = GotchaFileManager(args.gotchas_dir)

    # Group lessons by target file
    lessons_by_file: Dict[str, List[Dict]] = {}
    for lesson in lessons:
        category, filename = classifier.classify(lesson)
        if filename not in lessons_by_file:
            lessons_by_file[filename] = []
        lessons_by_file[filename].append((lesson, category))

    # Process each file
    updated_files = []
    for filename, items in lessons_by_file.items():
        print(f"\n📝 Processing {filename}...")

        # Read existing content
        existing_content = file_manager.read_file(filename)

        # Check for duplicates and add new lessons
        new_lessons_count = 0
        for lesson, category in items:
            if file_manager.check_duplicate(filename, lesson):
                print(f"   ⏭️  Skipping duplicate lesson")
                continue

            # Format and append
            formatted_lesson = formatter.format_lesson(lesson, category)
            updated_content = existing_content + formatted_lesson

            # Write back
            if file_manager.write_file(filename, updated_content, dry_run=args.dry_run):
                existing_content = updated_content
                new_lessons_count += 1

        if new_lessons_count > 0:
            updated_files.append((filename, new_lessons_count))

    # Summary
    print("\n" + "=" * 50)
    if updated_files:
        print("✅ Summary:")
        for filename, count in updated_files:
            print(f"   • {filename}: {count} new lesson(s)")
        print(f"\n📁 Gotchas directory: {args.gotchas_dir}")
    else:
        print("⚠️  No new lessons added (all duplicates)")

    # Error statistics (if enabled)
    if ENABLE_ERROR_TRACKING or any(error_stats.values()):
        print("\n📊 Error Statistics:")
        print(f"   • Total entries processed: {error_stats['total_entries_processed']}")
        print(f"   • JSON parse errors: {error_stats['json_parse_errors']}")
        print(f"   • File read errors: {error_stats['file_read_errors']}")
        print(f"   • File write errors: {error_stats['file_write_errors']}")
        print(f"   • Classification errors: {error_stats['classification_errors']}")

    if args.dry_run:
        print("\n[DRY RUN] No files were modified")


if __name__ == "__main__":
    main()
