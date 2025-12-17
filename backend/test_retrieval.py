"""
Test script to check if Qdrant retrieval is working
"""
import sys
import asyncio
sys.path.append('src')

from src.services.vector_store import VectorStore
from src.services.llm import get_cohere_embedding

async def test_retrieval():
    print("Testing Qdrant retrieval...")
    client = VectorStore.get_client()
    collection_name = VectorStore.get_collection_name()
    
    # Test query
    query = "What is ROS2?"
    print(f"\nQuery: {query}")
    
    # Generate embedding
    print("Generating embedding...")
    embedding = await get_cohere_embedding(query)
    print(f"Embedding dimension: {len(embedding)}")
    
    # Search with NO threshold to see if we get any results
    print("\nSearching Qdrant (no threshold)...")
    results = client.query_points(
        collection_name=collection_name,
        query=embedding,
        limit=5
    ).points
    
    print(f"\nFound {len(results)} results:")
    for i, hit in enumerate(results):
        print(f"\n{i+1}. Score: {hit.score:.4f}")
        print(f"   Source: {hit.payload.get('source', 'N/A')}")
        print(f"   Title: {hit.payload.get('title', 'N/A')}")
        print(f"   Text preview: {hit.payload.get('text', '')[:100]}...")

if __name__ == "__main__":
    asyncio.run(test_retrieval())
