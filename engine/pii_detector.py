import re
import json
import os
from typing import Dict, List, Tuple

class PIIDetector:
    def __init__(self, patterns_path: str = "config/patterns_au.json"):
        self.patterns = self._load_patterns(patterns_path)

    def _load_patterns(self, path: str) -> Dict[str, str]:
        # Adjust path if running from different context
        if not os.path.exists(path):
            # Try absolute path if relative fails
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            path = os.path.join(base_path, path)
            
        with open(path, 'r') as f:
            return json.load(f)

    def scan(self, text: str) -> Dict[str, List[str]]:
        """
        Scans text for all loaded patterns.
        Returns a dictionary of {pattern_name: [matches]}
        """
        results = {}
        for name, pattern in self.patterns.items():
            matches = re.findall(pattern, text)
            if matches:
                results[name] = matches
        return results

    def get_unique_matches(self, text: str) -> List[str]:
        """Returns a list of unique pattern names found in the text."""
        results = self.scan(text)
        return list(results.keys())
