import os
import uuid
import json
from datetime import datetime
from typing import Dict, List

class ActionHandler:
    def __init__(self, quarantine_dir: str = "quarantine"):
        self.quarantine_dir = quarantine_dir
        if not os.path.exists(self.quarantine_dir):
            os.makedirs(self.quarantine_dir)

    def redact(self, text: str, matches: Dict[str, List[str]]) -> str:
        """
        Redacts sensitive information from the text.
        Replaces matched strings with [REDACTED: TYPE].
        """
        redacted_text = text
        for pii_type, values in matches.items():
            for value in values:
                # Simple replace - in production, be careful with overlapping matches
                redacted_text = redacted_text.replace(value, f"[REDACTED: {pii_type}]")
        return redacted_text

    def quarantine(self, content: str, metadata: Dict) -> str:
        """
        Saves the content to a quarantine folder.
        Returns the filename.
        """
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4()}.txt"
        filepath = os.path.join(self.quarantine_dir, filename)
        
        data = {
            "metadata": metadata,
            "content": content
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
            
        return filepath

    def block(self) -> Dict:
        return {"status": "blocked", "message": "Content blocked by DLP policy."}

    def alert(self, policy_name: str, matches: List[str]) -> Dict:
        return {"status": "alert", "message": f"Alert triggered for policy: {policy_name}", "matches": matches}
