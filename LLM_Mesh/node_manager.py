"""
Network Node Manager for Free-S_Code
===================================

Manages model hosting nodes in the distributed network.
Each node can host one or more AI models and serve inference requests.
"""

import asyncio
import aiohttp
import psutil
import GPUtil
import json
import os
import sys
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import subprocess
import logging

@dataclass
class NodeCapacity:
    """Hardware capacity information for a node."""
    cpu_cores: int
    total_ram_gb: float
    available_ram_gb: float
    gpu_count: int
    gpu_memory_gb: List[float]
    disk_space_gb: float
    network_bandwidth_mbps: float

@dataclass
class ModelLoadInfo:
    """Information about a loaded model on a node."""
    model_name: str
    model_size_gb: float
    ram_usage_gb: float
    gpu_usage_gb: float
    load_time_seconds: float
    requests_served: int
    avg_response_time: float
    last_request_time: datetime

class ModelHostingNode:
    """
    A node in the Free-S_Code network that hosts AI models.
    Can run multiple models depending on hardware capacity.
    """
    
    def __init__(self, node_id: str, host_port: int = 8080):
        self.node_id = node_id
        self.host_port = host_port
        self.capacity = self._get_hardware_capacity()
        self.loaded_models: Dict[str, ModelLoadInfo] = {}
        self.is_running = False
        self.health_score = 1.0
        self.earnings = 0.0  # NetworkTokens earned
        
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(f"Node-{node_id}")
    
    def _get_hardware_capacity(self) -> NodeCapacity:
        """Detect hardware capacity of this node."""
        # CPU info
        cpu_cores = psutil.cpu_count()
        
        # RAM info
        ram = psutil.virtual_memory()
        total_ram_gb = ram.total / (1024**3)
        available_ram_gb = ram.available / (1024**3)
        
        # GPU info
        gpu_count = 0
        gpu_memory_gb = []
        try:
            gpus = GPUtil.getGPUs()
            gpu_count = len(gpus)
            gpu_memory_gb = [gpu.memoryTotal / 1024 for gpu in gpus]  # Convert MB to GB
        except:
            pass  # No GPUs available
        
        # Disk space
        disk = psutil.disk_usage('/')
        disk_space_gb = disk.free / (1024**3)
        
        # Network bandwidth (estimate)
        network_bandwidth_mbps = 100.0  # Default estimate
        
        return NodeCapacity(
            cpu_cores=cpu_cores,
            total_ram_gb=total_ram_gb,
            available_ram_gb=available_ram_gb,
            gpu_count=gpu_count,
            gpu_memory_gb=gpu_memory_gb,
            disk_space_gb=disk_space_gb,
            network_bandwidth_mbps=network_bandwidth_mbps
        )
    
    def can_host_model(self, model_name: str, model_size_gb: float, ram_required_gb: float) -> bool:
        """Check if this node has capacity to host a new model."""
        # Check RAM availability
        current_ram_usage = sum(model.ram_usage_gb for model in self.loaded_models.values())
        if (current_ram_usage + ram_required_gb) > (self.capacity.available_ram_gb * 0.8):  # 80% safety margin
            return False
        
        # Check disk space
        if model_size_gb > (self.capacity.disk_space_gb * 0.9):  # 90% safety margin
            return False
        
        # Check if already hosting this model
        if model_name in self.loaded_models:
            return False
        
        return True
    
    async def load_model(self, model_name: str, model_path: str, model_config: Dict[str, Any]) -> bool:
        """Load a model onto this node."""
        if not self.can_host_model(
            model_name, 
            model_config.get("size_gb", 5.0),
            model_config.get("ram_required_gb", 8.0)
        ):
            self.logger.warning(f"Cannot host model {model_name} - insufficient capacity")
            return False
        
        self.logger.info(f"Loading model {model_name}...")
        start_time = datetime.now()
        
        try:
            # In a real implementation, this would load the actual model
            # For now, we simulate the loading process
            await asyncio.sleep(2)  # Simulate model loading time
            
            load_time = (datetime.now() - start_time).total_seconds()
            
            # Record model load info
            self.loaded_models[model_name] = ModelLoadInfo(
                model_name=model_name,
                model_size_gb=model_config.get("size_gb", 5.0),
                ram_usage_gb=model_config.get("ram_required_gb", 8.0),
                gpu_usage_gb=model_config.get("gpu_required_gb", 0.0),
                load_time_seconds=load_time,
                requests_served=0,
                avg_response_time=0.0,
                last_request_time=datetime.now()
            )
            
            self.logger.info(f"✅ Model {model_name} loaded in {load_time:.2f}s")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load model {model_name}: {str(e)}")
            return False
    
    async def unload_model(self, model_name: str) -> bool:
        """Unload a model from this node."""
        if model_name not in self.loaded_models:
            self.logger.warning(f"Model {model_name} not loaded on this node")
            return False
        
        try:
            # In a real implementation, this would unload the actual model
            del self.loaded_models[model_name]
            self.logger.info(f"✅ Model {model_name} unloaded")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to unload model {model_name}: {str(e)}")
            return False
    
    async def handle_inference_request(self, model_name: str, prompt: str, max_tokens: int = 1000) -> Dict[str, Any]:
        """Handle an inference request for a loaded model."""
        if model_name not in self.loaded_models:
            return {
                "error": f"Model {model_name} not loaded on this node",
                "success": False
            }
        
        model_info = self.loaded_models[model_name]
        start_time = datetime.now()
        
        try:
            # In a real implementation, this would call the actual model
            # For now, we simulate the inference
            await asyncio.sleep(0.5)  # Simulate inference time
            
            response_time = (datetime.now() - start_time).total_seconds()
            
            # Update model statistics
            model_info.requests_served += 1
            model_info.avg_response_time = (
                (model_info.avg_response_time * (model_info.requests_served - 1) + response_time) /
                model_info.requests_served
            )
            model_info.last_request_time = datetime.now()
            
            # Calculate earnings (simplified)
            token_count = len(prompt.split()) + max_tokens  # Rough estimate
            earnings = (token_count / 1000) * 0.001  # $0.001 per 1k tokens
            self.earnings += earnings
            
            return {
                "success": True,
                "response": f"[SIMULATED RESPONSE] Generated text for prompt: {prompt[:50]}...",
                "model": model_name,
                "node_id": self.node_id,
                "response_time": response_time,
                "token_count": token_count,
                "earnings": earnings
            }
            
        except Exception as e:
            return {
                "error": f"Inference failed: {str(e)}",
                "success": False
            }
    
    async def get_health_status(self) -> Dict[str, Any]:
        """Get current health status of this node."""
        # Update hardware metrics
        current_capacity = self._get_hardware_capacity()
        
        # Calculate health score based on various factors
        ram_utilization = 1.0 - (current_capacity.available_ram_gb / current_capacity.total_ram_gb)
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # Health score factors
        ram_score = max(0, 1.0 - (ram_utilization / 0.9))  # Penalty if RAM > 90%
        cpu_score = max(0, 1.0 - (cpu_percent / 90.0))    # Penalty if CPU > 90%
        model_score = min(1.0, len(self.loaded_models) / 3.0)  # Bonus for hosting models
        
        self.health_score = (ram_score + cpu_score + model_score) / 3.0
        
        return {
            "node_id": self.node_id,
            "health_score": self.health_score,
            "capacity": asdict(current_capacity),
            "loaded_models": {
                name: {
                    "requests_served": info.requests_served,
                    "avg_response_time": info.avg_response_time,
                    "ram_usage_gb": info.ram_usage_gb,
                    "last_request": info.last_request_time.isoformat()
                }
                for name, info in self.loaded_models.items()
            },
            "total_earnings": self.earnings,
            "is_running": self.is_running
        }
    
    async def start_node_server(self):
        """Start the HTTP server for this node."""
        from aiohttp import web
        
        app = web.Application()
        
        # Health check endpoint
        async def health_handler(request):
            health_status = await self.get_health_status()
            return web.json_response(health_status)
        
        # Inference endpoint
        async def inference_handler(request):
            data = await request.json()
            model_name = data.get("model")
            prompt = data.get("prompt")
            max_tokens = data.get("max_tokens", 1000)
            
            result = await self.handle_inference_request(model_name, prompt, max_tokens)
            return web.json_response(result)
        
        # Model management endpoints
        async def load_model_handler(request):
            data = await request.json()
            model_name = data.get("model_name")
            model_path = data.get("model_path")
            model_config = data.get("config", {})
            
            success = await self.load_model(model_name, model_path, model_config)
            return web.json_response({"success": success})
        
        async def unload_model_handler(request):
            data = await request.json()
            model_name = data.get("model_name")
            
            success = await self.unload_model(model_name)
            return web.json_response({"success": success})
        
        # Set up routes
        app.router.add_get("/health", health_handler)
        app.router.add_post("/v1/completions", inference_handler)
        app.router.add_post("/load_model", load_model_handler)
        app.router.add_post("/unload_model", unload_model_handler)
        
        # Start server
        self.is_running = True
        self.logger.info(f"🚀 Starting node {self.node_id} on port {self.host_port}")
        
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, 'localhost', self.host_port)
        await site.start()
        
        self.logger.info(f"✅ Node {self.node_id} running on http://localhost:{self.host_port}")
        
        # Keep the server running
        try:
            while self.is_running:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            self.logger.info(f"Shutting down node {self.node_id}")
        finally:
            await runner.cleanup()

