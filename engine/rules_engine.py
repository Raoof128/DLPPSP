"""Rules engine that coordinates DLP detection, classification, and actions."""

from __future__ import annotations

import logging
import os
from typing import Any

import yaml

from .actions import ActionHandler
from .classifier import DataClassifier
from .pii_detector import PIIDetector

LOGGER = logging.getLogger(__name__)


class DLPEngine:
    """Core DLP workflow for evaluating content against configured policies."""

    def __init__(
        self,
        policies_path: str = "config/policies.yaml",
        patterns_path: str = "config/patterns_au.json",
    ) -> None:
        self.detector = PIIDetector(patterns_path)
        self.classifier = DataClassifier()
        self.action_handler = ActionHandler()
        self.policies = self._load_policies(policies_path)

    def _load_policies(self, path: str) -> list[dict[str, Any]]:
        """Load policy definitions from YAML with defensive validation."""

        candidate_paths = [path]
        if not os.path.isabs(path):
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            candidate_paths.append(os.path.join(base_path, path))

        policy_file = next((p for p in candidate_paths if os.path.exists(p)), None)
        if not policy_file:
            raise FileNotFoundError(f"Unable to locate policy file in {candidate_paths}")

        with open(policy_file, encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}

        policies: list[dict[str, Any]] = data.get("policies", [])
        valid_policies: list[dict[str, Any]] = []
        for policy in policies:
            if not {"name", "match", "channel", "action"}.issubset(policy):
                LOGGER.warning("Skipping malformed policy entry: %s", policy)
                continue
            if not isinstance(policy["channel"], list):
                LOGGER.warning("Policy %s has invalid channel format", policy["name"])
                continue
            valid_policies.append(policy)

        LOGGER.info("Loaded %d policies from %s", len(valid_policies), policy_file)
        return valid_policies

    def evaluate(self, text: str, channel: str) -> dict[str, Any]:
        """Evaluate the text against DLP policies for a specific channel."""

        if not isinstance(text, str):
            raise TypeError("text must be a string")
        if not isinstance(channel, str) or not channel.strip():
            raise ValueError("channel must be a non-empty string")

        normalized_channel = channel.lower().strip()

        matches = self.detector.scan(text)
        detected_types = list(matches.keys())
        classification = self.classifier.classify(matches)

        priority_order = {"block": 4, "quarantine": 3, "redact": 2, "alert": 1}
        matched_policies: list[dict[str, Any]] = []

        for policy in self.policies:
            if normalized_channel not in [channel.lower() for channel in policy["channel"]]:
                continue

            policy_matches = set(policy["match"]).intersection(set(detected_types))
            if policy_matches:
                matched_policies.append(policy)

        triggered_policy: dict[str, Any] | None = None
        action_result: dict[str, Any] = {
            "status": "allowed",
            "message": "No policy violation.",
        }
        final_text: str | None = text

        if matched_policies:
            matched_policies.sort(
                key=lambda policy: priority_order.get(policy["action"], 0), reverse=True
            )
            triggered_policy = matched_policies[0]
            action = triggered_policy["action"]

            if action == "block":
                action_result = self.action_handler.block()
                final_text = None
            elif action == "quarantine":
                filename = self.action_handler.quarantine(
                    text, {"policy": triggered_policy["name"], "matches": detected_types}
                )
                action_result = {"status": "quarantined", "location": filename}
                final_text = None
            elif action == "redact":
                final_text = self.action_handler.redact(text, matches)
                action_result = {"status": "redacted", "message": "Content redacted."}
            elif action == "alert":
                action_result = self.action_handler.alert(triggered_policy["name"], detected_types)

            LOGGER.info(
                "Policy %s applied with action %s for channel %s",
                triggered_policy["name"],
                triggered_policy["action"],
                normalized_channel,
            )

        return {
            "classification": classification,
            "matches": matches,
            "policy_triggered": triggered_policy["name"] if triggered_policy else None,
            "action_taken": triggered_policy["action"] if triggered_policy else "allow",
            "action_result": action_result,
            "processed_content": final_text,
        }
