from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import asyncio
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from AdministrativeMesh.admin_dispatcher import dispatch

app = FastAPI(title="Neural Coding Assistant API", version="1.0.0")

class ChatPayload(BaseModel):
    messages: list
    model: str
    temperature: float = 0.7
    stream: bool = False

@app.post("/v1/chat/completions")
async def route_chat(payload: ChatPayload):
    """OpenAI-compatible chat completions endpoint."""
    try:
        prompt = payload.messages[-1]["content"]
        result = await dispatch(prompt)
        
        if payload.stream:
            return StreamingResponse(
                event_stream(result), 
                media_type="text/event-stream"
            )
        
        return {
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": result
                },
                "index": 0,
                "finish_reason": "stop"
            }],
            "model": payload.model,
            "usage": {
                "prompt_tokens": len(prompt.split()),
                "completion_tokens": len(result.split()),
                "total_tokens": len(prompt.split()) + len(result.split())
            },
            "id": f"chatcmpl-{hash(prompt)}",
            "object": "chat.completion",
            "created": int(asyncio.get_event_loop().time())
        }
    except Exception as e:
        return {
            "error": {
                "message": f"Internal server error: {str(e)}",
                "type": "internal_error",
                "code": 500
            }
        }

async def event_stream(result: str):
    """Stream response for real-time updates."""
    words = result.split()
    for i, word in enumerate(words):
        chunk = {
            "choices": [{
                "delta": {"content": word + " "},
                "index": 0,
                "finish_reason": None
            }],
            "id": f"chatcmpl-stream-{i}",
            "object": "chat.completion.chunk"
        }
        yield f"data: {chunk}\n\n"
        await asyncio.sleep(0.01)
    
    # Send final chunk
    final_chunk = {
        "choices": [{
            "delta": {},
            "index": 0,
            "finish_reason": "stop"
        }],
        "id": "chatcmpl-stream-final",
        "object": "chat.completion.chunk"
    }
    yield f"data: {final_chunk}\n\n"
    yield "data: [DONE]\n\n"

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Neural Coding Assistant"}

@app.get("/")
async def root():
    """Root endpoint with service info."""
    return {
        "service": "Neural Coding Assistant",
        "version": "1.0.0",
        "endpoints": ["/v1/chat/completions", "/health"],
        "description": "AI-powered coding assistant with administrative mesh architecture"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
