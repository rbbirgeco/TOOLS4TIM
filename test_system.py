import asyncio
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from AdministrativeMesh.admin_dispatcher import dispatch
from NeuralCodingAssistant.scaffold import bootstrap_workspace

async def test_system():
    """Test the complete Neural Coding Assistant system."""
    print("🧪 Testing Neural Coding Assistant System\n")
    
    # Bootstrap the workspace
    bootstrap_workspace()
    print()
    
    # Test cases
    test_cases = [
        "Debug this TypeError: unsupported operand type(s) for +: 'int' and 'str'",
        "Analyze this Python function for optimization opportunities",
        "Fix the syntax error in my code",
        "Clean up this codebase and remove dead code"
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"🔍 Test {i}: {test_case}")
        try:
            result = await dispatch(test_case)
            print(f"✅ Result: {result[:100]}..." if len(result) > 100 else f"✅ Result: {result}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        print()

if __name__ == "__main__":
    asyncio.run(test_system())
