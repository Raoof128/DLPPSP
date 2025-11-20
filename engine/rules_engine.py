import yaml
import os
from typing import Dict, Any, List
from .pii_detector import PIIDetector
from .classifier import DataClassifier
from .actions import ActionHandler

class DLPEngine:
    def __init__(self, policies_path: str = "config/policies.yaml", patterns_path: str = "config/patterns_au.json"):
        self.detector = PIIDetector(patterns_path)
        self.classifier = DataClassifier()
        self.action_handler = ActionHandler()
        self.policies = self._load_policies(policies_path)

    def _load_policies(self, path: str) -> List[Dict]:
        if not os.path.exists(path):
             base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
             path = os.path.join(base_path, path)
             
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
            return data.get('policies', [])

    def evaluate(self, text: str, channel: str) -> Dict[str, Any]:
        """
        Evaluates the text against DLP policies for a specific channel.
        """
        # 1. Detect PII
        matches = self.detector.scan(text)
        detected_types = list(matches.keys())

        # 2. Classify
        classification = self.classifier.classify(matches)

        # 3. Find Matching Policy
        triggered_policy = None
        action_result = {"status": "allowed", "message": "No policy violation."}
        final_text = text

        # Sort policies by severity (simple heuristic or defined order)
        # We'll assume the order in file or prioritize Block > Quarantine > Redact > Alert
        priority_order = {"block": 4, "quarantine": 3, "redact": 2, "alert": 1}
        
        matched_policies = []

        for policy in self.policies:
            if channel not in policy['channel']:
                continue
            
            # Check if policy matches detected types
            # Intersection of policy['match'] and detected_types
            policy_matches = set(policy['match']).intersection(set(detected_types))
            
            if policy_matches:
                matched_policies.append(policy)

        # Select highest priority policy
        if matched_policies:
            matched_policies.sort(key=lambda p: priority_order.get(p['action'], 0), reverse=True)
            triggered_policy = matched_policies[0]
            
            action = triggered_policy['action']
            
            if action == "block":
                action_result = self.action_handler.block()
                final_text = None # Content blocked
            
            elif action == "quarantine":
                filename = self.action_handler.quarantine(text, {"policy": triggered_policy['name'], "matches": detected_types})
                action_result = {"status": "quarantined", "location": filename}
                final_text = None # Content quarantined (removed from flow)

            elif action == "redact":
                final_text = self.action_handler.redact(text, matches)
                action_result = {"status": "redacted", "message": "Content redacted."}

            elif action == "alert":
                action_result = self.action_handler.alert(triggered_policy['name'], detected_types)
                # Alert doesn't stop flow, but we note it
        
        return {
            "classification": classification,
            "matches": matches,
            "policy_triggered": triggered_policy['name'] if triggered_policy else None,
            "action_taken": triggered_policy['action'] if triggered_policy else "allow",
            "action_result": action_result,
            "processed_content": final_text
        }
