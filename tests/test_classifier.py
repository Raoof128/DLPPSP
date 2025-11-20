from engine.classifier import DataClassifier


def test_highly_sensitive_tfn():
    classifier = DataClassifier()
    classification = classifier.classify({"TFN": ["123 456 789"]})
    assert classification == "Highly Sensitive"


def test_highly_sensitive_credit_card():
    classifier = DataClassifier()
    classification = classifier.classify({"CreditCard": ["4532123456789010"]})
    assert classification == "Highly Sensitive"


def test_highly_sensitive_medical():
    classifier = DataClassifier()
    classification = classifier.classify(
        {"Medicare": ["2123456789"], "Medical_Terms": ["diagnosis"]}
    )
    assert classification == "Highly Sensitive"


def test_restricted_medicare():
    classifier = DataClassifier()
    classification = classifier.classify({"Medicare": ["2123456789"]})
    assert classification == "Restricted"


def test_restricted_financial():
    classifier = DataClassifier()
    classification = classifier.classify({"ABN": ["12 345 678 901"]})
    assert classification == "Restricted"


def test_internal_contact():
    classifier = DataClassifier()
    classification = classifier.classify({"Email": ["test@example.com"], "Mobile": ["0412345678"]})
    assert classification == "Internal"


def test_public_no_matches():
    classifier = DataClassifier()
    classification = classifier.classify({})
    assert classification == "Public"
