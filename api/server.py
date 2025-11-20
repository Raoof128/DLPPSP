"""FastAPI server exposing simulation endpoints for the DLP engine."""

from __future__ import annotations

import logging
import os
import sys

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

# Add parent directory to path for imports when running without package install
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.rules_engine import DLPEngine
from reporting.audit_logger import AuditLogger

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
LOGGER = logging.getLogger(__name__)


class APISettings(BaseSettings):
    """Runtime configuration for the API service."""

    policies_path: str = Field(
        default="config/policies.yaml", description="Path to the policy configuration file"
    )
    patterns_path: str = Field(
        default="config/patterns_au.json", description="Path to the regex patterns file"
    )

    class Config:
        env_prefix = "DLP_"


UPLOAD_FILE_FIELD = File(...)

settings = APISettings()

app = FastAPI(title="DLP Platform API", version="1.0.0", description="DLP policy simulator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine_config = {"policies_path": settings.policies_path, "patterns_path": settings.patterns_path}
dlp_engine = DLPEngine(**engine_config)
audit_logger = AuditLogger()


class EmailSimulation(BaseModel):
    sender: str = Field(min_length=3, description="Email sender identifier")
    recipient: str = Field(min_length=3, description="Email recipient identifier")
    subject: str = Field(min_length=1, description="Email subject line")
    body: str = Field(min_length=1, description="Email body content")


class ChatSimulation(BaseModel):
    message: str = Field(min_length=1, description="Chat message content")
    sender: str = Field(min_length=3, description="Sender identifier")
    recipient: str = Field(min_length=3, description="Recipient identifier")


class TextSimulation(BaseModel):
    content: str = Field(min_length=1, description="Text payload to evaluate")
    channel: str = Field(
        default="generic", min_length=3, description="Channel name for policy matching"
    )


@app.get("/")
def root() -> dict[str, str]:
    """Return service metadata for simple health verification."""

    return {"service": "DLP Platform API", "version": "1.0.0", "status": "operational"}


@app.post("/simulate/email")
def simulate_email(email: EmailSimulation) -> dict[str, object]:
    """Simulate DLP scanning of an email payload."""

    full_content = f"{email.subject}\n{email.body}"
    result = dlp_engine.evaluate(full_content, channel="email")
    audit_logger.log_dlp_result(result, channel="email", user=email.sender)
    return {"email": email.dict(), "dlp_result": result}


@app.post("/simulate/chat")
def simulate_chat(chat: ChatSimulation) -> dict[str, object]:
    """Simulate DLP scanning of a chat message."""

    result = dlp_engine.evaluate(chat.message, channel="chat")
    audit_logger.log_dlp_result(result, channel="chat", user=chat.sender)
    return {"chat": chat.dict(), "dlp_result": result}


@app.post("/simulate/text")
def simulate_text(text_sim: TextSimulation) -> dict[str, object]:
    """Simulate DLP scanning of arbitrary text."""

    result = dlp_engine.evaluate(text_sim.content, channel=text_sim.channel)
    audit_logger.log_dlp_result(result, channel=text_sim.channel)
    return {"dlp_result": result}


@app.post("/simulate/file")
async def simulate_file(
    file: UploadFile = UPLOAD_FILE_FIELD, channel: str = Form(default="file")
) -> dict[str, object]:
    """Simulate DLP scanning of an uploaded text file."""

    content = await file.read()
    try:
        text_content = content.decode("utf-8")
    except UnicodeDecodeError as exc:
        LOGGER.error("Rejected non-text upload: %s", file.filename)
        raise HTTPException(
            status_code=400,
            detail="File is not a text file. Only UTF-8 text files are supported in this demo.",
        ) from exc

    result = dlp_engine.evaluate(text_content, channel=channel)
    audit_logger.log_dlp_result(result, channel=channel)
    return {"filename": file.filename, "dlp_result": result}


@app.get("/policies")
def get_policies() -> dict[str, object]:
    """Return the currently loaded policies for inspection."""

    return {"policies": dlp_engine.policies}


@app.get("/health")
def health_check() -> dict[str, str]:
    """Simple health check endpoint used by orchestrators."""

    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
