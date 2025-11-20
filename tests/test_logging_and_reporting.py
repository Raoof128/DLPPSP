from pathlib import Path

from reporting.audit_logger import AuditLogger
from reporting.reporter import DLPReporter


def test_audit_logger_writes_file(tmp_path: Path):
    log_file = tmp_path / "audit.log"
    logger = AuditLogger(log_file=str(log_file))

    result = logger.log_event(
        event_type="dlp_evaluation",
        channel="email",
        classification="Highly Sensitive",
        policy="block_tfn_external",
        action="block",
        user="tester",
        metadata={"matches": ["TFN"]},
    )

    assert result["policy_triggered"] == "block_tfn_external"
    assert log_file.exists()
    assert log_file.read_text(encoding="utf-8") != ""


def test_reporter_outputs(tmp_path: Path):
    reporter = DLPReporter()
    reporter.add_event(
        {
            "timestamp": "2024-01-01T00:00:00",
            "channel": "email",
            "classification": "Restricted",
            "policy_triggered": "alert_medical_terms",
            "action_taken": "alert",
            "metadata": {"matches": ["Medical_Terms"]},
        }
    )

    md_path = reporter.generate_markdown_report(output_file=str(tmp_path / "report.md"))
    json_path = reporter.generate_json_summary(output_file=str(tmp_path / "report.json"))

    assert Path(md_path).exists()
    assert Path(json_path).exists()
    assert "alert_medical_terms" in Path(md_path).read_text(encoding="utf-8")
