import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.pii_detector import PIIDetector

class TestPIIDetector(unittest.TestCase):
    def setUp(self):
        self.detector = PIIDetector()

    def test_tfn_detection(self):
        text = "My TFN is 123 456 789"
        result = self.detector.scan(text)
        self.assertIn("TFN", result)
        self.assertEqual(len(result["TFN"]), 1)

    def test_medicare_detection(self):
        text = "Medicare number: 2123456789"
        result = self.detector.scan(text)
        self.assertIn("Medicare", result)

    def test_credit_card_detection(self):
        text = "Payment card: 4532123456789010"
        result = self.detector.scan(text)
        self.assertIn("CreditCard", result)

    def test_mobile_detection(self):
        text = "Call me at 0412 345 678"
        result = self.detector.scan(text)
        self.assertIn("Mobile", result)

    def test_email_detection(self):
        text = "Contact: test@example.com"
        result = self.detector.scan(text)
        self.assertIn("Email", result)

    def test_no_matches(self):
        text = "This is completely clean text with no PII"
        result = self.detector.scan(text)
        self.assertEqual(len(result), 0)

    def test_multiple_types(self):
        text = "TFN: 123 456 789, Email: test@example.com, Mobile: 0412345678"
        result = self.detector.scan(text)
        self.assertGreaterEqual(len(result), 2)

if __name__ == '__main__':
    unittest.main()
