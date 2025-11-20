"""PII detection utilities for the DLP engine."""

from __future__ import annotations

import json
import logging
import os
import re
from re import Pattern

LOGGER = logging.getLogger(__name__)


class PIIDetector:
    """Detects sensitive information based on configurable regex patterns."""

    def __init__(self, patterns_path: str = "config/patterns_au.json") -> None:
        self.patterns: dict[str, Pattern[str]] = self._load_patterns(patterns_path)

    def _load_patterns(self, path: str) -> dict[str, Pattern[str]]:
        """
        Load and compile regex patterns from a JSON file.

        The method resolves relative paths when running from different entry points
        (e.g., API server vs. tests) and raises a clear error when the pattern file
        cannot be found or parsed.
        """

        candidate_paths = [path]
        if not os.path.isabs(path):
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            candidate_paths.append(os.path.join(base_path, path))

        pattern_file = next((p for p in candidate_paths if os.path.exists(p)), None)
        if not pattern_file:
            raise FileNotFoundError(f"Unable to locate pattern file in {candidate_paths}")

        with open(pattern_file, encoding="utf-8") as handle:
            try:
                raw_patterns: dict[str, str] = json.load(handle)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON in pattern file {pattern_file}") from exc

        compiled_patterns: dict[str, Pattern[str]] = {}
        for name, pattern in raw_patterns.items():
            try:
                compiled_patterns[name] = re.compile(pattern)
            except re.error as exc:  # pragma: no cover - defensive programming
                LOGGER.error("Invalid regex pattern for %s: %s", name, exc)
                continue

        LOGGER.debug("Loaded %d PII patterns from %s", len(compiled_patterns), pattern_file)
        return compiled_patterns

    def scan(self, text: str) -> dict[str, list[str]]:
        """Scan text for all loaded patterns and return matches grouped by type."""

        if not isinstance(text, str):
            raise TypeError("Text to scan must be a string")

        results: dict[str, list[str]] = {}
        for name, pattern in self.patterns.items():
            matches = pattern.findall(text)
            if matches:
                results[name] = matches
        return results

    def get_unique_matches(self, text: str) -> list[str]:
        """Return a list of unique pattern names found in the text."""

        results = self.scan(text)
        return list(results.keys())
