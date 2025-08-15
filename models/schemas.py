# models/schemas.py
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class TranscriptionResult(BaseModel):
    text: str
    confidence: Optional[float] = None
    success: bool = True

class LLMResponse(BaseModel):
    text: str
    success: bool = True

class TTSResponse(BaseModel):
    audio_url: str
    success: bool = True

class ChatResponse(BaseModel):
    audio_url: str
    success: bool = True
    message: Optional[str] = None

class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    message: str

class SessionData(BaseModel):
    session_id: str
    history: List[Dict[str, Any]] = []
    created_at: str
    last_accessed: str
