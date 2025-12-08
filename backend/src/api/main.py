from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import settings

from src.api.routes import ingest, chat

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(ingest.router, prefix=settings.API_V1_STR, tags=["ingest"])
app.include_router(chat.router, prefix=settings.API_V1_STR, tags=["chat"])

@app.get("/")
def root():
    return {"message": "Welcome to Physical AI RAG Chatbot API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}