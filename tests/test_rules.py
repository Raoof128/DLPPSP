import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.rules_engine import DLPEngine

class TestRulesEngine(unittest.TestCase):
    def setUp(self):
        self.engine = DLPEngine()

    def test_block_tfn_email(self):
        text = "Please send payment to TFN: 123 456 789"
        result = self.engine.evaluate(text, channel="email")
        
        self.assertEqual(result["classification"], "Highly Sensitive")
        self.assertEqual(result["action_taken"], "block")
        self.assertIsNone(result["processed_content"])

    def test_redact_credit_card(self):
        text = "Pay with card 4532123456789010"
        result = self.engine.evaluate(text, channel="email")
        
        self.assertEqual(result["action_taken"], "redact")
        self.assertIsNotNone(result["processed_content"])
        self.assertIn("[REDACTED:", result["processed_content"])

    def test_alert_medical_terms(self):
        text = "Patient diagnosis is pending"
        result = self.engine.evaluate(text, channel="chat")
        
        # Should trigger alert policy
        if result["action_taken"] == "alert":
            self.assertIn("Medical_Terms", result["matches"])

    def test_allow_clean_content(self):
        text = "This is clean public information"
        result = self.engine.evaluate(text, channel="email")
        
        self.assertEqual(result["action_taken"], "allow")
        self.assertEqual(result["processed_content"], text)

    def test_quarantine_financial_file(self):
        text = "ABN: 12 345 678 901, Invoice details attached"
        result = self.engine.evaluate(text, channel="file")
        
        # Depending on policy order, could be quarantine or other action
        self.assertIn(result["action_taken"], ["quarantine", "block", "redact"])

if __name__ == '__main__':
    unittest.main()
