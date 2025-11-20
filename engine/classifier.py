"""Data classification helpers used by the DLP engine."""

from __future__ import annotations

from collections.abc import Iterable


class DataClassifier:
    """Simple policy-based classifier for detected PII matches."""

    def __init__(self) -> None:
        self.hierarchy = {
            "Highly Sensitive": 3,
            "Restricted": 2,
            "Internal": 1,
            "Public": 0,
        }

    def classify(self, matches: dict[str, list[str]]) -> str:
        """Determine the classification label based on detected PII matches."""

        detected_types: Iterable[str] = matches.keys()

        if "TFN" in detected_types or "CreditCard" in detected_types:
            return "Highly Sensitive"

        if "Medicare" in detected_types and "Medical_Terms" in detected_types:
            return "Highly Sensitive"

        if "Medicare" in detected_types:
            return "Restricted"

        if "ABN" in detected_types or "ACN" in detected_types:
            return "Restricted"

        if "Financial_Terms" in detected_types:
            return "Restricted"

        if "Mobile" in detected_types or "Email" in detected_types:
            return "Internal"

        if not matches:
            return "Public"

        return "Internal"
