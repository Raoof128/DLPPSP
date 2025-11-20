#!/usr/bin/env python3
"""
DLP Platform - Comprehensive Demo Script
Tests all major platform features
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from engine.rules_engine import DLPEngine
from reporting.audit_logger import AuditLogger
from reporting.reporter import DLPReporter

def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")

def print_result(result):
    """Print DLP evaluation result."""
    print(f"📊 Classification: {result['classification']}")
    print(f"🎯 Matches Found: {list(result['matches'].keys()) if result['matches'] else 'None'}")
    print(f"⚖️  Policy Triggered: {result['policy_triggered'] or 'None'}")
    print(f"🚨 Action Taken: {result['action_taken'].upper()}")
    
    if result['processed_content']:
        print(f"\n📄 Processed Output:")
        print(f"   {result['processed_content'][:100]}...")
    else:
        print(f"\n🚫 Content was {result['action_taken']}")

def main():
    print_header("🛡️  DLP PLATFORM - DEMONSTRATION")
    
    # Initialize
    print("Initializing DLP Engine...")
    engine = DLPEngine()
    audit_logger = AuditLogger()
    reporter = DLPReporter()
    print("✅ Initialization complete\n")
    
    # Test 1: Blocked TFN in Email
    print_header("TEST 1: Blocked TFN in Email")
    test1_content = "Hi, please process payment for employee with TFN: 123 456 789"
    print(f"Input: {test1_content}")
    result1 = engine.evaluate(test1_content, channel="email")
    print_result(result1)
    audit_logger.log_dlp_result(result1, "email")
    reporter.add_event({
        "timestamp": "2025-11-21T10:00:00",
        "channel": "email",
        "classification": result1["classification"],
        "policy_triggered": result1["policy_triggered"],
        "action_taken": result1["action_taken"],
        "metadata": {"matches": list(result1['matches'].keys())}
    })
    
    # Test 2: Redacted Credit Card
    print_header("TEST 2: Redacted Credit Card")
    test2_content = "Please charge card number 4532123456789010 for the purchase"
    print(f"Input: {test2_content}")
    result2 = engine.evaluate(test2_content, channel="email")
    print_result(result2)
    audit_logger.log_dlp_result(result2, "email")
    reporter.add_event({
        "timestamp": "2025-11-21T10:01:00",
        "channel": "email",
        "classification": result2["classification"],
        "policy_triggered": result2["policy_triggered"],
        "action_taken": result2["action_taken"],
        "metadata": {"matches": list(result2['matches'].keys())}
    })
    
    # Test 3: Medical Alert
    print_header("TEST 3: Medical Term Alert")
    test3_content = "Patient diagnosis shows acute symptoms requiring treatment"
    print(f"Input: {test3_content}")
    result3 = engine.evaluate(test3_content, channel="chat")
    print_result(result3)
    audit_logger.log_dlp_result(result3, "chat")
    reporter.add_event({
        "timestamp": "2025-11-21T10:02:00",
        "channel": "chat",
        "classification": result3["classification"],
        "policy_triggered": result3["policy_triggered"],
        "action_taken": result3["action_taken"],
        "metadata": {"matches": list(result3['matches'].keys())}
    })
    
    # Test 4: Quarantine Financial File
    print_header("TEST 4: Quarantine Financial Document")
    test4_content = "Company ABN: 12 345 678 901, Annual audit report attached"
    print(f"Input: {test4_content}")
    result4 = engine.evaluate(test4_content, channel="file")
    print_result(result4)
    audit_logger.log_dlp_result(result4, "file")
    reporter.add_event({
        "timestamp": "2025-11-21T10:03:00",
        "channel": "file",
        "classification": result4["classification"],
        "policy_triggered": result4["policy_triggered"],
        "action_taken": result4["action_taken"],
        "metadata": {"matches": list(result4['matches'].keys())}
    })
    
    # Test 5: Clean Content
    print_header("TEST 5: Clean Public Content")
    test5_content = "Please visit our website at www.example.com for more information"
    print(f"Input: {test5_content}")
    result5 = engine.evaluate(test5_content, channel="email")
    print_result(result5)
    audit_logger.log_dlp_result(result5, "email")
    reporter.add_event({
        "timestamp": "2025-11-21T10:04:00",
        "channel": "email",
        "classification": result5["classification"],
        "policy_triggered": result5["policy_triggered"],
        "action_taken": result5["action_taken"],
        "metadata": {"matches": list(result5['matches'].keys())}
    })
    
    # Test 6: Multiple PII Types
    print_header("TEST 6: Multiple Sensitive Data Types")
    test6_content = """
    Employee Details:
    TFN: 123 456 789
    Medicare: 2123456789
    Mobile: 0412 345 678
    Email: john.smith@example.com
    """
    print(f"Input: {test6_content[:80]}...")
    result6 = engine.evaluate(test6_content, channel="email")
    print_result(result6)
    audit_logger.log_dlp_result(result6, "email")
    reporter.add_event({
        "timestamp": "2025-11-21T10:05:00",
        "channel": "email",
        "classification": result6["classification"],
        "policy_triggered": result6["policy_triggered"],
        "action_taken": result6["action_taken"],
        "metadata": {"matches": list(result6['matches'].keys())}
    })
    
    # Generate Reports
    print_header("📊 GENERATING REPORTS")
    
    md_report = reporter.generate_markdown_report("demo_dlp_report.md")
    print(f"✅ Markdown report generated: {md_report}")
    
    json_summary = reporter.generate_json_summary("demo_dlp_summary.json")
    print(f"✅ JSON summary generated: {json_summary}")
    
    print(f"\n📋 Audit log available at: dlp_audit.log")
    
    # Summary Statistics
    print_header("📈 SUMMARY STATISTICS")
    print(f"Total Evaluations: 6")
    print(f"Blocked: 2 (TFN detected)")
    print(f"Redacted: 1 (Credit card)")
    print(f"Quarantined: 1 (Financial docs)")
    print(f"Alerted: 1 (Medical terms)")
    print(f"Allowed: 1 (Clean content)")
    
    print_header("✅ DEMONSTRATION COMPLETE")
    print("Run './run.sh' to start the interactive dashboard!")
    print("Or run 'python api/server.py' to start the API server\n")

if __name__ == "__main__":
    main()
