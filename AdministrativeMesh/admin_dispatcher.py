import asyncio
import os
import sys

# Add project paths for imports
project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.append(project_root)

from .council_router import select_admin
from .attention_router import get_context_slice
from .task_parser import parse_task
from .memory_expander import expand_memory
from .task_lifecycle import log_task_event
from .function_courier_parser import get_function_signature

# Import from LLM_Mesh
from LLM_Mesh.mesh_manager import MeshManager

# Global mesh manager instance
_mesh_manager = None

async def get_mesh_manager():
    """Get or create mesh manager instance."""
    global _mesh_manager
    if _mesh_manager is None:
        _mesh_manager = MeshManager()
        await _mesh_manager.initialize_models()
    return _mesh_manager

async def dispatch(prompt: str):
    """Main dispatch function for handling user requests."""
    try:
        # Step 1: Classify task
        task = parse_task(prompt)

        # Step 2: Select admin model (or could be fixed)
        admin = select_admin(task)

        # Step 3: Load context memory and compress to fit
        raw_context = get_context_slice(task)
        compressed_context = expand_memory(raw_context, task['window_tier'])

        # Step 4: Log dispatch phase
        log_task_event(task['id'], phase="dispatch", admin=admin)

        # Step 4.5: Load function signature
        function_sig = get_function_signature(task["type"])

        # Step 5: Package payload
        payload = {
            "code_str": task.get("code", ""),
            "error_msg": task.get("error", ""),
            "context": compressed_context,
            "summary": task.get("summary", ""),
            "function_sig": function_sig
        }

        # Step 6: Call mesh manager
        mesh_manager = await get_mesh_manager()
        result = await mesh_manager.handle_task(task["type"], payload)

        # Step 7: Log execution phase
        log_task_event(task["id"], phase="executed", status="complete")

        return result
        
    except Exception as e:
        # Step 7b: Log error and return fallback
        if 'task' in locals():
            log_task_event(task.get("id", "unknown"), phase="error", status=str(e))
        return f"[ERROR]: Dispatch failed: {str(e)}"

# Standalone for CLI test
if __name__ == "__main__":
    prompt = "Fix this TypeError in utils.py"
    asyncio.run(dispatch(prompt))
