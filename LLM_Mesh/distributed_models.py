"""
Distributed Model Hosting System for Free-S_Code
================================================

Models are hosted on network nodes, not downloaded locally.
This module handles routing requests to distributed model hosts.
"""

import asyncio
import aiohttp
import json
import random
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class ModelHost:
    """Represents a network node hosting a model."""
    host_url: str
    health_score: float
    last_response_time: float
    specialties: List[str]
    available: bool = True
    last_health_check: datetime = None

@dataclass
class ModelInfo:
    """Information about a distributed model."""
    name: str
    hosts: List[ModelHost]
    token_cost_per_1k: float
    context_window: int
    specialties: List[str]
    description: str

class DistributedModelRegistry:
    """
    Central registry for distributed models across the Free-S_Code network.
    Models are hosted on community nodes, not downloaded locally.
    """
    
    def __init__(self):
        self.models = self._initialize_model_registry()
        self.health_check_interval = 300  # 5 minutes
        self.last_health_check = None
    
    def _initialize_model_registry(self) -> Dict[str, ModelInfo]:
        """Initialize the registry with available distributed models."""
        return {
            "starcoder-15b": ModelInfo(
                name="starcoder-15b",
                hosts=[
                    ModelHost("https://node1.free-s-code.net:8080", 0.95, 1.2, ["python", "javascript", "rust"]),
                    ModelHost("https://node5.free-s-code.net:8080", 0.87, 1.8, ["python", "javascript", "rust"]),
                    ModelHost("https://node12.free-s-code.net:8080", 0.92, 1.5, ["python", "javascript", "rust"])
                ],
                token_cost_per_1k=0.002,
                context_window=8192,
                specialties=["code_generation", "debugging", "optimization"],
                description="Advanced code generation and analysis model"
            ),
            
            "code-llama-7b": ModelInfo(
                name="code-llama-7b", 
                hosts=[
                    ModelHost("https://node3.free-s-code.net:8080", 0.92, 0.8, ["python", "debugging", "documentation"]),
                    ModelHost("https://node7.free-s-code.net:8080", 0.94, 0.9, ["python", "debugging", "documentation"]),
                    ModelHost("https://node15.free-s-code.net:8080", 0.89, 1.1, ["python", "debugging", "documentation"])
                ],
                token_cost_per_1k=0.001,
                context_window=100000,
                specialties=["python", "debugging", "documentation", "analysis"],
                description="Python-specialized model with 100k token context"
            ),
            
            "mistral-7b": ModelInfo(
                name="mistral-7b",
                hosts=[
                    ModelHost("https://node2.free-s-code.net:8080", 0.89, 0.7, ["reasoning", "analysis", "general"]),
                    ModelHost("https://node6.free-s-code.net:8080", 0.91, 0.6, ["reasoning", "analysis", "general"]),
                    ModelHost("https://node9.free-s-code.net:8080", 0.93, 0.8, ["reasoning", "analysis", "general"])
                ],
                token_cost_per_1k=0.0008,
                context_window=32768,
                specialties=["reasoning", "analysis", "planning", "general"],
                description="Fast reasoning and general assistance model"
            ),
            
            "deepseek-coder-33b": ModelInfo(
                name="deepseek-coder-33b",
                hosts=[
                    ModelHost("https://node4.free-s-code.net:8080", 0.88, 2.1, ["code_analysis", "refactoring"]),
                    ModelHost("https://node8.free-s-code.net:8080", 0.90, 1.9, ["code_analysis", "refactoring"]),
                    ModelHost("https://node11.free-s-code.net:8080", 0.86, 2.3, ["code_analysis", "refactoring"])
                ],
                token_cost_per_1k=0.003,
                context_window=16384,
                specialties=["code_analysis", "refactoring", "optimization", "architecture"],
                description="Large model for complex code analysis and refactoring"
            )
        }
    
    async def find_best_host(self, model_name: str, task_type: str = None) -> Optional[ModelHost]:
        """Find the best available host for a model based on health, response time, and specialties."""
        model_info = self.models.get(model_name)
        if not model_info:
            print(f"Model '{model_name}' not found in registry")
            return None
        
        # Filter available hosts
        available_hosts = [host for host in model_info.hosts if host.available]
        if not available_hosts:
            print(f"No available hosts for model '{model_name}'")
            return None
        
        # Score hosts based on multiple factors
        scored_hosts = []
        for host in available_hosts:
            score = host.health_score
            
            # Boost for specialty match
            if task_type and task_type in host.specialties:
                score *= 1.3
            
            # Penalty for slow response time
            if host.last_response_time > 2.0:
                score *= 0.8
            elif host.last_response_time > 1.0:
                score *= 0.9
            
            scored_hosts.append((score, host))
        
        # Sort by score and return the best host
        scored_hosts.sort(key=lambda x: x[0], reverse=True)
        return scored_hosts[0][1]
    
    async def route_request(self, model_name: str, prompt: str, task_type: str = None, 
                          max_tokens: int = 1000, temperature: float = 0.7) -> Dict[str, Any]:
        """Route a request to the best available host for the specified model."""
        
        # Find the best host
        host = await self.find_best_host(model_name, task_type)
        if not host:
            return {
                "error": f"No available hosts for model '{model_name}'",
                "success": False
            }
        
        # Prepare the request
        request_data = {
            "model": model_name,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "task_type": task_type
        }
        
        # Route to the selected host
        try:
            start_time = asyncio.get_event_loop().time()
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{host.host_url}/v1/completions",
                    json=request_data,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        
                        # Update host performance metrics
                        response_time = asyncio.get_event_loop().time() - start_time
                        host.last_response_time = response_time
                        
                        # Calculate token cost
                        model_info = self.models[model_name]
                        estimated_tokens = len(prompt.split()) + max_tokens  # Rough estimate
                        token_cost = (estimated_tokens / 1000) * model_info.token_cost_per_1k
                        
                        return {
                            "success": True,
                            "response": result.get("choices", [{}])[0].get("text", ""),
                            "model": model_name,
                            "host": host.host_url,
                            "response_time": response_time,
                            "estimated_cost": token_cost,
                            "token_count": estimated_tokens
                        }
                    else:
                        # Mark host as temporarily unavailable
                        host.available = False
                        return {
                            "error": f"Host {host.host_url} returned status {response.status}",
                            "success": False
                        }
                        
        except asyncio.TimeoutError:
            host.available = False
            return {
                "error": f"Request to {host.host_url} timed out",
                "success": False
            }
        except Exception as e:
            host.available = False
            return {
                "error": f"Request to {host.host_url} failed: {str(e)}",
                "success": False
            }
    
    async def health_check_all_hosts(self):
        """Perform health checks on all registered hosts."""
        print("Performing health checks on all model hosts...")
        
        for model_name, model_info in self.models.items():
            for host in model_info.hosts:
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(
                            f"{host.host_url}/health",
                            timeout=aiohttp.ClientTimeout(total=10)
                        ) as response:
                            
                            if response.status == 200:
                                health_data = await response.json()
                                host.health_score = health_data.get("health_score", 0.5)
                                host.available = True
                                host.last_health_check = datetime.now()
                                print(f"✅ {host.host_url} - Health: {host.health_score:.2f}")
                            else:
                                host.available = False
                                print(f"❌ {host.host_url} - Status: {response.status}")
                                
                except Exception as e:
                    host.available = False
                    print(f"❌ {host.host_url} - Error: {str(e)}")
        
        self.last_health_check = datetime.now()
        print(f"Health check completed at {self.last_health_check}")
    
    def get_model_info(self, model_name: str = None) -> Dict[str, Any]:
        """Get information about available models."""
        if model_name:
            model_info = self.models.get(model_name)
            if not model_info:
                return {"error": f"Model '{model_name}' not found"}
            
            return {
                "name": model_info.name,
                "description": model_info.description,
                "specialties": model_info.specialties,
                "context_window": model_info.context_window,
                "cost_per_1k_tokens": model_info.token_cost_per_1k,
                "available_hosts": len([h for h in model_info.hosts if h.available]),
                "total_hosts": len(model_info.hosts)
            }
        
        # Return info for all models
        return {
            model_name: {
                "description": info.description,
                "specialties": info.specialties,
                "context_window": info.context_window,
                "cost_per_1k_tokens": info.token_cost_per_1k,
                "available_hosts": len([h for h in info.hosts if h.available]),
                "total_hosts": len(info.hosts)
            }
            for model_name, info in self.models.items()
        }

