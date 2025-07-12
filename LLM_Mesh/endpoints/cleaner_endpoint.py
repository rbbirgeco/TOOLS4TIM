from fastapi import FastAPI
from pydantic import BaseModel
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from AdministrativeMesh.mesh_manager import handle_task

app = FastAPI()

class CleanRequest(BaseModel):
    codebase: str
    cleanup_rules: list = []

@app.post("/clean")
async def clean_endpoint(request: CleanRequest):
    """Clean code endpoint using the cleaner worker model."""
    payload = {
        "code_str": request.codebase,
        "context": f"Cleanup rules: {', '.join(request.cleanup_rules)}",
        "function_sig": "def clean_codebase(codebase: str) -> str:"
    }
    
    try:
        result = await handle_task("clean", payload)
        return {
            "status": "success",
            "cleaned_code": result,
            "model_used": "mistral-7b-instruct-v0.2",
            "worker": "cleaner_worker"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "fallback_response": f"Code cleanup failed: {str(e)}"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
