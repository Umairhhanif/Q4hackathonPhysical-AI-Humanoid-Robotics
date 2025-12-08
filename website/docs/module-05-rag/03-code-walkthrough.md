---
sidebar_position: 3
---

# Code Walkthrough

Key components of the RAG implementation.

## Ingestion (`src/services/ingest.py`)

This service handles reading markdown files and chunking them. We use `RecursiveCharacterTextSplitter` to ensure chunks are of appropriate size for the context window.

```python
def chunk_markdown(content: str) -> List[Dict]:
    # ... logic to split by headers and then by characters ...
    return chunks
```

## Vector Store (`src/services/vector_store.py`)

We use Qdrant as our vector database. The client is initialized as a singleton.

```python
class VectorStore:
    @classmethod
    def get_client(cls) -> QdrantClient:
        # ... init client ...
        return cls._client
```

## Retrieval (`src/services/retrieval.py`)

We perform a semantic search using cosine similarity.

```python
async def retrieve_context(query: str, top_k: int = 5):
    embedding = await get_embedding(query)
    search_result = client.search(
        collection_name="book_content",
        query_vector=embedding,
        limit=top_k
    )
    return search_result
```

## Chat Orchestration (`src/services/chat.py`)

The chat service combines retrieval and generation. It constructs a prompt with the retrieved context and streams the response from Google Gemini.

```python
async def process_chat_request(request: ChatRequest):
    sources = await retrieve_context(request.query)
    # ... construct system prompt with sources ...
    async for chunk in generate_stream(user_prompt):
        yield chunk
```
