"""
Neural Coding Assistant - AI-powered coding assistance with mesh architecture
"""

__version__ = "0.1.0"
__author__ = "Neural Coding Team"

from .AdministrativeMesh.admin_dispatcher import dispatch
from .LLM_Mesh.mesh_manager import MeshManager

__all__ = ["dispatch", "MeshManager"]
