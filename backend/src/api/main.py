from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import chat

app = FastAPI(title="Physical AI Book RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Physical AI Book RAG API is running"}
