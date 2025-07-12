import json
import os
from datetime import datetime

LOG_PATH = "AdministrativeMesh/task_log.json"

def log_task_event(task_id, phase, admin=None, status=None):
    entry = {
        "task_id": task_id,
        "phase": phase,
        "timestamp": datetime.utcnow().isoformat(),
        "admin": admin,
        "status": status
    }

    if not os.path.exists(LOG_PATH):
        with open(LOG_PATH, "w") as f:
            json.dump([entry], f, indent=2)
    else:
        with open(LOG_PATH, "r+") as f:
            logs = json.load(f)
            logs.append(entry)
            f.seek(0)
            json.dump(logs, f, indent=2)

# Example usage:
# log_task_event("123456", phase="dispatch", admin="llama3_70b")
# log_task_event("123456", phase="execution", status="success")
