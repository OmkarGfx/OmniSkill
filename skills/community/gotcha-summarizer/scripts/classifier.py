#!/usr/bin/env python3
"""
Three-layer topic classifier for Gotcha Summarizer.

Implements a three-layer decision tree with weighted keyword matching:
Layer 1: Domain Classification (Frontend/Backend/Common)
Layer 2: Category Classification (e.g., Bugs/Framework/Database)
Layer 3: File Mapping (Category → markdown file)
"""

import logging
from typing import Dict, List, Tuple, Optional
from .keywords import (
    KEYWORD_CONFIG,
    DOMAIN_ORDER,
    DOMAIN_PRIORITIES,
    get_keywords_for_category,
    get_filename_for_category,
    get_categories_for_domain,
)


class DomainClassifier:
    """Layer 1: Classify technical issues into domains (Frontend/Backend/Common)."""

    # Minimum text length for classification (shorter texts are unreliable)
    MIN_TEXT_LENGTH = 20

    def __init__(self, enable_logging: bool = False):
        self.domain_order = DOMAIN_ORDER
        self.domain_keywords = self._build_domain_keywords()
        self.enable_logging = enable_logging
        self.logger = logging.getLogger(__name__)

    def _build_domain_keywords(self) -> Dict[str, List[Tuple[str, float]]]:
        """Build weighted keyword lists for each domain."""
        domain_keywords = {}
        for domain in self.domain_order:
            keywords = []
            categories = get_categories_for_domain(domain)
            for category in categories:
                keywords.extend(get_keywords_for_category(domain, category))
            domain_keywords[domain] = keywords
        return domain_keywords

    def classify(self, text: str) -> Tuple[str, Dict[str, float]]:
        """
        Classify text into a domain using weighted scoring.

        Priority: Common > Frontend > Backend
        Common is checked first to capture general topics (testing, git, etc.)
        Uses weighted scoring to determine the best match.

        Returns:
            (domain, confidence_scores) tuple
            - domain: The classified domain name
            - confidence_scores: Dictionary with all domain scores and max score
        """
        text_lower = text.lower()

        # Check minimum text length
        if len(text) < self.MIN_TEXT_LENGTH:
            if self.enable_logging:
                self.logger.warning(
                    f"Text too short for reliable classification ({len(text)} < {self.MIN_TEXT_LENGTH}), defaulting to 'common'"
                )

        # Calculate scores for each domain
        scores = {}
        for domain in self.domain_order:
            keywords = self.domain_keywords.get(domain, [])
            scores[domain] = self._calculate_score(text_lower, keywords)

        # Return domain with highest score above threshold
        max_score = max(scores.values())
        if max_score > 0.5:  # Minimum threshold for classification
            best_domain = max(scores, key=scores.get)
        else:
            best_domain = "common"

        # Build confidence info
        confidence_info = {
            "scores": scores,
            "max_score": max_score,
            "winner": best_domain,
            "confidence_ratio": max_score / (sum(scores.values()) or 1),
        }

        if self.enable_logging:
            self.logger.info(f"Domain classification: {best_domain} (confidence: {max_score:.2f})")

        return (best_domain, confidence_info)

    def _calculate_score(self, text: str, keywords: List[Tuple[str, float]]) -> float:
        """
        Calculate a weighted score based on keyword matches.

        Returns a score from 0 to infinity, where higher is better match.
        """
        score = 0.0
        for keyword, weight in keywords:
            if keyword in text:
                # Count occurrences and multiply by weight
                count = text.count(keyword)
                score += count * weight
        return score


class CategoryClassifier:
    """Layer 2: Classify issues within a domain into categories using weighted scoring."""

    # Minimum text length for category classification
    MIN_TEXT_LENGTH = 15

    def __init__(self, domain: str, enable_logging: bool = False):
        self.domain = domain
        self.category_priorities = get_categories_for_domain(domain)
        self.enable_logging = enable_logging
        self.logger = logging.getLogger(__name__)

    def classify(self, text: str) -> Tuple[str, Dict[str, float]]:
        """
        Classify text into a category within the domain using weighted scoring.

        Returns:
            (category, confidence_scores) tuple
            - category: The classified category name
            - confidence_scores: Dictionary with all category scores and max score
        """
        text_lower = text.lower()

        # Check minimum text length
        if len(text) < self.MIN_TEXT_LENGTH and self.enable_logging:
            self.logger.warning(
                f"Text too short for reliable category classification ({len(text)} < {self.MIN_TEXT_LENGTH})"
            )

        # Calculate weighted scores for each category
        scores = {}
        for category in self.category_priorities:
            keywords = get_keywords_for_category(self.domain, category)
            scores[category] = self._calculate_score(text_lower, keywords)

        # Return category with highest score above threshold
        max_score = max(scores.values())
        if max_score > 0.3:  # Lower threshold for categories
            best_category = max(scores, key=scores.get)
        else:
            best_category = self.category_priorities[0] if self.category_priorities else "code-quality"

        # Build confidence info
        confidence_info = {
            "scores": scores,
            "max_score": max_score,
            "winner": best_category,
            "confidence_ratio": max_score / (sum(scores.values()) or 1),
        }

        if self.enable_logging:
            self.logger.info(f"Category classification: {best_category} (confidence: {max_score:.2f})")

        return (best_category, confidence_info)

    def _calculate_score(self, text: str, keywords: List[Tuple[str, float]]) -> float:
        """
        Calculate a weighted score based on keyword matches.

        Returns a score from 0 to infinity, where higher is better match.
        """
        score = 0.0
        for keyword, weight in keywords:
            if keyword in text:
                # Count occurrences and multiply by weight
                count = text.count(keyword)
                score += count * weight
        return score


