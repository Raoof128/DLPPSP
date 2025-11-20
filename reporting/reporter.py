"""Reporting utilities for summarizing DLP events."""

import json
from datetime import datetime


class DLPReporter:
    """Generate markdown and JSON summaries of DLP audit events."""

    def __init__(self) -> None:
        self.events: list[dict] = []

    def add_event(self, event: dict) -> None:
        """Add an event to the report."""

        self.events.append(event)

    def generate_markdown_report(self, output_file: str = "dlp_report.md") -> str:
        """Generate a markdown report of DLP events."""
        report_lines = [
            "# DLP Activity Report",
            f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"\n**Total Events:** {len(self.events)}\n",
            "---\n",
        ]

        # Summary statistics
        blocked = sum(1 for e in self.events if e.get("action_taken") == "block")
        quarantined = sum(1 for e in self.events if e.get("action_taken") == "quarantine")
        redacted = sum(1 for e in self.events if e.get("action_taken") == "redact")
        alerted = sum(1 for e in self.events if e.get("action_taken") == "alert")
        allowed = sum(1 for e in self.events if e.get("action_taken") == "allow")

        report_lines.extend(
            [
                "## Summary\n",
                f"- **Blocked:** {blocked}",
                f"- **Quarantined:** {quarantined}",
                f"- **Redacted:** {redacted}",
                f"- **Alerted:** {alerted}",
                f"- **Allowed:** {allowed}\n",
                "---\n",
                "## Events\n",
            ]
        )

        # Event details
        for idx, event in enumerate(self.events, 1):
            report_lines.extend(
                [
                    f"### Event {idx}",
                    f"- **Timestamp:** {event.get('timestamp', 'N/A')}",
                    f"- **Channel:** {event.get('channel', 'N/A')}",
                    f"- **Classification:** {event.get('classification', 'N/A')}",
                    f"- **Policy Triggered:** {event.get('policy_triggered', 'None')}",
                    f"- **Action Taken:** {event.get('action_taken', 'allow')}",
                    f"- **Matches:** {', '.join(event.get('metadata', {}).get('matches', []))}",
                    "",
                ]
            )

        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(report_lines))

        return output_file

    def generate_json_summary(self, output_file: str = "dlp_summary.json") -> str:
        """Generate a JSON summary for SIEM ingestion."""
        summary = {
            "generated_at": datetime.now().isoformat(),
            "total_events": len(self.events),
            "summary": {
                "blocked": sum(1 for e in self.events if e.get("action_taken") == "block"),
                "quarantined": sum(1 for e in self.events if e.get("action_taken") == "quarantine"),
                "redacted": sum(1 for e in self.events if e.get("action_taken") == "redact"),
                "alerted": sum(1 for e in self.events if e.get("action_taken") == "alert"),
                "allowed": sum(1 for e in self.events if e.get("action_taken") == "allow"),
            },
            "events": self.events,
        }

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)

        return output_file
