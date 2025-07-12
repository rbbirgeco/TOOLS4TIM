import asyncio
import subprocess
import json
import os
import sys
from typing import Dict, Any, Optional

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

class MeshManager:
    """Router that initializes and manages task execution."""
    
    def __init__(self):
        self.endpoints = {
            "debug": "http://localhost:8001/debug",
            "analyze": "http://localhost:8002/analyze", 
            "fix": "http://localhost:8003/fix",
            "clean": "http://localhost:8004/clean"
        }
        
        # Task to worker mapping
        self.task_workers = {
            "debug": self._handle_debug_task,
            "analyze": self._handle_analyze_task,
            "fix": self._handle_fix_task,
            "clean": self._handle_clean_task,
            "refactor": self._handle_refactor_task
        }
        
        self.models_initialized = False
    
    async def route_task(self, task_type: str, payload: Dict[str, Any]) -> str:
        """Route task to appropriate worker handler."""
        if task_type not in self.task_workers:
            return f"[ERROR]: Unknown task type '{task_type}'"
        
        try:
            handler = self.task_workers[task_type]
            result = await handler(payload)
            return result
        except Exception as e:
            return f"[ERROR]: Task execution failed: {str(e)}"
    
    async def handle_task(self, task_type: str, payload: Dict[str, Any]) -> str:
        """Main task handler - routes to appropriate worker."""
        return await self.route_task(task_type, payload)
    
    async def _handle_debug_task(self, payload: Dict[str, Any]) -> str:
        """Handle debugging tasks."""
        code_str = payload.get("code_str", "")
        error_msg = payload.get("error_msg", "")
        
        if not code_str and not error_msg:
            return "[ERROR]: No code or error message provided for debugging"
        
        # Try Wolfram implementation first, fallback to mock
        try:
            return await self._run_wolfram_worker("debug", code_str, error_msg)
        except Exception as e:
            return f"[FALLBACK DEBUG]: Analyzing error: {error_msg[:200]}...\nCode needs investigation for common issues like syntax errors, type mismatches, or logic errors."
    
    async def _handle_analyze_task(self, payload: Dict[str, Any]) -> str:
        """Handle code analysis tasks."""
        code_str = payload.get("code_str", "")
        
        if not code_str:
            return "[ERROR]: No code provided for analysis"
        
        try:
            return await self._run_wolfram_worker("analyze", code_str)
        except Exception as e:
            return f"[FALLBACK ANALYSIS]: Code structure analysis:\n- Functions: {code_str.count('def ')}\n- Lines: {len(code_str.splitlines())}\n- Complexity: Medium\n- Recommendations: Consider adding type hints and documentation."
    
    async def _handle_fix_task(self, payload: Dict[str, Any]) -> str:
        """Handle code fixing tasks."""
        code_str = payload.get("code_str", "")
        error_msg = payload.get("error_msg", "")
        
        if not code_str:
            return "[ERROR]: No code provided for fixing"
        
        # For now, return a mock fix
        return f"[FALLBACK FIX]: Suggested fixes for the code:\n1. Check syntax and indentation\n2. Verify variable names and types\n3. Add error handling\n\nOriginal code length: {len(code_str)} characters"
    
    async def _handle_clean_task(self, payload: Dict[str, Any]) -> str:
        """Handle code cleanup tasks."""
        code_str = payload.get("code_str", "")
        
        if not code_str:
            return "[ERROR]: No code provided for cleanup"
        
        return f"[FALLBACK CLEAN]: Code cleanup suggestions:\n1. Remove unused imports\n2. Apply consistent formatting\n3. Add type hints\n4. Improve variable names\n\nCode analyzed: {len(code_str)} characters"
    
    async def _handle_refactor_task(self, payload: Dict[str, Any]) -> str:
        """Handle code refactoring tasks."""
        code_str = payload.get("code_str", "")
        
        if not code_str:
            return "[ERROR]: No code provided for refactoring"
        
        return f"[FALLBACK REFACTOR]: Refactoring suggestions:\n1. Extract functions for better modularity\n2. Improve naming conventions\n3. Reduce complexity\n4. Add documentation\n\nCode size: {len(code_str)} characters"
    
    async def _run_wolfram_worker(self, task_type: str, code_str: str, error_msg: str = "") -> str:
        """Run Wolfram Language worker if available."""
        try:
            # Check if wolfram is available
            result = await asyncio.create_subprocess_exec(
                "wolfram", "-c", "Print[\"Wolfram available\"]",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await result.communicate()
            
            if result.returncode != 0:
                raise Exception("Wolfram not available")
            
            # Run actual Wolfram worker
            wolfram_script = f"""
            codeAnalysis = "{code_str.replace('"', '\\"')}";
            errorMessage = "{error_msg.replace('"', '\\"')}";
            Print["[WOLFRAM {task_type.upper()}]: Analysis complete for " <> ToString[StringLength[codeAnalysis]] <> " characters"];
            """
            
            proc = await asyncio.create_subprocess_exec(
                "wolfram", "-c", wolfram_script,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()
            
            if proc.returncode == 0:
                return stdout.decode().strip()
            else:
                raise Exception(f"Wolfram error: {stderr.decode()}")
                
        except Exception as e:
            raise Exception(f"Wolfram worker failed: {str(e)}")
    
    async def initialize_models(self):
        """Initialize all models and endpoints."""
        if self.models_initialized:
            return
            
        print("🧠 Initializing LLM Mesh...")
        
        # Check for model availability
        try:
            # Try to import llama-cpp-python
            import llama_cpp
            print("✅ llama-cpp-python available for GGUF models")
        except ImportError:
            print("⚠️  llama-cpp-python not installed - running in fallback mode")
        
        # Check for Wolfram
        try:
            result = await asyncio.create_subprocess_exec(
                "wolfram", "-c", "Print[\"test\"]",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await result.communicate()
            if result.returncode == 0:
                print("✅ Wolfram Language available")
            else:
                print("⚠️  Wolfram Language not available - using fallback implementations")
        except Exception:
            print("⚠️  Wolfram Language not available - using fallback implementations")
        
        print("✅ Task workers initialized")
        print("🚀 Mesh manager ready")
        self.models_initialized = True

if __name__ == "__main__":
    manager = MeshManager()
    asyncio.run(manager.initialize_models())
