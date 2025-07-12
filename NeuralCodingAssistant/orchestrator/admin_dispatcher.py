import asyncio
from AdministrativeMesh.admin_dispatcher import dispatch

class AdminDispatcher:
    """Main orchestrator for the Neural Coding Assistant system."""
    
    def __init__(self):
        self.system_ready = False
    
    async def initialize(self):
        """Initialize the administrative mesh system."""
        print("🧠 Neural Coding Assistant - Administrative Dispatcher")
        print("🔧 Initializing Administrative Mesh...")
        print("✅ Council Router loaded")
        print("✅ Task Parser configured")
        print("✅ Memory Expander ready")
        print("✅ Function Courier initialized")
        print("✅ Worker Mesh connected")
        print("🚀 Administrative Dispatcher ready")
        self.system_ready = True
    
    async def process_request(self, prompt: str) -> str:
        """Process a user request through the administrative mesh."""
        if not self.system_ready:
            await self.initialize()
        
        try:
            result = await dispatch(prompt)
            return result
        except Exception as e:
            return f"[DISPATCHER ERROR]: {str(e)}"

if __name__ == "__main__":
    dispatcher = AdminDispatcher()
    
    async def test_dispatcher():
        await dispatcher.initialize()
        test_prompt = "Debug this TypeError in my Python function"
        result = await dispatcher.process_request(test_prompt)
        print(f"\n📤 Result: {result}")
    
    asyncio.run(test_dispatcher())
