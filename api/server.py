import sys
import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.rules_engine import DLPEngine
from reporting.audit_logger import AuditLogger

app = FastAPI(title="DLP Platform API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DLP engine and logger
dlp_engine = DLPEngine()
audit_logger = AuditLogger()

# Request models
class EmailSimulation(BaseModel):
    sender: str
    recipient: str
    subject: str
    body: str

class ChatSimulation(BaseModel):
    message: str
    sender: str
    recipient: str

class TextSimulation(BaseModel):
    content: str
    channel: str = "generic"

@app.get("/")
def root():
    return {
        "service": "DLP Platform API",
        "version": "1.0.0",
        "status": "operational"
    }

@app.post("/simulate/email")
def simulate_email(email: EmailSimulation):
    """
    Simulates DLP scanning of an email.
    """
    # Combine email parts
    full_content = f"{email.subject}\n{email.body}"
    
    result = dlp_engine.evaluate(full_content, channel="email")
    
    # Log the event
    audit_logger.log_dlp_result(result, channel="email", user=email.sender)
    
    return {
        "email": email.dict(),
        "dlp_result": result
    }

@app.post("/simulate/chat")
def simulate_chat(chat: ChatSimulation):
    """
    Simulates DLP scanning of a chat message.
    """
    result = dlp_engine.evaluate(chat.message, channel="chat")
    
    # Log the event
    audit_logger.log_dlp_result(result, channel="chat", user=chat.sender)
    
    return {
        "chat": chat.dict(),
        "dlp_result": result
    }

@app.post("/simulate/text")
def simulate_text(text_sim: TextSimulation):
    """
    Simulates DLP scanning of arbitrary text.
    """
    result = dlp_engine.evaluate(text_sim.content, channel=text_sim.channel)
    
    # Log the event
    audit_logger.log_dlp_result(result, channel=text_sim.channel)
    
    return {
        "dlp_result": result
    }

@app.post("/simulate/file")
async def simulate_file(file: UploadFile = File(...), channel: str = Form(default="file")):
    """
    Simulates DLP scanning of an uploaded file.
    """
    # Read file content
    content = await file.read()
    
    try:
        # Try to decode as text
        text_content = content.decode('utf-8')
    except UnicodeDecodeError:
        return {
            "error": "File is not a text file. Only text files are supported in this demo."
        }
    
    result = dlp_engine.evaluate(text_content, channel="file")
    
    # Log the event
    audit_logger.log_dlp_result(result, channel="file")
    
    return {
        "filename": file.filename,
        "dlp_result": result
    }

@app.get("/policies")
def get_policies():
    """
    Returns the currently loaded policies.
    """
    return {"policies": dlp_engine.policies}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
