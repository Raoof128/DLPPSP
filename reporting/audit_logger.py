"""Structured audit logging for DLP events."""

from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Any


class AuditLogger:
    """Application-specific logger for recording DLP outcomes."""

    def __init__(self, log_file: str = "dlp_audit.log") -> None:
        self.log_file = log_file
        self.logger = logging.getLogger("DLP_Audit")
        self.logger.setLevel(logging.INFO)

        if not self.logger.handlers:
            handler = logging.FileHandler(log_file)
            handler.setLevel(logging.INFO)
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def log_event(
        self,
        event_type: str,
        channel: str,
        classification: str,
        policy: str,
        action: str,
        user: str = "system",
        metadata: dict | None = None,
    ) -> dict[str, Any]:
        """Log a DLP event to the configured audit log."""

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "channel": channel,
            "classification": classification,
            "policy_triggered": policy,
            "action_taken": action,
            "user": user,
            "metadata": metadata or {},
        }

        self.logger.info(json.dumps(log_entry))
        return log_entry

    def log_dlp_result(
        self, result: dict[str, Any], channel: str, user: str = "system"
    ) -> dict[str, Any]:
        """Convenience method to log a DLP evaluation result."""

        return self.log_event(
            event_type="dlp_evaluation",
            channel=channel,
            classification=result.get("classification", "Unknown"),
            policy=result.get("policy_triggered", "None"),
            action=result.get("action_taken", "allow"),
            user=user,
            metadata={
                "matches": list(result.get("matches", {}).keys()),
                "action_result": result.get("action_result", {}),
            },
        )
