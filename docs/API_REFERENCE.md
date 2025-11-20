# API Reference

This document summarizes the FastAPI endpoints exposed by the DLP Policy Simulation Platform.

## Base URL

```
http://localhost:8000
```

## Endpoints

### `GET /`
Returns service metadata and uptime indicator.

### `GET /health`
Simple health check used by orchestrators.

### `GET /policies`
Returns the policies loaded from `config/policies.yaml`.

Response example:
```json
{
  "policies": [
    {
      "name": "block_tfn_external",
      "match": ["TFN"],
      "channel": ["email", "chat", "file"],
      "action": "block",
      "severity": "high"
    }
  ]
}
```

### `POST /simulate/email`
Simulate an email payload and evaluate DLP enforcement.

Request body:
```json
{
  "sender": "alice@example.com",
  "recipient": "bob@example.com",
  "subject": "Quarterly results",
  "body": "Include TFN 123 456 789"
}
```

### `POST /simulate/chat`
Simulate a chat message.

Request body:
```json
{
  "sender": "alice",
  "recipient": "bob",
  "message": "Patient diagnosis is pending"
}
```

### `POST /simulate/text`
Evaluate arbitrary text for a specified channel.

Request body:
```json
{
  "content": "This is clean",
  "channel": "email"
}
```

### `POST /simulate/file`
Upload a text file for scanning. Non-text uploads are rejected.

Form fields:
- `file`: the text file
- `channel`: optional override for policy channel (defaults to `file`)

## Response Structure

All simulation endpoints return a consistent structure:

```json
{
  "dlp_result": {
    "classification": "Restricted",
    "matches": {"ABN": ["12 345 678 901"]},
    "policy_triggered": "quarantine_financial",
    "action_taken": "quarantine",
    "action_result": {"status": "quarantined", "location": "quarantine/20241001_...txt"},
    "processed_content": null
  }
}
```

- `classification`: sensitivity label assigned by the classifier.
- `matches`: detected PII grouped by type.
- `policy_triggered`: name of the policy that matched (if any).
- `action_taken`: final enforcement action (defaults to `allow`).
- `action_result`: action-specific metadata (e.g., quarantine location).
- `processed_content`: redacted text when `redact` action is applied.

## Error Handling

- Non-text uploads return a structured error message.
- Invalid payloads are validated by Pydantic request models.
- Server-side exceptions are logged for observability.

