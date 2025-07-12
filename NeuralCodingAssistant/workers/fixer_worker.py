import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from AdministrativeMesh.mesh_manager import run_model_inference

async def run_fixer(code_str: str, context: str, **kwargs) -> str:
    """Fix code using CodeLlama model."""
    error_msg = kwargs.get('error_msg', 'Fix any issues in this code')
    
    prompt = f"""You are a code fixing expert. Fix the following code:

Code to fix:
```
{code_str}
```

Error/Issue: {error_msg}
Context: {context}

Please provide only the corrected code without explanations:
"""
    
    try:
        result = await run_model_inference("codellama-7b-instruct", prompt, max_tokens=512)
        return result
    except Exception as e:
        return f"[FIX ERROR]: Model execution failed: {str(e)}"
