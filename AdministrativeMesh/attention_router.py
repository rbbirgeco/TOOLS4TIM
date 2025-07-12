import json

def get_context_slice(task):
    with open("NeuralCodingAssistant/AgentMemory/ContextMap.json") as f:
        context_map = json.load(f)
    return context_map.get(task["type"], "")
