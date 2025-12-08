from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime

class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str

class ChatRequest(BaseModel):
    query: str
    selected_text: Optional[str] = None
    history: List[ChatMessage] = []

class SourceReference(BaseModel):
    source_file: str
    header_path: Optional[str] = None
    snippet: str
    score: float

class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceReference] = []

class IngestResponse(BaseModel):
    status: str
    chunks_processed: int
    message: str
