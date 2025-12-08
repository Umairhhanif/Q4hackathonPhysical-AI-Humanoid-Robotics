from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from src.models.api import ChatRequest
from src.services.retrieval import retrieve_context
from src.services.logging import log_interaction
import json
import time

router = APIRouter()

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    start_time = time.time()
    
    try:
        sources = await retrieve_context(request.query, request.selected_text)
        
        async def event_generator():
            full_response = ""
            try:
                # Send sources first
                sources_data = [s.model_dump() for s in sources]
                yield f"data: {json.dumps({'type': 'sources', 'data': sources_data})}\n\n"
                
                # Generate response
                from src.services.chat import generate_stream 
                
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
                async for chunk in generate_stream(user_prompt, system_instruction=system_prompt):
                    full_response += chunk
                    yield f"data: {json.dumps({'type': 'token', 'data': chunk})}\n\n"
                
                yield "data: [DONE]\n\n"
                
                # Log success
                latency = int((time.time() - start_time) * 1000)
                await log_interaction(
                    user_query=request.query,
                    bot_response=full_response,
                    selected_text=request.selected_text,
                    latency_ms=latency,
                    successful=True
                )

            except Exception as e:
                # Log failure
                latency = int((time.time() - start_time) * 1000)
                await log_interaction(
                    user_query=request.query,
                    bot_response=full_response, # partial
                    selected_text=request.selected_text,
                    latency_ms=latency,
                    successful=False
                )
                yield f"data: {json.dumps({'type': 'error', 'data': str(e)})}\n\n"

        return StreamingResponse(event_generator(), media_type="text/event-stream")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))