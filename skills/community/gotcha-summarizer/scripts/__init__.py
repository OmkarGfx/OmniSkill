#!/usr/bin/env python3
"""
Gotcha Summarizer Scripts Package

Provides three-layer topic classification and lesson summarization.
"""

from .classifier import ThreeLayerTopicClassifier, TopicClassifier
from .config import get_template, MARKDOWN_TEMPLATES
from .keywords import (
    KEYWORD_CONFIG,
    DOMAIN_ORDER,
    DOMAIN_PRIORITIES,
    get_all_keywords,
    get_keywords_for_domain,
    get_keywords_for_category,
    get_filename_for_category,
    get_categories_for_domain,
)

__all__ = [
    "ThreeLayerTopicClassifier",
    "TopicClassifier",
    "get_template",
    "MARKDOWN_TEMPLATES",
    "KEYWORD_CONFIG",
    "DOMAIN_ORDER",
    "DOMAIN_PRIORITIES",
    "get_all_keywords",
    "get_keywords_for_domain",
    "get_keywords_for_category",
    "get_filename_for_category",
    "get_categories_for_domain",
]
