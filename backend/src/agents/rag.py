from src.services.vector_store import get_qdrant_client
from src.services.llm import get_openai_client
from src.models.chat import ChatResponse, Citation

def generate_answer(query: str) -> ChatResponse:
    qdrant = get_qdrant_client()
    openai = get_openai_client()
    
    # 1. Embed query
    emb = openai.embeddings.create(
        input=query,
        model="text-embedding-3-small"
    ).data[0].embedding
    
    # 2. Search
    search_result = qdrant.search(
        collection_name="physical_ai_book",
        query_vector=emb,
        limit=3
    )
    
    context = "\n\n".join([hit.payload["text"] for hit in search_result])
    sources = [Citation(source=hit.payload["source"], text=hit.payload["text"][:100]+"...") for hit in search_result]
    
    # 3. Generate
    prompt = f"""
    You are an expert on Physical AI and Humanoid Robotics.
    Answer the user's question strictly based on the context below.
    If the answer is not in the context, say "I don't know based on the book content."
    
    Context:
    {context}
    
    Question: {query}
    """
    
    completion = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return ChatResponse(
        answer=completion.choices[0].message.content,
        citations=sources
    )
