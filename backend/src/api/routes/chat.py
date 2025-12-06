from fastapi import APIRouter, HTTPException
from src.models.chat import ChatQuery, ChatResponse
from src.agents.rag import generate_answer

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(query: ChatQuery):
    try:
        return generate_answer(query.query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
