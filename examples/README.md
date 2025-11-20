# Sample Data Examples

This directory contains test data for validating the DLP Platform.

## 📁 Contents

### `sample_text/sensitive_data.txt`
**Purpose:** Demonstrates detection of multiple Australian PII types

**Contains:**
- Tax File Number (TFN)
- Medicare Number
- Australian Business Number (ABN)
- Australian Company Number (ACN)
- Credit Card Number
- Mobile Number
- Email Address
- Medical Terms
- Financial Keywords

**Expected Behavior:**
- **Classification:** Highly Sensitive
- **Policy Triggered:** block_tfn_external
- **Action:** BLOCKED

### `sample_text/clean_data.txt`
**Purpose:** Demonstrates content with no sensitive data

**Contains:**
- Public company information
- Website URLs
- Generic contact information

**Expected Behavior:**
- **Classification:** Public
- **Policy Triggered:** None
- **Action:** ALLOWED

## 🧪 How to Use

### Option 1: Dashboard
1. Launch dashboard: `streamlit run dashboard/app.py`
2. Select "File Upload" mode
3. Upload a sample file
4. View results

### Option 2: API
```bash
curl -X POST http://localhost:8000/simulate/file \
  -F "file=@examples/sample_text/sensitive_data.txt" \
  -F "channel=file"
```

### Option 3: Python
```python
from engine.rules_engine import DLPEngine

engine = DLPEngine()

# Test sensitive data
with open('examples/sample_text/sensitive_data.txt', 'r') as f:
    content = f.read()
    result = engine.evaluate(content, channel="file")
    print(result)

# Test clean data
with open('examples/sample_text/clean_data.txt', 'r') as f:
    content = f.read()
    result = engine.evaluate(content, channel="file")
    print(result)
```

## 🔍 Creating Custom Examples

### Template for Sensitive Data
```
[Context describing the data]
TFN: XXX XXX XXX
Medicare: XXXXXXXXXX
ABN: XX XXX XXX XXX
Credit Card: XXXX XXXX XXXX XXXX
Mobile: 04XX XXX XXX
Email: user@example.com
[Medical or Financial context]
```

### Template for Clean Data
```
Public information only
Company website: www.example.com
General contact: info@example.com
Business hours: 9am-5pm AEST
```

## ⚠️ Important Notes

1. **Use Synthetic Data Only**
   - Never use real PII in examples
   - Generate fake but realistic patterns
   - Ensure compliance with privacy laws

2. **Test Data Validity**
   - TFNs should follow pattern but be fake
   - Credit cards should be test numbers or invalid
   - Use example.com for email domains

3. **File Formats**
   - Currently supports: `.txt`, `.csv`, `.log`
   - Plain text encoding (UTF-8)
   - Binary files not supported in demo

## 📊 Expected Detection Results

### Sensitive Data File
```json
{
  "classification": "Highly Sensitive",
  "matches": {
    "TFN": ["123 456 789"],
    "Medicare": ["2123456789"],
    "ABN": ["12 345 678 901"],
    "ACN": ["123 456 789"],
    "CreditCard": ["4532 1234 5678 9010"],
    "Mobile": ["0412 345 678"],
    "Email": ["john.smith@example.com"],
    "Medical_Terms": ["diagnosis", "patient", "treatment"],
    "Financial_Terms": ["salary", "audit"]
  },
  "policy_triggered": "block_tfn_external",
  "action_taken": "block"
}
```

### Clean Data File
```json
{
  "classification": "Public",
  "matches": {},
  "policy_triggered": null,
  "action_taken": "allow"
}
```

## 🎓 Learning Exercises

1. **Modify Patterns**
   - Edit `config/patterns_au.json`
   - Add new detection patterns
   - Test against sample files

2. **Create New Policies**
   - Edit `config/policies.yaml`
   - Define different actions
   - Observe behavior changes

3. **Test Edge Cases**
   - Create files with borderline content
   - Test policy priority resolution
   - Experiment with channel restrictions

## 📚 Additional Resources

- Main README: `../README.md`
- Pattern Configuration: `../config/patterns_au.json`
- Policy Configuration: `../config/policies.yaml`
- API Documentation: `http://localhost:8000/docs`

---

**🛡️ Remember: Only use synthetic test data. Never input real PII.**
