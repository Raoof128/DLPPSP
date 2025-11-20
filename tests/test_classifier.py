import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.classifier import DataClassifier

class TestDataClassifier(unittest.TestCase):
    def setUp(self):
        self.classifier = DataClassifier()

    def test_highly_sensitive_tfn(self):
        matches = {"TFN": ["123 456 789"]}
        classification = self.classifier.classify(matches)
        self.assertEqual(classification, "Highly Sensitive")

    def test_highly_sensitive_credit_card(self):
        matches = {"CreditCard": ["4532123456789010"]}
        classification = self.classifier.classify(matches)
        self.assertEqual(classification, "Highly Sensitive")

    def test_highly_sensitive_medical(self):
        matches = {"Medicare": ["2123456789"], "Medical_Terms": ["diagnosis"]}
        classification = self.classifier.classify(matches)
        self.assertEqual(classification, "Highly Sensitive")

    def test_restricted_medicare(self):
        matches = {"Medicare": ["2123456789"]}
        classification = self.classifier.classify(matches)
        self.assertEqual(classification, "Restricted")

    def test_restricted_financial(self):
        matches = {"ABN": ["12 345 678 901"]}
        classification = self.classifier.classify(matches)
        self.assertEqual(classification, "Restricted")

    def test_internal_contact(self):
        matches = {"Email": ["test@example.com"], "Mobile": ["0412345678"]}
        classification = self.classifier.classify(matches)
        self.assertEqual(classification, "Internal")

    def test_public_no_matches(self):
        matches = {}
        classification = self.classifier.classify(matches)
        self.assertEqual(classification, "Public")

if __name__ == '__main__':
    unittest.main()
