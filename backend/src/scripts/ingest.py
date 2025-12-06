import os
import glob
from typing import List
from qdrant_client import models
from src.services.vector_store import get_qdrant_client
from src.services.llm import get_openai_client
from src.core.config import settings

def ingest_docs():
    client = get_qdrant_client()
    openai = get_openai_client()
    
    # Ensure collection exists
    try:
        client.get_collection("physical_ai_book")
    except Exception:
        client.create_collection(
            collection_name="physical_ai_book",
            vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE)
        )

    docs_path = os.path.join("..", "website", "docs", "*.md")
    files = glob.glob(docs_path)
    
    points = []
    idx = 0
    
    for file_path in files:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            # Naive splitting by headers or chunks
            # For MVP, just chunk by 1000 chars
            chunks = [content[i:i+1000] for i in range(0, len(content), 1000)]
            
            for chunk in chunks:
                # Embed
                emb = openai.embeddings.create(
                    input=chunk,
                    model="text-embedding-3-small"
                ).data[0].embedding
                
                points.append(models.PointStruct(
                    id=idx,
                    vector=emb,
                    payload={
                        "text": chunk,
                        "source": os.path.basename(file_path)
                    }
                ))
                idx += 1
    
    if points:
        client.upsert(
            collection_name="physical_ai_book",
            points=points
        )
        print(f"Ingested {len(points)} chunks.")

if __name__ == "__main__":
    ingest_docs()
