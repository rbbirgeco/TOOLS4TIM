from fastapi import FastAPI
from pydantic import BaseModel
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from AdministrativeMesh.mesh_manager import handle_task

app = FastAPI()

class DebugRequest(BaseModel):
    code: str
    error_message: str
    context: str = ""

@app.post("/debug")
async def debug_endpoint(request: DebugRequest):
    """Debug code endpoint using the debugger worker model."""
    payload = {
        "code_str": request.code,
        "error_msg": request.error_message,
        "context": request.context,
        "function_sig": "def debug_code_snippet(code_str: str, error_msg: str) -> str:"
    }
    
    try:
        result = await handle_task("debug", payload)
        return {
            "status": "success",
            "analysis": result,
            "model_used": "starcoder2-15b",
            "worker": "debugger_worker"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "fallback_response": f"Debug analysis failed: {str(e)}"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
