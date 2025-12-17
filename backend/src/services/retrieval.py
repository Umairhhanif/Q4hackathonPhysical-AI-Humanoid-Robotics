from src.services.vector_store import VectorStore
from src.services.llm import get_cohere_embedding  # Changed to use Cohere
from src.models.api import SourceReference
from typing import List, Optional

async def retrieve_context(query: str, selected_text: Optional[str] = None, top_k: int = 5) -> List[SourceReference]:
    client = VectorStore.get_client()
    collection_name = VectorStore.get_collection_name()
    
    # Ensure collection exists to avoid crash if not ingested yet
    VectorStore.ensure_collection()

    # If selected_text is provided, we might want to prioritize it or use it for retrieval
    # For now, let's combine them for the search vector if selected_text is short, 
    # or just use query but filter?
    # Better: Use query for retrieval, but if selected_text is present, we might want to find where it is.
    # Plan says: "Perform retrieval using the selected_text + query as the search vector"
    
    search_text = query
    if selected_text:
        search_text = f"{selected_text}\n\n{query}"

    embedding = await get_cohere_embedding(search_text)  # Changed to Cohere

    search_result = client.query_points(
        collection_name=collection_name,
        query=embedding,
        limit=top_k,
        score_threshold=0.3  # Lowered from 0.7 to allow more results
    ).points

    sources = []
    for hit in search_result:
        payload = hit.payload
        sources.append(SourceReference(
            source_file=payload.get("source", "unknown"),  # Changed from source_file
            header_path=payload.get("title"),  # Changed from header_path
            snippet=payload.get("text", ""),  # Changed from content
            score=hit.score
        ))
    
    return sources
