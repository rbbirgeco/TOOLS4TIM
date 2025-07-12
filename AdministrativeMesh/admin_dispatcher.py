import asyncio
from council_router import select_admin
from attention_router import get_context_slice
from task_parser import parse_task
from memory_expander import expand_memory
from task_lifecycle import log_task_event
from function_courier_parser import get_function_signature
from mesh_manager import handle_task

async def dispatch(prompt: str):
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

    # Step 6: Call mesh (which selects PyTorch or Wolfram)
    result = await handle_task(task["type"], payload)

    # Step 7: Log execution phase
    log_task_event(task["id"], phase="executed", status="complete")

    return result

# Standalone for CLI test
if __name__ == "__main__":
    prompt = "Fix this TypeError in utils.py"
    asyncio.run(dispatch(prompt))
