"""
Ingestion script for Physical AI Book content into Qdrant.
This script reads markdown files from the website/docs folder,
chunks them, generates embeddings using Cohere, and stores them in Qdrant.
"""

import os
import re
from pathlib import Path
from typing import List, Dict
import cohere
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import uuid

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configuration
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "")
COHERE_API_KEY = os.getenv("COHERE_API_KEY", "")
COLLECTION_NAME = "physical_ai_book"
DOCS_PATH = Path(__file__).parent.parent.parent.parent / "website" / "docs"
CHUNK_SIZE = 1000  # characters per chunk
CHUNK_OVERLAP = 200  # overlap between chunks

# Cohere embed-english-v3.0 has 1024 dimensions
EMBEDDING_DIMENSION = 1024


def get_qdrant_client() -> QdrantClient:
    """Create and return Qdrant client."""
    return QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY if QDRANT_API_KEY else None
    )


def get_cohere_client() -> cohere.ClientV2:
    """Create and return Cohere client."""
    return cohere.ClientV2(api_key=COHERE_API_KEY)


def clean_markdown(text: str) -> str:
    """Remove markdown formatting for cleaner text."""
    # Remove code blocks
    text = re.sub(r'```[\s\S]*?```', '', text)
    # Remove inline code
    text = re.sub(r'`[^`]+`', '', text)
    # Remove images
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    # Remove links but keep text
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove frontmatter
    text = re.sub(r'^---[\s\S]*?---', '', text)
    # Clean up extra whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    text_len = len(text)
    
    while start < text_len:
        end = start + chunk_size
        
        # Try to end at a sentence or paragraph boundary
        if end < text_len:
            # Look for paragraph break
            para_break = text.rfind('\n\n', start, end)
            if para_break > start + chunk_size // 2:
                end = para_break
            else:
                # Look for sentence break
                sentence_break = text.rfind('. ', start, end)
                if sentence_break > start + chunk_size // 2:
                    end = sentence_break + 1
        
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        start = end - overlap if end < text_len else text_len
    
    return chunks


def read_markdown_files(docs_path: Path) -> List[Dict]:
    """Read all markdown files and return list of documents."""
    documents = []
    
    for md_file in docs_path.rglob("*.md"):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract title from first heading or filename
            title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            title = title_match.group(1) if title_match else md_file.stem
            
            # Get relative path for source reference
            relative_path = md_file.relative_to(docs_path)
            
            # Clean and chunk the content
            cleaned_content = clean_markdown(content)
            chunks = chunk_text(cleaned_content)
            
            for i, chunk in enumerate(chunks):
                documents.append({
                    "text": chunk,
                    "source": str(relative_path),
                    "title": title,
                    "chunk_index": i,
                    "total_chunks": len(chunks)
                })
            
            print(f"✓ Processed: {relative_path} ({len(chunks)} chunks)")
            
        except Exception as e:
            print(f"✗ Error processing {md_file}: {e}")
    
    return documents


def generate_embeddings(co: cohere.ClientV2, texts: List[str]) -> List[List[float]]:
    """Generate embeddings for a list of texts using Cohere."""
    embeddings = []
    batch_size = 96  # Cohere allows up to 96 texts per request
    
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        try:
            response = co.embed(
                texts=batch,
                model="embed-english-v3.0",
                input_type="search_document",
                embedding_types=["float"]
            )
            embeddings.extend(response.embeddings.float_)
            print(f"  Generated embeddings: {min(i + batch_size, len(texts))}/{len(texts)}")
                
        except Exception as e:
            print(f"  Error generating embeddings for batch starting at {i}: {e}")
            # Return zero vectors as fallback
            embeddings.extend([[0.0] * EMBEDDING_DIMENSION for _ in batch])
    
    return embeddings


def create_collection(client: QdrantClient, collection_name: str, vector_size: int = EMBEDDING_DIMENSION):
    """Create Qdrant collection if it doesn't exist."""
    collections = client.get_collections().collections
    collection_names = [c.name for c in collections]
    
    if collection_name in collection_names:
        print(f"Collection '{collection_name}' already exists. Deleting and recreating...")
        client.delete_collection(collection_name)
    
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
    )
    print(f"✓ Created collection: {collection_name}")


def ingest_documents(client: QdrantClient, collection_name: str, documents: List[Dict], embeddings: List[List[float]]):
    """Ingest documents into Qdrant."""
    points = []
    
    for i, (doc, embedding) in enumerate(zip(documents, embeddings)):
        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={
                "text": doc["text"],
                "source": doc["source"],
                "title": doc["title"],
                "chunk_index": doc["chunk_index"],
                "total_chunks": doc["total_chunks"]
            }
        )
        points.append(point)
    
    # Upsert in batches
    batch_size = 100
    for i in range(0, len(points), batch_size):
        batch = points[i:i + batch_size]
        client.upsert(collection_name=collection_name, points=batch)
        print(f"  Uploaded batch {i // batch_size + 1}/{(len(points) + batch_size - 1) // batch_size}")
    
    print(f"✓ Ingested {len(points)} document chunks")


def main():
    print("=" * 60)
    print("Physical AI Book Ingestion Script (Cohere)")
    print("=" * 60)
    
    # Validate configuration
    if not COHERE_API_KEY:
        print("✗ Error: COHERE_API_KEY not set in environment")
        return
    
    if not QDRANT_URL:
        print("✗ Error: QDRANT_URL not set in environment")
        return
    
    print(f"\nConfiguration:")
    print(f"  Qdrant URL: {QDRANT_URL}")
    print(f"  Docs Path: {DOCS_PATH}")
    print(f"  Collection: {COLLECTION_NAME}")
    print(f"  Embedding Model: embed-english-v3.0 ({EMBEDDING_DIMENSION} dimensions)")
    
    # Step 1: Read documents
    print(f"\n[1/4] Reading markdown files from {DOCS_PATH}...")
    if not DOCS_PATH.exists():
        print(f"✗ Error: Docs path does not exist: {DOCS_PATH}")
        return
    
    documents = read_markdown_files(DOCS_PATH)
    print(f"✓ Total document chunks: {len(documents)}")
    
    if not documents:
        print("✗ No documents found!")
        return
    
    # Step 2: Generate embeddings
    print(f"\n[2/4] Generating embeddings using Cohere...")
    co = get_cohere_client()
    texts = [doc["text"] for doc in documents]
    embeddings = generate_embeddings(co, texts)
    print(f"✓ Generated {len(embeddings)} embeddings")
    
    # Step 3: Connect to Qdrant and create collection
    print(f"\n[3/4] Connecting to Qdrant and creating collection...")
    client = get_qdrant_client()
    create_collection(client, COLLECTION_NAME, vector_size=len(embeddings[0]))
    
    # Step 4: Ingest documents
    print(f"\n[4/4] Ingesting documents into Qdrant...")
    ingest_documents(client, COLLECTION_NAME, documents, embeddings)
    
    print("\n" + "=" * 60)
    print("✓ Ingestion complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
