from openai import AsyncOpenAI
import google.generativeai as genai
from src.core.config import settings
from typing import List

# Initialize clients
openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
genai.configure(api_key=settings.GEMINI_API_KEY)

async def get_embedding(text: str) -> List[float]:
    """Generate embedding for a single string using Google Gemini."""
    # Text embedding-004 output dimension is 768
    result = genai.embed_content(
        model="models/text-embedding-004",
        content=text,
        task_type="retrieval_query"
    )
    return result['embedding']

async def get_cohere_embedding(text: str) -> List[float]:
    """Generate embedding using Cohere (matches ingested data)."""
    import cohere
    import os
    co = cohere.ClientV2(api_key=os.getenv("COHERE_API_KEY"))
    response = co.embed(
        texts=[text],
        model="embed-english-v3.0",
        input_type="search_query",
        embedding_types=["float"]
    )
    return response.embeddings.float_[0]

async def generate_response(prompt: str, system_instruction: str = None) -> str:
    """Generate response using Google Gemini."""
    model = genai.GenerativeModel("gemini-2.5-flash")
    
    full_prompt = prompt
    if system_instruction:
        full_prompt = f"System: {system_instruction}\n\nUser: {prompt}"

    response = model.generate_content(full_prompt)
    return response.text

async def generate_stream(prompt: str, system_instruction: str = None):
    """Generate streaming response using Google Gemini."""
    model = genai.GenerativeModel("gemini-2.5-flash")
    
    full_prompt = prompt
    if system_instruction:
        full_prompt = f"System: {system_instruction}\n\nUser: {prompt}"

    response = model.generate_content(full_prompt, stream=True)
    for chunk in response:
        yield chunk.text