# Global registry instance
model_registry = DistributedModelRegistry()

async def get_model_response(model_name: str, prompt: str, task_type: str = None, 
                           max_tokens: int = 1000, temperature: float = 0.7) -> Dict[str, Any]:
    """
    Convenience function to get a response from a distributed model.
    
    Args:
        model_name: Name of the model to use
        prompt: The prompt to send to the model
        task_type: Optional task type for specialty routing
        max_tokens: Maximum tokens to generate
        temperature: Sampling temperature
    
    Returns:
        Dict containing the response and metadata
    """
    return await model_registry.route_request(
        model_name=model_name,
        prompt=prompt,
        task_type=task_type,
        max_tokens=max_tokens,
        temperature=temperature
    )

async def initialize_distributed_models():
    """Initialize the distributed model system."""
    print("🌐 Initializing distributed model system...")
    print("Models are hosted on network nodes, not downloaded locally.")
    
    # Perform initial health check
    await model_registry.health_check_all_hosts()
    
    print("✅ Distributed model system initialized")
    print(f"Available models: {list(model_registry.models.keys())}")

if __name__ == "__main__":
    # Example usage
    async def test_distributed_models():
        await initialize_distributed_models()
        
        # Test getting model info
        print("\nModel Registry:")
        print(json.dumps(model_registry.get_model_info(), indent=2))
        
        # Test a simple request (this would fail in a real environment without actual hosts)
        print("\nTesting request routing...")
        result = await get_model_response(
            model_name="mistral-7b",
            prompt="def fibonacci(n):",
            task_type="python",
            max_tokens=100
        )
        print(f"Request result: {result}")
    
    asyncio.run(test_distributed_models())
