# DLP Activity Report

**Generated:** 2025-11-21 10:12:35

**Total Events:** 6

---

## Summary

- **Blocked:** 3
- **Quarantined:** 0
- **Redacted:** 1
- **Alerted:** 1
- **Allowed:** 1

---

## Events

### Event 1
- **Timestamp:** 2025-11-21T10:00:00
- **Channel:** email
- **Classification:** Highly Sensitive
- **Policy Triggered:** block_tfn_external
- **Action Taken:** block
- **Matches:** TFN, ACN

### Event 2
- **Timestamp:** 2025-11-21T10:01:00
- **Channel:** email
- **Classification:** Highly Sensitive
- **Policy Triggered:** redact_credit_cards
- **Action Taken:** redact
- **Matches:** CreditCard

### Event 3
- **Timestamp:** 2025-11-21T10:02:00
- **Channel:** chat
- **Classification:** Internal
- **Policy Triggered:** alert_medical_terms
- **Action Taken:** alert
- **Matches:** Medical_Terms

### Event 4
- **Timestamp:** 2025-11-21T10:03:00
- **Channel:** file
- **Classification:** Highly Sensitive
- **Policy Triggered:** block_tfn_external
- **Action Taken:** block
- **Matches:** TFN, ABN, ACN, Financial_Terms

### Event 5
- **Timestamp:** 2025-11-21T10:04:00
- **Channel:** email
- **Classification:** Public
- **Policy Triggered:** None
- **Action Taken:** allow
- **Matches:** 

### Event 6
- **Timestamp:** 2025-11-21T10:05:00
- **Channel:** email
- **Classification:** Highly Sensitive
- **Policy Triggered:** block_tfn_external
- **Action Taken:** block
- **Matches:** TFN, Medicare, ACN, Mobile, Email
