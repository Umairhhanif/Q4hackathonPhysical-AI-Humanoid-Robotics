from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Physical AI RAG Chatbot"
    API_SECRET: str
    
    OPENAI_API_KEY: Optional[str] = None
    GOOGLE_API_KEY: str
    
    QDRANT_URL: str
    QDRANT_API_KEY: str
    
    DATABASE_URL: str
    
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "https://q4hackathon-physical-ai-humanoid-ro.vercel.app"]

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

settings = Settings()