#!/usr/bin/env python3
"""
DLP Platform Banner Display
"""

BANNER = """
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║   ██████╗ ██╗     ██████╗     ██████╗ ██╗      █████╗ ████████╗  ║
║   ██╔══██╗██║     ██╔══██╗    ██╔══██╗██║     ██╔══██╗╚══██╔══╝  ║
║   ██║  ██║██║     ██████╔╝    ██████╔╝██║     ███████║   ██║     ║
║   ██║  ██║██║     ██╔═══╝     ██╔═══╝ ██║     ██╔══██║   ██║     ║
║   ██████╔╝███████╗██║         ██║     ███████╗██║  ██║   ██║     ║
║   ╚═════╝ ╚══════╝╚═╝         ╚═╝     ╚══════╝╚═╝  ╚═╝   ╚═╝     ║
║                                                                    ║
║              Data Loss Prevention Policy Simulation               ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝

🛡️  Enterprise-Grade DLP Testing Platform
🇦🇺  Australian Data Protection Compliance
📊  Multi-Channel Policy Enforcement
🔍  Real-Time PII Detection
⚖️  Policy Simulation & Validation

═══════════════════════════════════════════════════════════════════
"""

INFO = """
📋 FEATURES:
   • Detect Australian PII (TFN, Medicare, ABN/ACN)
   • Enforce DLP Policies (Block/Redact/Quarantine/Alert)
   • Generate Compliance Reports (Markdown, JSON)
   • Test Multi-Channel Scenarios (Email, Chat, File)
   • Streamlit Dashboard + FastAPI + Docker Ready

🚀 QUICK START:
   1. Run: ./run.sh
   2. Select: Dashboard (Option 1)
   3. Visit: http://localhost:8501

📚 DOCUMENTATION:
   • README.md       - Complete documentation
   • QUICKSTART.md   - Quick reference guide
   • SECURITY.md     - Security considerations
   • PROJECT_SUMMARY.md - Completion report

🧪 TESTING:
   • Run Tests: python -m unittest discover tests
   • Run Demo:  python demo.py
   • API Docs:  http://localhost:8000/docs

═══════════════════════════════════════════════════════════════════

⚠️  IMPORTANT: This is a demonstration platform for portfolio
   and educational purposes. See SECURITY.md before production use.

Version: 1.0.0 | License: MIT | Python: 3.11+
Built with ❤️  for Australian Cybersecurity Professionals

═══════════════════════════════════════════════════════════════════
"""

if __name__ == "__main__":
    print(BANNER)
    print(INFO)
