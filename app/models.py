from pydantic import BaseModel
from typing import Optional, List

class ChatRequest(BaseModel):
    context: str
    question: str
    conversation_history: Optional[List[dict]] = None
    language: Optional[str] = "en"  # "en", "si", or "ta"

class ChatResponse(BaseModel):
    answer: str
    context_used: str
    success: bool
    error: Optional[str] = None