class NetworkNodeManager:
    """Manages multiple model hosting nodes in the Free-S_Code network."""
    
    def __init__(self):
        self.nodes: Dict[str, ModelHostingNode] = {}
        self.model_registry_url = "https://registry.free-s-code.net"
        
    async def create_node(self, node_id: str, host_port: int = 8080) -> ModelHostingNode:
        """Create a new model hosting node."""
        if node_id in self.nodes:
            raise ValueError(f"Node {node_id} already exists")
        
        node = ModelHostingNode(node_id, host_port)
        self.nodes[node_id] = node
        return node
    
    async def start_node(self, node_id: str):
        """Start a model hosting node."""
        if node_id not in self.nodes:
            raise ValueError(f"Node {node_id} not found")
        
        node = self.nodes[node_id]
        await node.start_node_server()
    
    async def register_node_with_network(self, node_id: str):
        """Register a node with the Free-S_Code network registry."""
        if node_id not in self.nodes:
            raise ValueError(f"Node {node_id} not found")
        
        node = self.nodes[node_id]
        health_status = await node.get_health_status()
        
        # In a real implementation, this would register with the central registry
        print(f"🌐 Registering node {node_id} with network...")
        print(f"Node capacity: {health_status['capacity']}")
        print(f"✅ Node {node_id} registered with network")
    
    def get_network_status(self) -> Dict[str, Any]:
        """Get status of all nodes in this network."""
        return {
            "total_nodes": len(self.nodes),
            "running_nodes": len([n for n in self.nodes.values() if n.is_running]),
            "total_models": sum(len(n.loaded_models) for n in self.nodes.values()),
            "total_earnings": sum(n.earnings for n in self.nodes.values()),
            "nodes": {
                node_id: {
                    "health_score": node.health_score,
                    "loaded_models": list(node.loaded_models.keys()),
                    "earnings": node.earnings,
                    "is_running": node.is_running
                }
                for node_id, node in self.nodes.items()
            }
        }

