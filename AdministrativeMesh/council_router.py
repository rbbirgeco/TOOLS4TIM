def select_admin(task):
    """Select the best administrative model based on task characteristics."""
    if task["length"] > 16000:
        return "llama-2-70b-chat"  # Large context tasks
    if task["type"] in ["math", "chain_of_thought", "analyze"]:
        return "deepseek-llm-67b-chat"  # Deep reasoning tasks
    if "tool" in task["keywords"] or "steps" in task["text"] or task["type"] == "debug":
        return "qwen1.5-72b-chat"  # Tool usage and debugging
    return "deepseek-llm-67b-chat"  # Default to deepseek for general tasks
