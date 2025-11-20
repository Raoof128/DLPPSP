import pytest

from engine.pii_detector import PIIDetector


def test_tfn_detection():
    detector = PIIDetector()
    text = "My TFN is 123 456 789"
    result = detector.scan(text)
    assert "TFN" in result and len(result["TFN"]) == 1


def test_medicare_detection():
    detector = PIIDetector()
    result = detector.scan("Medicare number: 2123456789")
    assert "Medicare" in result


def test_credit_card_detection():
    detector = PIIDetector()
    result = detector.scan("Payment card: 4532123456789010")
    assert "CreditCard" in result


def test_mobile_detection():
    detector = PIIDetector()
    result = detector.scan("Call me at 0412 345 678")
    assert "Mobile" in result


def test_email_detection():
    detector = PIIDetector()
    result = detector.scan("Contact: test@example.com")
    assert "Email" in result


def test_no_matches():
    detector = PIIDetector()
    result = detector.scan("This is completely clean text with no PII")
    assert result == {}


def test_multiple_types():
    detector = PIIDetector()
    result = detector.scan("TFN: 123 456 789, Email: test@example.com, Mobile: 0412345678")
    assert len(result.keys()) >= 2


def test_invalid_text_type():
    detector = PIIDetector()
    with pytest.raises(TypeError):
        detector.scan(None)  # type: ignore[arg-type]