# Example usage and setup script
async def setup_local_node_cluster():
    """Set up a local cluster of model hosting nodes for testing."""
    manager = NetworkNodeManager()
    
    # Create multiple nodes
    node1 = await manager.create_node("node1", 8081)
    node2 = await manager.create_node("node2", 8082)
    node3 = await manager.create_node("node3", 8083)
    
    # Load different models on different nodes
    await node1.load_model("mistral-7b", "/models/mistral-7b", {"size_gb": 4.5, "ram_required_gb": 6.0})
    await node2.load_model("code-llama-7b", "/models/code-llama-7b", {"size_gb": 5.2, "ram_required_gb": 8.0})
    await node3.load_model("starcoder-15b", "/models/starcoder-15b", {"size_gb": 8.1, "ram_required_gb": 12.0})
    
    # Register nodes with network
    await manager.register_node_with_network("node1")
    await manager.register_node_with_network("node2")
    await manager.register_node_with_network("node3")
    
    print("🌐 Local node cluster set up successfully!")
    print(json.dumps(manager.get_network_status(), indent=2))
    
    return manager

if __name__ == "__main__":
    # Example: Set up and run a local node
    async def run_single_node():
        node = ModelHostingNode("test-node", 8080)
        
        # Load a test model
        await node.load_model("mistral-7b", "/models/mistral-7b", {
            "size_gb": 4.5,
            "ram_required_gb": 6.0
        })
        
        # Start the node server
        await node.start_node_server()
    
    print("🚀 Starting Free-S_Code model hosting node...")
    asyncio.run(run_single_node())
