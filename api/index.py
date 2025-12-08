import os
import sys

# Vercel serverless function handler
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
import json

# Create FastAPI app
app = FastAPI(title="Physical AI RAG Chatbot")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    query: str
    selected_text: Optional[str] = None
    history: List[ChatMessage] = []

# Health check endpoint
@app.get("/")
@app.get("/health")
def health_check():
    env_status = {
        "GOOGLE_API_KEY": "✓" if os.getenv("GOOGLE_API_KEY") else "✗",
        "QDRANT_URL": "✓" if os.getenv("QDRANT_URL") else "✗",
        "QDRANT_API_KEY": "✓" if os.getenv("QDRANT_API_KEY") else "✗",
        "DATABASE_URL": "✓" if os.getenv("DATABASE_URL") else "✗",
        "API_SECRET": "✓" if os.getenv("API_SECRET") else "✗",
    }
    return {
        "status": "ok",
        "message": "Physical AI RAG Chatbot API",
        "environment_variables": env_status,
        "python_version": sys.version,
        "cwd": os.getcwd()
    }

# Chat endpoint
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        # Check if required env vars are present
        if not os.getenv("GOOGLE_API_KEY"):
            raise HTTPException(status_code=500, detail="GOOGLE_API_KEY not configured")
        
        # Import here to avoid startup issues
        import google.generativeai as genai
        
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        async def event_generator():
            try:
                # Simple response without RAG for now (to test basic functionality)
                system_prompt = """You are an expert assistant for the 'Physical AI & Humanoid Robotics' book.
Answer the user's question helpfully and concisely."""
                
                full_prompt = f"{system_prompt}\n\nQuestion: {request.query}"
                
                # Generate streaming response
                response = model.generate_content(full_prompt, stream=True)
                
                full_response = ""
                for chunk in response:
                    if chunk.text:
                        full_response += chunk.text
                        yield f"data: {json.dumps({'type': 'token', 'data': chunk.text})}\n\n"
                
                yield "data: [DONE]\n\n"
                
            except Exception as e:
                yield f"data: {json.dumps({'type': 'error', 'data': str(e)})}\n\n"
        
        return StreamingResponse(event_generator(), media_type="text/event-stream")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Vercel requires the app to be exported
handler = app
