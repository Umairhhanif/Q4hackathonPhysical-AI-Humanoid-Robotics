from src.services.retrieval import retrieve_context
from src.services.llm import generate_stream
from src.models.api import ChatRequest
from typing import AsyncGenerator

async def process_chat_request(request: ChatRequest) -> AsyncGenerator[str, None]:
    # 1. Retrieve context
    sources = await retrieve_context(request.query, request.selected_text)
    
    # 2. Construct Prompt
    context_str = "\n\n".join([f"Source: {s.source_file}\nContent: {s.snippet}" for s in sources])
    
    system_prompt = """You are an expert assistant for the 'Physical AI & Humanoid Robotics' book.
Answer the user's question based ONLY on the provided context.
If the answer is not in the context, say you don't know.
Cite the source file if possible.
"""

    if request.selected_text:
        system_prompt += f"\n\nThe user has selected the following text for specific context:\n\"{request.selected_text}\"\nFocus your answer on this text if relevant."

    user_prompt = f"""Context:
{context_str}

Question: {request.query}
"""

    # 3. Generate (Stream)
    # We yield the sources first as a special JSON line or header if we want to send them early?
    # Or just stream the text. The API model `ChatResponse` in tasks.md implies a non-streaming response structure 
    # but the contract said "text/event-stream".
    # We will stream the text. We can send sources as a final chunk or header?
    # For simplicity in this function, we just yield the text chunks. 
    # The caller can handle sending sources separate or we format them into the stream.
    # Let's verify requirements. "Returns streaming response".
    
    # We will just yield the text.
    
    async for chunk in generate_stream(user_prompt, system_instruction=system_prompt):
        yield chunk
