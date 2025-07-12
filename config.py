"""
Configuration for function signatures and task mappings.
Single source of truth for worker function definitions.
"""

# Function signatures for each task type
FUNCTION_SIGNATURES = {
    "debug": "def debug_code_snippet(code_str: str, error_msg: str) -> str:",
    "analyze": "def analyze_code_snippet(code_str: str) -> str:",
    "fix": "def fix_code_snippet(code_str: str, error_msg: str = '') -> str:",
    "clean": "def clean_code_snippet(code_str: str) -> str:",
    "refactor": "def refactor_code_snippet(code_str: str) -> str:"
}

# Task classification keywords
TASK_KEYWORDS = {
    "debug": ["error", "bug", "debug", "fix error", "broken", "exception", "traceback", "crash"],
    "analyze": ["analyze", "analysis", "review", "examine", "inspect", "understand", "explain", "check"],
    "fix": ["fix", "repair", "correct", "solve", "resolve", "patch", "mend"],
    "clean": ["clean", "cleanup", "optimize", "improve", "beautify", "format", "tidy"],
    "refactor": ["refactor", "restructure", "reorganize", "rewrite", "modernize", "redesign"]
}

# Worker endpoint mappings
WORKER_ENDPOINTS = {
    "debug": "http://localhost:8001/debug",
    "analyze": "http://localhost:8002/analyze", 
    "fix": "http://localhost:8003/fix",
    "clean": "http://localhost:8004/clean",
    "refactor": "http://localhost:8005/refactor"
}

def get_function_signature_from_config(task_type: str) -> str:
    """Get function signature from configuration."""
    return FUNCTION_SIGNATURES.get(task_type, "def process_code(code_str: str) -> str:")

def classify_task_by_keywords(prompt: str) -> str:
    """Classify task type based on keywords in prompt."""
    prompt_lower = prompt.lower()
    
    # Priority order - more specific first
    for task_type, keywords in TASK_KEYWORDS.items():
        if any(keyword in prompt_lower for keyword in keywords):
            return task_type
    
    return "refactor"  # default
