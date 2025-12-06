from pydantic import BaseModel
from typing import List, Optional

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatQuery(BaseModel):
    query: str
    history: Optional[List[ChatMessage]] = []

class Citation(BaseModel):
    source: str
    text: str

class ChatResponse(BaseModel):
    answer: str
    citations: List[Citation]
