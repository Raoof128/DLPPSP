# Contributing to DLP Platform

Thank you for your interest in contributing to the DLP Platform! This document provides guidelines for contributing to this project.

## 🎯 Project Vision

This is a **portfolio and educational project** designed to demonstrate enterprise-grade DLP concepts, Australian data protection compliance, and modern cybersecurity engineering practices.

## 🤝 How to Contribute

### Reporting Issues

If you find a bug or have a suggestion:

1. Check if the issue already exists in the [Issues](../../issues) section
2. Create a new issue with:
   - Clear, descriptive title
   - Steps to reproduce (for bugs)
   - Expected vs. actual behavior
   - Your environment (Python version, OS)

### Suggesting Enhancements

We welcome ideas for:
- Additional Australian PII patterns
- New DLP policy types
- Improved detection algorithms
- Documentation improvements
- Performance optimizations

### Pull Requests

1. **Fork** the repository
2. **Create a branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**:
   - Follow existing code style
   - Add tests for new features
   - Update documentation as needed
4. **Test your changes**:
   ```bash
   python -m unittest discover tests
   ```
5. **Commit** with clear messages:
   ```bash
   git commit -m "Add: New Medicare card validation pattern"
   ```
6. **Push** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Open a Pull Request** with:
   - Description of changes
   - Why the change is needed
   - Any testing performed

## 🧪 Testing Standards

All contributions must include tests:

```python
# Example test structure
import unittest
from engine.pii_detector import PIIDetector

class TestNewFeature(unittest.TestCase):
    def setUp(self):
        self.detector = PIIDetector()
    
    def test_specific_behavior(self):
        # Arrange
        test_input = "..."
        
        # Act
        result = self.detector.scan(test_input)
        
        # Assert
        self.assertIn("ExpectedPattern", result)
```

## 📝 Code Style

- **Python**: Follow PEP 8 guidelines
- **Docstrings**: Use Google-style docstrings
- **Type Hints**: Strongly encouraged for new code
- **Comments**: Explain *why*, not *what*

Example:

```python
def classify(self, matches: Dict[str, List[str]]) -> str:
    """
    Determines the classification label based on detected PII matches.
    
    Args:
        matches: Dictionary of {pattern_name: [matched_values]}
    
    Returns:
        Classification label: "Highly Sensitive", "Restricted", "Internal", or "Public"
    """
    # TFN and credit cards always trigger highest classification
    # to prevent accidental financial data exposure
    if "TFN" in matches or "CreditCard" in matches:
        return "Highly Sensitive"
    ...
```

## 🔒 Security Considerations

When contributing:

- ❌ **Never commit** real sensitive data (actual TFNs, credit cards, etc.)
- ✅ **Use synthetic data** for examples and tests
- ✅ **Review patterns** to ensure they don't create false positives
- ✅ **Document security implications** of new features

## 📚 Documentation

Update the README.md if your contribution:

- Adds new features
- Changes how the platform is used
- Introduces new dependencies
- Modifies the architecture

## 🌏 Australian Context

When adding new patterns or policies, consider:

- **Privacy Act 1988** – Australian privacy principles
- **APRA standards** – Financial sector requirements
- **ACSC guidance** – Cybersecurity best practices
- **Regional variations** – State-specific data types

## ✅ Checklist Before Submitting

- [ ] Code follows project style guidelines
- [ ] Tests added and passing (`python -m unittest discover tests`)
- [ ] Documentation updated (if needed)
- [ ] Commit messages are clear and descriptive
- [ ] No sensitive data in code or commits
- [ ] Changes work on Python 3.11+

## 🎓 Learning Resources

If you're new to DLP concepts:

- [NIST Guide to DLP](https://csrc.nist.gov/publications/detail/sp/800-177/final)
- [Australian Privacy Principles](https://www.oaic.gov.au/privacy/australian-privacy-principles)
- [APRA CPS 234](https://www.apra.gov.au/cps-234-information-security)

## 📧 Questions?

Feel free to:
- Open an issue for discussion
- Comment on existing issues
- Reach out via GitHub Discussions

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for helping improve the DLP Platform!** 🛡️
