from typing import List, Dict

class DataClassifier:
    def __init__(self):
        self.hierarchy = {
            "Highly Sensitive": 3,
            "Restricted": 2,
            "Internal": 1,
            "Public": 0
        }

    def classify(self, matches: Dict[str, List[str]]) -> str:
        """
        Determines the classification label based on detected PII matches.
        """
        detected_types = matches.keys()

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

        if not detected_types:
            return "Public"

        return "Internal"
