from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import sys
import os
import logging

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from AdministrativeMesh.admin_dispatcher import dispatch
from error_handling import handle_errors, with_timeout_and_retry, RetryConfig

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Neural Coding Assistant API", 
    version="1.0.0",
    description="AI-powered coding assistance with mesh architecture"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatPayload(BaseModel):
    messages: list
    model: str
    temperature: float = 0.7
    stream: bool = False

@app.post("/v1/chat/completions")
@handle_errors("[ERROR]: Chat completion failed")
async def route_chat(payload: ChatPayload):
    """OpenAI-compatible chat completions endpoint with enhanced error handling."""
    try:
        if not payload.messages or len(payload.messages) == 0:
            raise HTTPException(status_code=400, detail="No messages provided")
        
        prompt = payload.messages[-1]["content"]
        if not prompt or not prompt.strip():
            raise HTTPException(status_code=400, detail="Empty prompt provided")
        
        # Use retry logic for dispatch
        retry_config = RetryConfig(max_retries=2, timeout=30.0)
        result = await with_timeout_and_retry(
            dispatch,
            prompt,
            retry_config=retry_config
        )
        
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
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chat completion error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

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
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": int(asyncio.get_event_loop().time())
    }

@app.get("/models")
async def list_models():
    """List available models."""
    return {
        "object": "list",
        "data": [
            {"id": "neural-coding-assistant", "object": "model", "owned_by": "neural-coding"},
            {"id": "debug-specialist", "object": "model", "owned_by": "neural-coding"},
            {"id": "analyzer", "object": "model", "owned_by": "neural-coding"},
            {"id": "code-fixer", "object": "model", "owned_by": "neural-coding"},
            {"id": "code-cleaner", "object": "model", "owned_by": "neural-coding"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
