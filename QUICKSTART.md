# DLP Platform - Quick Reference Guide

## 🚀 Getting Started (30 seconds)

```bash
# 1. Clone and navigate
cd dlp_platform

# 2. Run the platform
./run.sh
# Select option 1 for Dashboard

# 3. Open browser
# Visit: http://localhost:8501
```

## 📚 Common Commands

### Run Dashboard
```bash
streamlit run dashboard/app.py
```

### Run API Server
```bash
python api/server.py
# Docs at: http://localhost:8000/docs
```

### Run Tests
```bash
python -m unittest discover tests -v
```

### Run Demo Script
```bash
python demo.py
```

### Docker Compose
```bash
docker-compose up --build
```

## 🔍 Test Examples

### Detect TFN (Blocked)
```
Input: "Employee TFN: 123 456 789"
Result: BLOCKED
```

### Redact Credit Card
```
Input: "Card: 4532123456789010"
Result: REDACTED → "Card: [REDACTED: CreditCard]"
```

### Alert on Medical Terms
```
Input: "Patient diagnosis pending"
Result: ALERT (logged)
```

## 📊 API Endpoints

### Email Simulation
```bash
curl -X POST http://localhost:8000/simulate/email \
  -H "Content-Type: application/json" \
  -d '{
    "sender": "user@example.com",
    "recipient": "external@gmail.com",
    "subject": "Payment",
    "body": "TFN: 123 456 789"
  }'
```

### Text Analysis
```bash
curl -X POST http://localhost:8000/simulate/text \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Medicare: 2123456789",
    "channel": "email"
  }'
```

### File Upload
```bash
curl -X POST http://localhost:8000/simulate/file \
  -F "file=@test.txt" \
  -F "channel=file"
```

### View Policies
```bash
curl http://localhost:8000/policies
```

## 🎯 Australian PII Patterns

| Type | Pattern | Example |
|------|---------|---------|
| TFN | `\d{3} \d{3} \d{3}` | 123 456 789 |
| Medicare | `[2-6]\d{9}` | 2123456789 |
| ABN | `\d{2} \d{3} \d{3} \d{3}` | 12 345 678 901 |
| Credit Card | Luhn valid | 4532123456789010 |
| Mobile | `04\d{2} \d{3} \d{3}` | 0412 345 678 |

## ⚖️ DLP Actions

| Action | Behavior | Use Case |
|--------|----------|----------|
| **block** | Reject entirely | TFN, Credit Cards |
| **quarantine** | Store in isolation | Suspicious files |
| **redact** | Mask values | Partial blocking |
| **alert** | Log event | Monitoring |
| **allow** | Permit with log | Clean content |

## 🗂️ File Locations

```
dlp_audit.log          # Audit trail
dlp_report.md          # Generated reports
dlp_summary.json       # SIEM export
quarantine/            # Quarantined files
config/policies.yaml   # DLP rules
config/patterns_au.json # PII patterns
```

## 🐛 Troubleshooting

### "Module not found"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "Port already in use"
```bash
# For 8501 (Streamlit)
lsof -ti:8501 | xargs kill

# For 8000 (FastAPI)
lsof -ti:8000 | xargs kill
```

### "Config file not found"
```bash
# Ensure you're in the project root
cd /path/to/dlp_platform
python api/server.py
```

## 📝 Adding Custom Policies

Edit `config/policies.yaml`:

```yaml
policies:
  - name: my_custom_policy
    description: "Your description"
    match: ["TFN", "CreditCard"]  # Patterns to match
    channel: ["email", "chat"]     # Where to enforce
    action: "block"                # What to do
    severity: "high"               # Risk level
```

## 🔬 Testing New Patterns

1. Add pattern to `config/patterns_au.json`:
```json
{
  "MyPattern": "\\b[A-Z]{3}\\d{6}\\b"
}
```

2. Create test in `tests/`:
```python
def test_my_pattern(self):
    text = "ABC123456"
    result = self.detector.scan(text)
    self.assertIn("MyPattern", result)
```

3. Run tests:
```bash
python -m unittest tests.test_pii_detector
```

## 📊 Reports

### Generate Markdown Report
```python
from reporting.reporter import DLPReporter
reporter = DLPReporter()
# ... add events ...
reporter.generate_markdown_report()
```

### Generate JSON Summary
```python
reporter.generate_json_summary()
```

## 🔐 Security Notes

⚠️ **This is a demo platform**:
- ❌ No authentication
- ❌ No encryption
- ❌ Not production-ready
- ✅ For testing/learning only

See `SECURITY.md` for hardening checklist.

## 📚 Documentation

- **README.md** - Full documentation
- **CONTRIBUTING.md** - How to contribute
- **SECURITY.md** - Security policy
- **CHANGELOG.md** - Version history

## 💡 Tips

1. **Start with Dashboard** - Easiest way to understand the platform
2. **Use Sample Files** - Check `examples/sample_text/`
3. **Review Logs** - Learn from `dlp_audit.log`
4. **Run Demo First** - `python demo.py` shows all features
5. **Test Incrementally** - Start simple, add complexity

## 🆘 Need Help?

- Run: `./run.sh` and select an option
- Check: `README.md` for detailed docs
- Review: `demo.py` for working examples
- Open: GitHub issue for bugs/questions

---

**Built with ❤️ for Australian cybersecurity professionals**
