import asyncio
import json
import importlib
import sys
import os

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from llama_cpp import Llama
    LLAMA_CPP_AVAILABLE = True
except ImportError:
    LLAMA_CPP_AVAILABLE = False
    print("⚠️  llama-cpp-python not found. Install with: pip install llama-cpp-python")

# Model paths
MODEL_PATHS = {
    # Administrative models
    "llama-2-70b-chat": "LLM_Mesh/models/administrative/llama-2-70b-chat.ggmlv3.q2_K.bin",
    "deepseek-llm-67b-chat": "LLM_Mesh/models/administrative/deepseek-llm-67b-chat.Q2_K.gguf",
    "qwen1.5-72b-chat": "LLM_Mesh/models/administrative/qwen1.5-72b-chat-q2_k.gguf",
    # Worker models  
    "starcoder2-15b": "LLM_Mesh/models/worker/starcoder2-15b-Q4_K_M.gguf",
    "deepseek-coder-6.7b-instruct": "LLM_Mesh/models/worker/deepseek-coder-6.7b-instruct.Q4_K_S.gguf",
    "codellama-7b-instruct": "LLM_Mesh/models/worker/codellama-7b-instruct.Q4_K_M.gguf",
    "wizardcoder-python-13b": "LLM_Mesh/models/worker/wizardcoder-python-13b-v1.0.Q4_K_S.gguf",
    "wizardcoder-python-34b": "LLM_Mesh/models/worker/wizardcoder-python-34b-v1.0.Q3_K_S.gguf",
    "mistral-7b-instruct-v0.2": "LLM_Mesh/models/worker/mistral-7b-instruct-v0.2.Q4_K_M.gguf"
}

# Model cache to avoid reloading
model_cache = {}

# Mapping task types to worker models and their functions
TASK_MAP = {
    "debug": ("starcoder2-15b", "run_debugger_analysis"),
    "analyze": ("deepseek-coder-6.7b-instruct", "run_analyzer_deep"), 
    "fix": ("codellama-7b-instruct", "run_fixer_pytorch"),
    "fix_helper": ("wizardcoder-python-13b", "run_fixer_helper"),
    "clean": ("mistral-7b-instruct-v0.2", "run_cleaner_optimization"),
    "refactor": ("wizardcoder-python-34b", "run_advanced_refactor")
}

# Load model with caching
def load_model(model_name: str):
    """Load a GGUF/GGML model with caching."""
    if not LLAMA_CPP_AVAILABLE:
        print(f"⚠️  llama-cpp-python not available, using fallback for {model_name}")
        return None
        
    if model_name in model_cache:
        return model_cache[model_name]
    
    if model_name not in MODEL_PATHS:
        print(f"❌ Model {model_name} not found in MODEL_PATHS")
        return None
    
    model_path = MODEL_PATHS[model_name]
    if not os.path.exists(model_path):
        print(f"❌ Model file not found: {model_path}")
        return None
    
    try:
        print(f"📥 Loading {model_name}...")
        model = Llama(
            model_path=model_path,
            n_ctx=4096,  # Context window
            n_threads=4,  # CPU threads
            verbose=False
        )
        model_cache[model_name] = model
        print(f"✅ {model_name} loaded successfully")
        return model
    except Exception as e:
        print(f"❌ Failed to load {model_name}: {str(e)}")
        return None

# Async wrapper for model inference
async def run_model_inference(model_name: str, prompt: str, max_tokens: int = 512) -> str:
    """Run inference on a GGUF model asynchronously."""
    if not LLAMA_CPP_AVAILABLE:
        return f"[FALLBACK {model_name}]: {_generate_fallback_response(prompt, model_name)}"
    
    model = load_model(model_name)
    if not model:
        return f"[FALLBACK {model_name}]: {_generate_fallback_response(prompt, model_name)}"
    
    try:
        # Run inference in a thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None, 
            lambda: model(prompt, max_tokens=max_tokens, stop=["</s>", "\n\n"])
        )
        return response['choices'][0]['text'].strip()
    except Exception as e:
        return f"[FALLBACK {model_name}]: Error during inference - {_generate_fallback_response(prompt, model_name)}"

def _generate_fallback_response(prompt: str, model_name: str) -> str:
    """Generate a fallback response when models are not available."""
    if "debug" in model_name or "debug" in prompt.lower():
        return "Debugging analysis: Check variable types, function signatures, and error messages. Consider using print statements or debugger."
    elif "fix" in model_name or "fix" in prompt.lower():
        return "Code fix suggestion: Review the error message, check syntax, and ensure proper imports and dependencies."
    elif "analyze" in model_name or "analyze" in prompt.lower():
        return "Code analysis: Consider code structure, performance implications, and maintainability improvements."
    elif "clean" in model_name or "clean" in prompt.lower():
        return "Code cleanup: Remove unused imports, variables, and functions. Optimize for readability and performance."
    else:
        return f"AI assistant response using {model_name} would analyze and provide suggestions for the given code."

# Main router
async def handle_task(task_type: str, payload: dict) -> str:
    """Route task to appropriate model for processing."""
    if task_type not in TASK_MAP:
        return f"[ERROR]: Unknown task_type '{task_type}'"

    model_name, func_name = TASK_MAP[task_type]
    
    # Build prompt based on task type and function signature
    function_sig = payload.get('function_sig', '')
    context = payload.get('context', '')
    code_str = payload.get('code_str', '')
    error_msg = payload.get('error_msg', '')
    
    # Create task-specific prompts
    if task_type == "debug":
        prompt = f"""You are a debugging assistant. {function_sig}

Code to debug:
{code_str}

Error message:
{error_msg}

Context:
{context}

Please provide a clear analysis and fix:"""
    
    elif task_type == "analyze":
        prompt = f"""You are a code analysis expert. {function_sig}

Code to analyze:
{code_str}

Context:
{context}

Please provide detailed analysis and insights:"""
    
    elif task_type == "fix":
        prompt = f"""You are a code fixing specialist. {function_sig}

Code to fix:
{code_str}

Context:
{context}

Error to fix:
{error_msg}

Please provide the corrected code:"""
    
    elif task_type == "clean":
        prompt = f"""You are a code cleanup expert. {function_sig}

Code to clean:
{code_str}

Please remove dead code and optimize:"""
        
    else:
        prompt = f"{function_sig}\n\nTask: {task_type}\nCode: {code_str}\nContext: {context}"
    
    # Run inference on the selected model
    result = await run_model_inference(model_name, prompt)
    return result


