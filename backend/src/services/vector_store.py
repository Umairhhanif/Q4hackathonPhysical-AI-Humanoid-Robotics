from qdrant_client import QdrantClient
from src.core.config import settings

class VectorStore:
    _client: QdrantClient = None

    @classmethod
    def get_client(cls) -> QdrantClient:
        if cls._client is None:
            cls._client = QdrantClient(
                url=settings.QDRANT_URL,
                api_key=settings.QDRANT_API_KEY,
            )
        return cls._client

    @classmethod
    def get_collection_name(cls) -> str:
        return "book_content_gemini"

    @classmethod
    def ensure_collection(cls):
        client = cls.get_client()
        collection_name = cls.get_collection_name()
        
        collections = client.get_collections().collections
        exists = any(c.name == collection_name for c in collections)
        
        if not exists:
            from qdrant_client.http import models
            client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=768,  # Google Gemini text-embedding-004
                    distance=models.Distance.COSINE
                )
            )
            print(f"Created collection: {collection_name}")
        else:
            print(f"Collection {collection_name} already exists")

def get_vector_client() -> QdrantClient:
    return VectorStore.get_client()