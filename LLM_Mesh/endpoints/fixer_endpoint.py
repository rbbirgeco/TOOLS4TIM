from fastapi import FastAPI
from pydantic import BaseModel
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from AdministrativeMesh.mesh_manager import handle_task

app = FastAPI()

class FixRequest(BaseModel):
    code: str
    context: str
    fix_instruction: str = ""

@app.post("/fix")
async def fix_endpoint(request: FixRequest):
    """Fix code endpoint using the fixer worker model."""
    payload = {
        "code_str": request.code,
        "context": request.context,
        "error_msg": request.fix_instruction,
        "function_sig": "def fix_code_snippet(code_str: str, context: str) -> str:"
    }
    
    try:
        result = await handle_task("fix", payload)
        return {
            "status": "success",
            "fixed_code": result,
            "model_used": "codellama-7b-instruct",
            "worker": "fixer_worker"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "fallback_response": f"# Error fixing code: {str(e)}\n{request.code}"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
