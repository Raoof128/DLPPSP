import os
import sys

import streamlit as st

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.rules_engine import DLPEngine
from reporting.audit_logger import AuditLogger
from reporting.reporter import DLPReporter

# Page configuration
st.set_page_config(
    page_title="DLP Policy Simulation Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown(
    """
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .danger-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Initialize session state
if "dlp_engine" not in st.session_state:
    st.session_state.dlp_engine = DLPEngine()

if "audit_logger" not in st.session_state:
    st.session_state.audit_logger = AuditLogger()

if "reporter" not in st.session_state:
    st.session_state.reporter = DLPReporter()

# Header
st.markdown(
    '<div class="main-header">🛡️ Data Loss Prevention (DLP) Policy Simulation Platform</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sub-header">Enterprise-grade DLP testing and compliance validation for Australian data protection</div>',
    unsafe_allow_html=True,
)

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")

    simulation_mode = st.selectbox(
        "Select Simulation Mode",
        ["Text Analysis", "Email Simulation", "File Upload", "Chat Message"],
    )

    st.divider()

    st.header("📋 Loaded Policies")
    for idx, policy in enumerate(st.session_state.dlp_engine.policies, 1):
        with st.expander(f"{idx}. {policy['name']}"):
            st.write(f"**Action:** {policy['action']}")
            st.write(f"**Channels:** {', '.join(policy['channel'])}")
            st.write(f"**Matches:** {', '.join(policy['match'])}")
            st.write(f"**Severity:** {policy['severity']}")

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📥 Input")

    if simulation_mode == "Text Analysis":
        text_input = st.text_area(
            "Enter text to analyze",
            height=300,
            placeholder="Paste content here (e.g., emails, documents, chat messages)...",
        )
        channel = st.selectbox("Channel", ["email", "chat", "file"])

        if st.button("🔍 Analyze", type="primary", use_container_width=True):
            if text_input:
                result = st.session_state.dlp_engine.evaluate(text_input, channel)
                st.session_state.last_result = result
                st.session_state.audit_logger.log_dlp_result(result, channel)
                st.session_state.reporter.add_event(
                    {
                        "timestamp": st.session_state.audit_logger.log_dlp_result(
                            result, channel
                        ).get("timestamp"),
                        "channel": channel,
                        "classification": result.get("classification"),
                        "policy_triggered": result.get("policy_triggered"),
                        "action_taken": result.get("action_taken"),
                        "metadata": {"matches": list(result.get("matches", {}).keys())},
                    }
                )
            else:
                st.warning("Please enter some text to analyze.")

    elif simulation_mode == "Email Simulation":
        sender = st.text_input("From", placeholder="sender@example.com")
        recipient = st.text_input("To", placeholder="recipient@example.com")
        subject = st.text_input("Subject", placeholder="Email subject")
        body = st.text_area("Body", height=200, placeholder="Email body content...")

        if st.button("📧 Send Email (Simulate)", type="primary", use_container_width=True):
            if sender and recipient and subject and body:
                full_content = f"{subject}\n{body}"
                result = st.session_state.dlp_engine.evaluate(full_content, "email")
                st.session_state.last_result = result
                st.session_state.audit_logger.log_dlp_result(result, "email", user=sender)
                st.session_state.reporter.add_event(
                    {
                        "timestamp": st.session_state.audit_logger.log_dlp_result(
                            result, "email", user=sender
                        ).get("timestamp"),
                        "channel": "email",
                        "classification": result.get("classification"),
                        "policy_triggered": result.get("policy_triggered"),
                        "action_taken": result.get("action_taken"),
                        "metadata": {"matches": list(result.get("matches", {}).keys())},
                    }
                )
            else:
                st.warning("Please fill in all email fields.")

    elif simulation_mode == "File Upload":
        uploaded_file = st.file_uploader("Upload a text file", type=["txt", "csv", "log"])

        if uploaded_file is not None:
            content = uploaded_file.read().decode("utf-8")
            st.text_area(
                "File Preview", content[:500] + "..." if len(content) > 500 else content, height=200
            )

            if st.button("🔍 Scan File", type="primary", use_container_width=True):
                result = st.session_state.dlp_engine.evaluate(content, "file")
                st.session_state.last_result = result
                st.session_state.audit_logger.log_dlp_result(result, "file")
                st.session_state.reporter.add_event(
                    {
                        "timestamp": st.session_state.audit_logger.log_dlp_result(
                            result, "file"
                        ).get("timestamp"),
                        "channel": "file",
                        "classification": result.get("classification"),
                        "policy_triggered": result.get("policy_triggered"),
                        "action_taken": result.get("action_taken"),
                        "metadata": {"matches": list(result.get("matches", {}).keys())},
                    }
                )

    elif simulation_mode == "Chat Message":
        sender = st.text_input("Sender", placeholder="user123")
        recipient = st.text_input("Recipient", placeholder="user456")
        message = st.text_area("Message", height=200, placeholder="Chat message content...")

        if st.button("💬 Send Message (Simulate)", type="primary", use_container_width=True):
            if sender and recipient and message:
                result = st.session_state.dlp_engine.evaluate(message, "chat")
                st.session_state.last_result = result
                st.session_state.audit_logger.log_dlp_result(result, "chat", user=sender)
                st.session_state.reporter.add_event(
                    {
                        "timestamp": st.session_state.audit_logger.log_dlp_result(
                            result, "chat", user=sender
                        ).get("timestamp"),
                        "channel": "chat",
                        "classification": result.get("classification"),
                        "policy_triggered": result.get("policy_triggered"),
                        "action_taken": result.get("action_taken"),
                        "metadata": {"matches": list(result.get("matches", {}).keys())},
                    }
                )
            else:
                st.warning("Please fill in all fields.")

with col2:
    st.header("📊 Results")

    if "last_result" in st.session_state:
        result = st.session_state.last_result

        # Classification
        classification = result.get("classification", "Unknown")

        if classification == "Highly Sensitive":
            st.markdown(
                f'<div class="danger-box"><strong>🔴 Classification:</strong> {classification}</div>',
                unsafe_allow_html=True,
            )
        elif classification == "Restricted":
            st.markdown(
                f'<div class="warning-box"><strong>🟡 Classification:</strong> {classification}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="success-box"><strong>🟢 Classification:</strong> {classification}</div>',
                unsafe_allow_html=True,
            )

        # Matches
        st.subheader("🎯 Detected PII/Sensitive Data")
        matches = result.get("matches", {})
        if matches:
            for pii_type, values in matches.items():
                st.write(f"**{pii_type}:** {len(values)} match(es)")
                with st.expander("View matches"):
                    for val in values:
                        st.code(val)
        else:
            st.info("No sensitive data detected.")

        # Policy
        st.subheader("⚖️ Policy Decision")
        policy = result.get("policy_triggered")
        action = result.get("action_taken", "allow")

        if policy:
            st.write(f"**Policy Triggered:** `{policy}`")
        else:
            st.write("**Policy Triggered:** None (No violation)")

        st.write(f"**Action Taken:** `{action.upper()}`")

        # Action result
        action_result = result.get("action_result", {})
        if action_result:
            st.json(action_result)

        # Processed content
        st.subheader("📄 Processed Content")
        processed = result.get("processed_content")
        if processed:
            st.text_area("Output", processed, height=200)
        else:
            st.warning("Content was blocked or quarantined.")

    else:
        st.info("👈 Submit content on the left to see DLP analysis results here.")

# Footer
st.divider()
col_a, col_b, col_c = st.columns(3)

with col_a:
    if st.button("📄 Generate Markdown Report", use_container_width=True):
        report_file = st.session_state.reporter.generate_markdown_report()
        st.success(f"Report generated: {report_file}")

with col_b:
    if st.button("📊 Generate JSON Summary", use_container_width=True):
        summary_file = st.session_state.reporter.generate_json_summary()
        st.success(f"Summary generated: {summary_file}")

with col_c:
    if st.button("🔄 Reset Session", use_container_width=True):
        st.session_state.reporter = DLPReporter()
        if "last_result" in st.session_state:
            del st.session_state.last_result
        st.success("Session reset!")
        st.rerun()