class FileMapper:
    """Layer 3: Map categories to file paths."""

    def __init__(self):
        pass

    def get_file_path(self, domain: str, category: str) -> str:
        """
        Get the file path for a given domain and category.

        Returns:
            Relative path to markdown file (e.g., "frontend/bugs.md")
        """
        return get_filename_for_category(domain, category)

    def get_category_name(self, domain: str, category: str) -> str:
        """
        Get a human-readable category name for display.

        Returns:
            Formatted category name (e.g., "Backend Bugs")
        """
        # Map category codes to display names
        display_names = {
            # Frontend
            "bugs": "Frontend Bugs",
            "frameworks": "Frontend Frameworks",
            "styling": "Frontend Styling",
            "build-tools": "Build Tools",
            "state-mgmt": "State Management",
            "ui-components": "UI Components",
            # Backend
            "database": "Database",
            "api": "API",
            "concurrency": "Concurrency",
            "performance": "Performance",
            "precision": "Precision",
            # Common
            "testing": "Testing",
            "cicd": "CI/CD",
            "git": "Git",
            "code-quality": "Code Quality",
        }

        base_name = display_names.get(category, category.title())

        # For bugs category, use the domain as prefix
        if category == "bugs":
            if domain == "frontend":
                return "Frontend Bugs"
            elif domain == "backend":
                return "Backend Bugs"
            else:
                return "Bugs"

        # For common domain, don't prefix
        if domain == "common":
            return base_name

        return base_name


class ThreeLayerTopicClassifier:
    """
    Main classifier that coordinates the three-layer classification.

    Layer 1: Domain (Frontend/Backend/Common)
    Layer 2: Category (e.g., Bugs/Framework/Database)
    Layer 3: File Path
    """

    def __init__(self, enable_logging: bool = False):
        self.domain_classifier = DomainClassifier(enable_logging=enable_logging)
        self.category_classifiers: Dict[str, CategoryClassifier] = {}
        self.file_mapper = FileMapper()
        self.enable_logging = enable_logging
        self.logger = logging.getLogger(__name__)

    def classify(self, lesson: Dict) -> Tuple[str, str, str, Dict]:
        """
        Classify a lesson using the three-layer decision tree.

        Args:
            lesson: Dictionary with lesson data (errors, content_preview, etc.)

        Returns:
            (category_name, filename, domain, confidence_info) tuple
            - category_name: Human-readable category (e.g., "Frontend Bugs")
            - filename: Path to markdown file (e.g., "frontend/bugs.md")
            - domain: Domain name (e.g., "frontend", "backend", "common")
            - confidence_info: Dictionary with classification confidence scores
        """
        # Extract text content from lesson
        content = lesson.get("content_preview", "").lower()
        errors = " ".join(lesson.get("errors", []))
        text = f"{content} {errors}".lower()

        # Layer 1: Classify domain
        domain, domain_confidence = self.domain_classifier.classify(text)

        # Layer 2: Get or create category classifier for this domain
        if domain not in self.category_classifiers:
            self.category_classifiers[domain] = CategoryClassifier(domain, enable_logging=self.enable_logging)

        category, category_confidence = self.category_classifiers[domain].classify(text)

        # Layer 3: Map to file path
        filename = self.file_mapper.get_file_path(domain, category)

        # Get display category name
        category_name = self.file_mapper.get_category_name(domain, category)

        # Combine confidence info
        confidence_info = {
            "domain": domain_confidence,
            "category": category_confidence,
        }

        if self.enable_logging:
            self.logger.info(
                f"Classified lesson as {domain}/{category} -> {filename} "
                f"(domain confidence: {domain_confidence['max_score']:.2f}, "
                f"category confidence: {category_confidence['max_score']:.2f})"
            )

        return (category_name, filename, domain, confidence_info)


# Backward compatibility: keep the old TopicClassifier name as an alias
class TopicClassifier(ThreeLayerTopicClassifier):
    """
    Alias for ThreeLayerTopicClassifier for backward compatibility.

    This allows existing code to continue working without changes.
    """

    def classify(self, lesson: Dict) -> Tuple[str, str]:
        """
        Classify a lesson (backward compatible interface).

        Returns:
            (category, filename) tuple (omits domain and confidence for backward compatibility)
        """
        category_name, filename, domain, confidence_info = super().classify(lesson)
        return (category_name, filename)
