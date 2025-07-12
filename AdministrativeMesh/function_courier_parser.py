import re

COURIER_PATH = "NeuralCodingAssistant/Function_Courier.md"

def get_function_signature(task_type: str) -> str:
    with open(COURIER_PATH, "r") as f:
        text = f.read()

    # Find the section matching the task
    pattern = rf"## {task_type}\n```python\n(.*?)```"
    match = re.search(pattern, text, re.DOTALL)

    if not match:
        raise ValueError(f"[ERROR]: No function definition found for task '{task_type}'")

    return match.group(1).strip()
