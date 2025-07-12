from fastapi import FastAPI
from pydantic import BaseModel
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from AdministrativeMesh.mesh_manager import handle_task

app = FastAPI()

class AnalyzeRequest(BaseModel):
    code_summary: str
    component_path: str
    context: str = ""

@app.post("/analyze")
async def analyze_endpoint(request: AnalyzeRequest):
    """Analyze code endpoint using the analyzer worker model."""
    payload = {
        "code_str": request.code_summary,
        "context": f"Component: {request.component_path}\n{request.context}",
        "function_sig": "def analyze_code_snippet(code_summary: str, component_path: str) -> str:"
    }
    
    try:
        result = await handle_task("analyze", payload)
        return {
            "status": "success",
            "analysis": result,
            "component": request.component_path,
            "model_used": "deepseek-coder-6.7b-instruct",
            "worker": "analyzer_worker"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "fallback_response": f"Analysis failed for {request.component_path}: {str(e)}"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
