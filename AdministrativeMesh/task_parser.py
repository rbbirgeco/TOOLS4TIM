def parse_task(prompt: str) -> dict:
    return {
        "id": hash(prompt),
        "type": "debug" if "error" in prompt.lower() else "refactor",
        "function": "debug_code_snippet",
        "keywords": prompt.lower().split(),
        "length": len(prompt),
        "text": prompt,
        "window_tier": 2,
        "code": "",
        "error": "",
        "summary": ""
    }
