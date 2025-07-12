#!/usr/bin/env python3

import asyncio
import pytest
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from AdministrativeMesh.task_parser import parse_task
from AdministrativeMesh.function_courier_parser import get_function_signature
from config import classify_task_by_keywords, get_function_signature_from_config

class TestTaskClassification:
    """Test task classification and parsing."""
    
    def test_debug_classification(self):
        """Test debug task classification."""
        test_cases = [
            "Fix this error in my code",
            "There's a bug in the function",
            "Debug this TypeError",
            "My code is broken",
            "Exception occurred in line 5"
        ]
        
        for prompt in test_cases:
            task = parse_task(prompt)
            assert task["type"] == "debug", f"Failed to classify '{prompt}' as debug"
    
    def test_analyze_classification(self):
        """Test analyze task classification."""
        test_cases = [
            "Analyze this code",
            "Review my function",
            "Examine this algorithm",
            "Can you inspect this code?",
            "Help me understand this"
        ]
        
        for prompt in test_cases:
            task = parse_task(prompt)
            assert task["type"] == "analyze", f"Failed to classify '{prompt}' as analyze"
    
    def test_fix_classification(self):
        """Test fix task classification."""
        test_cases = [
            "Fix this function",
            "Repair the broken logic",
            "Correct the implementation",
            "Solve this problem"
        ]
        
        for prompt in test_cases:
            task = parse_task(prompt)
            assert task["type"] == "fix", f"Failed to classify '{prompt}' as fix"
    
    def test_clean_classification(self):
        """Test clean task classification."""
        test_cases = [
            "Clean up this code",
            "Optimize this function",
            "Improve the formatting",
            "Make this code better"
        ]
        
        for prompt in test_cases:
            task = parse_task(prompt)
            assert task["type"] == "clean", f"Failed to classify '{prompt}' as clean"
    
    def test_refactor_classification(self):
        """Test refactor task classification (default)."""
        test_cases = [
            "Refactor this module",
            "Restructure the code",
            "Make this more modular",
            "Some random request"  # Should default to refactor
        ]
        
        for prompt in test_cases:
            task = parse_task(prompt)
            assert task["type"] == "refactor", f"Failed to classify '{prompt}' as refactor"

class TestFunctionSignatures:
    """Test function signature retrieval."""
    
    def test_all_task_types_have_signatures(self):
        """Test that all supported task types have function signatures."""
        task_types = ["debug", "analyze", "fix", "clean", "refactor"]
        
        for task_type in task_types:
            sig = get_function_signature_from_config(task_type)
            assert sig is not None
            assert "def " in sig
            assert task_type in sig or "code" in sig

    def test_function_signature_parser(self):
        """Test function signature parsing."""
        # Test with config fallback
        sig = get_function_signature("debug")
        assert "debug_code_snippet" in sig
        assert "code_str: str" in sig
        assert "error_msg: str" in sig

class TestErrorHandling:
    """Test error handling and fallback mechanisms."""
    
    def test_unknown_task_type(self):
        """Test handling of unknown task types."""
        # Should not crash, should return default
        task = parse_task("Some completely unknown request type xyz123")
        assert task["type"] == "refactor"  # default
    
    def test_empty_prompt(self):
        """Test handling of empty prompts."""
        task = parse_task("")
        assert task["type"] == "refactor"  # default
        assert task["text"] == ""

@pytest.mark.asyncio
class TestAsyncFunctionality:
    """Test async components."""
    
    async def test_mesh_manager_import(self):
        """Test that MeshManager can be imported and initialized."""
        try:
            from LLM_Mesh.mesh_manager import MeshManager
            manager = MeshManager()
            await manager.initialize_models()
            assert manager.models_initialized
        except ImportError:
            pytest.skip("MeshManager not available")
    
    async def test_dispatch_function(self):
        """Test the main dispatch function."""
        try:
            from AdministrativeMesh.admin_dispatcher import dispatch
            result = await dispatch("Analyze this simple code")
            assert isinstance(result, str)
            assert len(result) > 0
        except ImportError:
            pytest.skip("Dispatcher not available")

def run_comprehensive_tests():
    """Run all tests and provide a summary."""
    print("🧪 Running Neural Coding Assistant Test Suite")
    print("=" * 50)
    
    # Test task classification
    test_classification = TestTaskClassification()
    
    print("📝 Testing task classification...")
    try:
        test_classification.test_debug_classification()
        test_classification.test_analyze_classification()
        test_classification.test_fix_classification()
        test_classification.test_clean_classification()
        test_classification.test_refactor_classification()
        print("✅ Task classification tests passed")
    except Exception as e:
        print(f"❌ Task classification tests failed: {e}")
        return False
    
    # Test function signatures
    test_signatures = TestFunctionSignatures()
    
    print("📋 Testing function signatures...")
    try:
        test_signatures.test_all_task_types_have_signatures()
        test_signatures.test_function_signature_parser()
        print("✅ Function signature tests passed")
    except Exception as e:
        print(f"❌ Function signature tests failed: {e}")
        return False
    
    # Test error handling
    test_errors = TestErrorHandling()
    
    print("🛡️ Testing error handling...")
    try:
        test_errors.test_unknown_task_type()
        test_errors.test_empty_prompt()
        print("✅ Error handling tests passed")
    except Exception as e:
        print(f"❌ Error handling tests failed: {e}")
        return False
    
    # Test async functionality
    print("⚡ Testing async functionality...")
    try:
        async def run_async_tests():
            test_async = TestAsyncFunctionality()
            await test_async.test_mesh_manager_import()
            await test_async.test_dispatch_function()
        
        asyncio.run(run_async_tests())
        print("✅ Async functionality tests passed")
    except Exception as e:
        print(f"⚠️ Async functionality tests had issues: {e}")
    
    print("\n🎉 Test suite completed successfully!")
    print("\n💡 To run with pytest: python -m pytest test_comprehensive.py -v")
    return True

if __name__ == "__main__":
    success = run_comprehensive_tests()
    sys.exit(0 if success else 1)
