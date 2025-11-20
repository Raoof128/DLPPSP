# Changelog

All notable changes to the DLP Platform will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-21

### Added

#### Core Engine
- **PII Detector** with Australian-specific patterns:
  - Tax File Number (TFN)
  - Medicare Number
  - ABN/ACN (Australian Business/Company Number)
  - Credit Card numbers (Luhn validation)
  - Australian mobile numbers
  - Email addresses
  - Medical terminology
  - Financial keywords

- **Data Classifier** with four-tier classification:
  - Highly Sensitive
  - Restricted
  - Internal
  - Public

- **Rules Engine** supporting:
  - YAML-based policy definitions
  - Multi-channel enforcement (email, chat, file)
  - Priority-based policy resolution

- **Action Handler** with enforcement capabilities:
  - Block (reject transmission)
  - Quarantine (isolate content)
  - Redact (mask sensitive data)
  - Alert (log and notify)
  - Allow (permit with logging)

#### API & Dashboard
- **FastAPI REST API** with endpoints:
  - `/simulate/email` - Email DLP testing
  - `/simulate/chat` - Chat message testing
  - `/simulate/text` - Generic text analysis
  - `/simulate/file` - File upload scanning
  - `/policies` - View active policies
  - `/health` - Health check

- **Streamlit Dashboard** featuring:
  - Interactive testing interface
  - Real-time policy visualization
  - Multi-mode simulation (text/email/file/chat)
  - Results display with color-coded classification
  - Report generation buttons

#### Reporting & Logging
- **Audit Logger** for compliance:
  - JSON-formatted log entries
  - Timestamp, user, channel tracking
  - Policy and action metadata

- **Report Generator** with formats:
  - Markdown reports for human review
  - JSON summaries for SIEM integration

#### Configuration
- `patterns_au.json` - Australian PII regex patterns
- `policies.yaml` - DLP policy definitions

#### Testing
- Unit test suite with 19 tests:
  - PII detector tests (7 tests)
  - Classifier tests (7 tests)
  - Rules engine tests (5 tests)
- Sample data files for validation
- Comprehensive demo script

#### DevOps
- Docker support:
  - `Dockerfile.api` for API service
  - `Dockerfile.dashboard` for UI service
  - `docker-compose.yml` for full stack
- Quick start script (`run.sh`)
- Python virtual environment setup

#### Documentation
- Comprehensive README with:
  - Architecture diagrams (Mermaid)
  - Usage examples
  - API documentation
  - Security considerations
  - Compliance context (APRA, Privacy Act, ISO 27001)
- CONTRIBUTING.md for collaboration guidelines
- SECURITY.md for vulnerability reporting
- LICENSE (MIT)

### Security Considerations

⚠️ **Important**: This v1.0.0 release is designed for:
- **Portfolio demonstration**
- **Educational purposes**
- **Testing and validation**
- **Proof-of-concept**

It is **NOT production-ready** without additional security hardening (see SECURITY.md).

### Dependencies

- Python 3.11+
- FastAPI 0.115.0
- Streamlit 1.39.0
- Uvicorn 0.32.0
- PyYAML 6.0.2
- Pydantic 2.9.2

### Known Limitations

- Regex patterns can be bypassed with encoding/obfuscation
- No authentication or authorization
- No encryption at rest or in transit
- Local file storage only (no database)
- Limited to text files (no binary scanning)
- English language only

### Future Roadmap

Planned for future releases:
- [ ] Machine learning-based detection
- [ ] Binary file support (PDF, DOCX)
- [ ] Multi-language support
- [ ] Azure Information Protection integration
- [ ] Custom pattern builder UI
- [ ] Historical analytics dashboard
- [ ] Production hardening (auth, encryption, etc.)

---

## Release Notes Format

For future releases, use:

### [Version] - YYYY-MM-DD

#### Added
- New features

#### Changed
- Changes to existing functionality

#### Deprecated
- Soon-to-be removed features

#### Removed
- Removed features

#### Fixed
- Bug fixes

#### Security
- Security improvements or patches

---

[1.0.0]: https://github.com/yourusername/dlp_platform/releases/tag/v1.0.0
