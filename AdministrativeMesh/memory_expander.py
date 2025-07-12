def expand_memory(context: str, window_tier: int):
    if window_tier == 1:
        return str(context)[:512]
    if window_tier == 2:
        return str(context)[:2048]
    return str(context)  # full
