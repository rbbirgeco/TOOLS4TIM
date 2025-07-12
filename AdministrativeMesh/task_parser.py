import os
import sys

# Add project root to path
project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.append(project_root)

from config import classify_task_by_keywords, FUNCTION_SIGNATURES

def parse_task(prompt: str) -> dict:
    """Parse user prompt to determine task type and extract relevant information."""
    # Use centralized classification
    task_type = classify_task_by_keywords(prompt)
    function_name = FUNCTION_SIGNATURES.get(task_type, "process_code").split("(")[0].replace("def ", "")
    
    return {
        "id": hash(prompt),
        "type": task_type,
        "function": function_name,
        "keywords": prompt.lower().split(),
        "length": len(prompt),
        "text": prompt,
        "window_tier": 2,
        "code": "",
        "error": "",
        "summary": ""
    }
