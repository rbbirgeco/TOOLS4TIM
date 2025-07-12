import re
import os
import sys

# Add project root to path
project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.append(project_root)

from config import get_function_signature_from_config

# Use relative path from project root
COURIER_PATH = os.path.join(project_root, "NeuralCodingAssistant", "Function_Courier.md")

def get_function_signature(task_type: str) -> str:
    """Get function signature for a specific task type."""
    # First try configuration (single source of truth)
    config_signature = get_function_signature_from_config(task_type)
    if config_signature != "def process_code(code_str: str) -> str:":
        return config_signature
    
    # Fallback to Function_Courier.md if available
    try:
        with open(COURIER_PATH, "r") as f:
            text = f.read()
            
        # Find the section matching the task
        pattern = rf"## {task_type}\n```python\n(.*?)```"
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)

        if match:
            return match.group(1).strip()
            
    except FileNotFoundError:
        pass
    
    # Final fallback to config
    return config_signature
