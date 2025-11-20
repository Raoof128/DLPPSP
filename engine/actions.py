"""Action handlers for DLP policy enforcement."""

from __future__ import annotations

import json
import logging
import os
import uuid
from datetime import datetime

LOGGER = logging.getLogger(__name__)


class ActionHandler:
    """Implements quarantine, redaction, blocking, and alerting actions."""

    def __init__(self, quarantine_dir: str = "quarantine") -> None:
        self.quarantine_dir = quarantine_dir
        os.makedirs(self.quarantine_dir, exist_ok=True)

    def redact(self, text: str, matches: dict[str, list[str]]) -> str:
        """
        Redact sensitive information from the provided text.

        Each detected value is replaced with a marker that includes the PII type.
        """

        redacted_text = text
        for pii_type, values in matches.items():
            for value in values:
                redacted_text = redacted_text.replace(value, f"[REDACTED: {pii_type}]")
        LOGGER.info("Applied redaction for PII types: %s", list(matches.keys()))
        return redacted_text

    def quarantine(self, content: str, metadata: dict) -> str:
        """
        Persist the offending content and metadata to the quarantine directory.

        Returns the full path to the quarantined artifact.
        """

        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4()}.txt"
        filepath = os.path.join(self.quarantine_dir, filename)

        data = {"metadata": metadata, "content": content}

        with open(filepath, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2)

        LOGGER.warning("Content quarantined at %s", filepath)
        return filepath

    def block(self) -> dict[str, str]:
        """Return a standard block response."""

        LOGGER.warning("Content blocked by policy")
        return {"status": "blocked", "message": "Content blocked by DLP policy."}

    def alert(self, policy_name: str, matches: list[str]) -> dict[str, object]:
        """Return an alert payload for downstream handling."""

        LOGGER.info("Alert triggered for policy %s with matches %s", policy_name, matches)
        return {
            "status": "alert",
            "message": f"Alert triggered for policy: {policy_name}",
            "matches": matches,
        }
