def build_plan(task):
    return [
        {"step": 1, "task": "analyze", "target": "analyzer_worker"},
        {"step": 2, "task": "fix", "target": "fixer_worker"},
        {"step": 3, "task": "clean", "target": "cleaner_worker"}
    ]
