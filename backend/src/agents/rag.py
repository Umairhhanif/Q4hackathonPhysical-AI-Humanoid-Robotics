"""
RAG agent using Cohere for embeddings and chat.
"""

import cohere
from src.services.vector_store import get_qdrant_client
from src.core.config import settings
from src.models.chat import ChatResponse, Citation

# Create Cohere client
def get_cohere_client() -> cohere.ClientV2:
    return cohere.ClientV2(api_key=settings.COHERE_API_KEY)


def generate_answer(query: str) -> ChatResponse:
    qdrant = get_qdrant_client()
    co = get_cohere_client()
    
    # 1. Embed query using Cohere
    emb_response = co.embed(
        texts=[query],
        model="embed-english-v3.0",
        input_type="search_query",
        embedding_types=["float"]
    )
    emb = emb_response.embeddings.float_[0]
    
    # 2. Search using query method (qdrant-client v1.16+)
    search_result = qdrant.query_points(
        collection_name="physical_ai_book",
        query=emb,
        limit=3
    ).points
    
    # Handle case where no results are found
    if not search_result:
        return ChatResponse(
            answer="I couldn't find relevant information in the book content.",
            citations=[]
        )
    
    context = "\n\n".join([hit.payload["text"] for hit in search_result])
    sources = [Citation(source=hit.payload["source"], text=hit.payload["text"][:100]+"...") for hit in search_result]
    
    # 3. Generate using Cohere
    system_message = """You are an expert on Physical AI and Humanoid Robotics.
Answer the user's question strictly based on the context provided.
If the answer is not in the context, say "I don't know based on the book content."
Be concise and helpful."""

    response = co.chat(
        model="command-a-03-2025",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
        ]
    )
    
    return ChatResponse(
        answer=response.message.content[0].text,
        citations=sources
    )
