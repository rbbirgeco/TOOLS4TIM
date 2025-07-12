import asyncio
import subprocess
import json
import os
import sys
from typing import Dict, Any, Optional

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from .distributed_models import model_registry, get_model_response, initialize_distributed_models

class MeshManager:
    """Router that manages task execution using distributed models hosted on network nodes."""
    
    def __init__(self):
        # Task to model mapping for distributed routing
        self.task_model_mapping = {
            "debug": "code-llama-7b",  # Python-specialized with large context
            "analyze": "starcoder-15b",  # Advanced code analysis
            "fix": "code-llama-7b",  # Debugging specialist
            "clean": "mistral-7b",  # General reasoning for code cleanup
            "refactor": "deepseek-coder-33b",  # Large model for complex refactoring
            "optimize": "starcoder-15b",  # Code optimization
            "document": "code-llama-7b"  # Documentation generation
        }
        
        # Task to worker mapping
        self.task_workers = {
            "debug": self._handle_debug_task,
            "analyze": self._handle_analyze_task,
            "fix": self._handle_fix_task,
            "clean": self._handle_clean_task,
            "refactor": self._handle_refactor_task,
            "optimize": self._handle_optimize_task,
            "document": self._handle_document_task
        }
        
        self.models_initialized = False
    
    async def initialize_models(self):
        """Initialize the distributed model system."""
        if not self.models_initialized:
            print("🌐 Initializing distributed AI models...")
            await initialize_distributed_models()
            self.models_initialized = True
            print("✅ Distributed model system ready")
    
    async def route_task(self, task_type: str, payload: Dict[str, Any]) -> str:
        """Route task to appropriate distributed model handler."""
        # Ensure models are initialized
        await self.initialize_models()
        
        if task_type not in self.task_workers:
            return f"[ERROR]: Unknown task type '{task_type}'"
        
        try:
            handler = self.task_workers[task_type]
            result = await handler(payload)
            return result
        except Exception as e:
            return f"[ERROR]: Task execution failed: {str(e)}"
    
    async def handle_task(self, task_type: str, payload: Dict[str, Any]) -> str:
        """Main task handler - routes to appropriate distributed model worker."""
        return await self.route_task(task_type, payload)
    
    async def _get_model_response(self, task_type: str, prompt: str, max_tokens: int = 1000) -> str:
        """Get response from the appropriate distributed model for the task type."""
        model_name = self.task_model_mapping.get(task_type, "mistral-7b")
        
        result = await get_model_response(
            model_name=model_name,
            prompt=prompt,
            task_type=task_type,
            max_tokens=max_tokens,
            temperature=0.3  # Lower temperature for coding tasks
        )
        
        if result.get("success"):
            return result["response"]
        else:
            return f"[ERROR]: {result.get('error', 'Unknown error occurred')}"
    
    async def _handle_debug_task(self, payload: Dict[str, Any]) -> str:
        """Handle debugging tasks using distributed Code Llama model."""
        code = payload.get("code", "")
        error_msg = payload.get("error", "")
        
        prompt = f"""You are a debugging expert. Analyze this code and error:

CODE:
{code}

ERROR:
{error_msg}

Provide:
1. Root cause analysis
2. Specific fix suggestions
3. Prevention strategies

Response:"""
        
        return await self._get_model_response("debug", prompt, max_tokens=1500)
    
    async def _handle_analyze_task(self, payload: Dict[str, Any]) -> str:
        """Handle code analysis tasks using distributed StarCoder model."""
        code = payload.get("code", "")
        analysis_type = payload.get("analysis_type", "general")
        
        prompt = f"""Analyze this code for {analysis_type} aspects:

CODE:
{code}

Provide detailed analysis including:
- Code quality assessment
- Performance considerations
- Security issues
- Best practices recommendations
- Architecture suggestions

Analysis:"""
        
        return await self._get_model_response("analyze", prompt, max_tokens=2000)
    
    async def _handle_fix_task(self, payload: Dict[str, Any]) -> str:
        """Handle code fixing tasks using distributed Code Llama model."""
        code = payload.get("code", "")
        issue = payload.get("issue", "")
        
        prompt = f"""Fix the following code issue:

ISSUE: {issue}

CODE:
{code}

Provide the corrected code with explanations:"""
        
        return await self._get_model_response("fix", prompt, max_tokens=1500)
    
    async def _handle_clean_task(self, payload: Dict[str, Any]) -> str:
        """Handle code cleanup tasks using distributed Mistral model."""
        code = payload.get("code", "")
        
        prompt = f"""Clean up and improve this code:

CODE:
{code}

Provide:
1. Cleaned version with better structure
2. Explanations of improvements made
3. Any additional suggestions

Cleaned code:"""
        
        return await self._get_model_response("clean", prompt, max_tokens=2000)
    
    async def _handle_refactor_task(self, payload: Dict[str, Any]) -> str:
        """Handle refactoring tasks using distributed DeepSeek Coder model."""
        code = payload.get("code", "")
        refactor_goal = payload.get("goal", "improve structure")
        
        prompt = f"""Refactor this code to {refactor_goal}:

CODE:
{code}

Provide:
1. Refactored code with improved architecture
2. Explanation of changes made
3. Benefits of the refactoring

Refactored code:"""
        
        return await self._get_model_response("refactor", prompt, max_tokens=2500)
    
    async def _handle_optimize_task(self, payload: Dict[str, Any]) -> str:
        """Handle optimization tasks using distributed StarCoder model."""
        code = payload.get("code", "")
        optimization_target = payload.get("target", "performance")
        
        prompt = f"""Optimize this code for {optimization_target}:

CODE:
{code}

Provide:
1. Optimized version
2. Performance improvements explanation
3. Benchmarking suggestions

Optimized code:"""
        
        return await self._get_model_response("optimize", prompt, max_tokens=2000)
    
    async def _handle_document_task(self, payload: Dict[str, Any]) -> str:
        """Handle documentation tasks using distributed Code Llama model."""
        code = payload.get("code", "")
        doc_type = payload.get("type", "docstring")
        
        prompt = f"""Generate {doc_type} documentation for this code:

CODE:
{code}

Provide comprehensive documentation including:
- Function/class descriptions
- Parameter explanations
- Return value descriptions
- Usage examples
- Edge cases

Documentation:"""
        
        return await self._get_model_response("document", prompt, max_tokens=1500)
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
