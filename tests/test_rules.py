import pytest

from engine.rules_engine import DLPEngine


@pytest.fixture()
def engine():
    return DLPEngine()


def test_block_tfn_email(engine: DLPEngine):
    text = "Please send payment to TFN: 123 456 789"
    result = engine.evaluate(text, channel="email")

    assert result["classification"] == "Highly Sensitive"
    assert result["action_taken"] == "block"
    assert result["processed_content"] is None


def test_redact_credit_card(engine: DLPEngine):
    result = engine.evaluate("Pay with card 4532123456789010", channel="email")

    assert result["action_taken"] == "redact"
    assert result["processed_content"] is not None
    assert "[REDACTED:" in result["processed_content"]


def test_alert_medical_terms(engine: DLPEngine):
    result = engine.evaluate("Patient diagnosis is pending", channel="chat")

    assert result["matches"] != {}
    assert result["action_taken"] in {"alert", "allow"}


def test_allow_clean_content(engine: DLPEngine):
    text = "This is clean public information"
    result = engine.evaluate(text, channel="email")

    assert result["action_taken"] == "allow"
    assert result["processed_content"] == text


def test_quarantine_financial_file(engine: DLPEngine):
    result = engine.evaluate("ABN: 12 345 678 901, Invoice details attached", channel="file")

    assert result["action_taken"] in {"quarantine", "block", "redact"}


def test_invalid_channel(engine: DLPEngine):
    with pytest.raises(ValueError):
        engine.evaluate("data", channel="   ")
