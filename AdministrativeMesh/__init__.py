# Administrative Mesh Package
"""
Administrative Mesh - Task routing and orchestration
"""

__version__ = "1.0.0"

from .admin_dispatcher import dispatch
from .task_parser import parse_task
from .council_router import select_admin

__all__ = ["dispatch", "parse_task", "select_admin"]
