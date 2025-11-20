import logging
import json
from datetime import datetime
from typing import Dict, Any

class AuditLogger:
    def __init__(self, log_file: str = "dlp_audit.log"):
        self.log_file = log_file
        self.logger = logging.getLogger("DLP_Audit")
        self.logger.setLevel(logging.INFO)
        
        # File handler
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        
        self.logger.addHandler(fh)

    def log_event(self, event_type: str, channel: str, classification: str, 
                  policy: str, action: str, user: str = "system", metadata: Dict = None):
        """
        Logs a DLP event to the audit log.
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "channel": channel,
            "classification": classification,
            "policy_triggered": policy,
            "action_taken": action,
            "user": user,
            "metadata": metadata or {}
        }
        
        self.logger.info(json.dumps(log_entry))
        return log_entry

    def log_dlp_result(self, result: Dict[str, Any], channel: str, user: str = "system"):
        """
        Convenience method to log a DLP evaluation result.
        """
        return self.log_event(
            event_type="dlp_evaluation",
            channel=channel,
            classification=result.get("classification", "Unknown"),
            policy=result.get("policy_triggered", "None"),
            action=result.get("action_taken", "allow"),
            user=user,
            metadata={
                "matches": list(result.get("matches", {}).keys()),
                "action_result": result.get("action_result", {})
            }
        )
