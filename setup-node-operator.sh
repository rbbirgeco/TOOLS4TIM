#!/bin/bash

# Free-S_Code Node Operator Setup Script
# ======================================
# This script helps community members set up model hosting nodes
# to join the Free-S_Code decentralized network

set -e

echo "🌐 Free-S_Code Node Operator Setup"
echo "=================================="
echo ""
echo "Welcome to the Free-S_Code network! This script will help you"
echo "set up a model hosting node to earn NetworkTokens by providing"
echo "AI inference services to the community."
echo ""

# Check system requirements
echo "📋 Checking system requirements..."

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3.8+ is required but not found"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
if [[ $(echo "$PYTHON_VERSION < 3.8" | bc) -eq 1 ]]; then
    echo "❌ Python 3.8+ is required (found $PYTHON_VERSION)"
    exit 1
fi
echo "✅ Python $PYTHON_VERSION found"

# Check available RAM
TOTAL_RAM=$(free -g | awk '/^Mem:/{print $2}')
if [[ $TOTAL_RAM -lt 8 ]]; then
    echo "⚠️  Warning: Only ${TOTAL_RAM}GB RAM available. Recommended: 16GB+ for optimal performance"
else
    echo "✅ ${TOTAL_RAM}GB RAM available"
fi

# Check available disk space
AVAILABLE_DISK=$(df -BG / | awk 'NR==2 {print $4}' | sed 's/G//')
if [[ $AVAILABLE_DISK -lt 50 ]]; then
    echo "⚠️  Warning: Only ${AVAILABLE_DISK}GB disk space available. Recommended: 100GB+ for model storage"
else
    echo "✅ ${AVAILABLE_DISK}GB disk space available"
fi

# Check for GPU
if command -v nvidia-smi &> /dev/null; then
    GPU_COUNT=$(nvidia-smi -L | wc -l)
    echo "✅ $GPU_COUNT NVIDIA GPU(s) detected"
    
    # Check GPU memory
    GPU_MEMORY=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits | head -1)
    echo "   GPU Memory: ${GPU_MEMORY}MB"
    
    if [[ $GPU_MEMORY -lt 8000 ]]; then
        echo "   ⚠️  GPU memory < 8GB. You can still host smaller models."
    fi
else
    echo "⚠️  No NVIDIA GPU detected. CPU-only inference will be slower but still valuable."
fi

echo ""

# Get node configuration from user
echo "⚙️  Node Configuration"
echo "====================="
echo ""

read -p "Enter a unique node ID (e.g., your-name-node1): " NODE_ID
if [[ -z "$NODE_ID" ]]; then
    echo "❌ Node ID cannot be empty"
    exit 1
fi

read -p "Enter the port for your node (default: 8080): " NODE_PORT
NODE_PORT=${NODE_PORT:-8080}

read -p "Enter your Free-S_Code wallet address (for NetworkToken payments): " WALLET_ADDRESS
if [[ -z "$WALLET_ADDRESS" ]]; then
    echo "❌ Wallet address is required for payments"
    exit 1
fi

echo ""
echo "📦 Installing Dependencies"
echo "========================="

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv free-s-code-node
source free-s-code-node/bin/activate

# Install required packages
echo "Installing required Python packages..."
pip install --upgrade pip
pip install aiohttp asyncio psutil py3nvml torch transformers accelerate

# Install GPU support if available
if command -v nvidia-smi &> /dev/null; then
    echo "Installing GPU support..."
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
fi

echo ""
echo "📁 Setting up Node Directory Structure"
echo "======================================"

# Create node directory
mkdir -p "free-s-code-node-$NODE_ID"
cd "free-s-code-node-$NODE_ID"

# Create configuration file
cat > node_config.json << EOF
{
    "node_id": "$NODE_ID",
    "host_port": $NODE_PORT,
    "wallet_address": "$WALLET_ADDRESS",
    "network_registry": "https://registry.free-s-code.net",
    "auto_start": true,
    "max_models": 3,
    "storage_path": "./models",
    "logs_path": "./logs",
    "earnings_threshold": 10.0,
    "health_check_interval": 300,
    "supported_models": [
        "mistral-7b",
        "code-llama-7b",
        "starcoder-15b"
    ]
}
EOF

# Create node startup script
cat > start_node.py << 'EOF'
#!/usr/bin/env python3
"""
Free-S_Code Node Startup Script
"""

import asyncio
import json
import os
import sys
import logging
from datetime import datetime

# Add the parent directory to path to import from Free-S_Code
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from LLM_Mesh.node_manager import ModelHostingNode, NetworkNodeManager
except ImportError:
    print("❌ Failed to import Free-S_Code modules. Please ensure Free-S_Code is properly installed.")
    sys.exit(1)

async def main():
    # Load configuration
    with open('node_config.json', 'r') as f:
        config = json.load(f)
    
    # Set up logging
    os.makedirs(config['logs_path'], exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f"{config['logs_path']}/node.log"),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger("NodeOperator")
    
    # Create and start node
    logger.info(f"🚀 Starting Free-S_Code node: {config['node_id']}")
    
    node = ModelHostingNode(config['node_id'], config['host_port'])
    
    # Create model storage directory
    os.makedirs(config['storage_path'], exist_ok=True)
    
    # Auto-load recommended models based on hardware
    logger.info("🤖 Auto-loading recommended models based on hardware capacity...")
    
    # Load lightweight model first
    await node.load_model("mistral-7b", f"{config['storage_path']}/mistral-7b", {
        "size_gb": 4.5,
        "ram_required_gb": 6.0,
        "specialties": ["reasoning", "analysis", "general"]
    })
    
    # Load additional models if capacity allows
    if node.capacity.available_ram_gb >= 16:
        logger.info("Sufficient RAM detected, loading Code Llama...")
        await node.load_model("code-llama-7b", f"{config['storage_path']}/code-llama-7b", {
            "size_gb": 5.2,
            "ram_required_gb": 8.0,
            "specialties": ["python", "debugging", "documentation"]
        })
    
    if node.capacity.available_ram_gb >= 24:
        logger.info("High RAM capacity detected, loading StarCoder...")
        await node.load_model("starcoder-15b", f"{config['storage_path']}/starcoder-15b", {
            "size_gb": 8.1,
            "ram_required_gb": 12.0,
            "specialties": ["code_generation", "optimization"]
        })
    
    # Start node server
    logger.info(f"🌐 Node will be available at http://localhost:{config['host_port']}")
    logger.info(f"💰 Earnings will be sent to wallet: {config['wallet_address']}")
    
    await node.start_node_server()

if __name__ == "__main__":
    print("🌐 Free-S_Code Node Operator")
    print("============================")
    print("Starting your model hosting node...")
    print("Press Ctrl+C to stop the node")
    print("")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Node shutdown complete. Thank you for contributing to Free-S_Code!")
EOF

chmod +x start_node.py

# Create systemd service file for auto-start (Linux only)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    cat > free-s-code-node.service << EOF
[Unit]
Description=Free-S_Code Model Hosting Node
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
ExecStart=$(pwd)/../free-s-code-node/bin/python start_node.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

    echo ""
    echo "🔧 System Service Setup (Optional)"
    echo "================================="
    echo "To run your node automatically on system startup:"
    echo "sudo cp free-s-code-node.service /etc/systemd/system/"
    echo "sudo systemctl enable free-s-code-node"
    echo "sudo systemctl start free-s-code-node"
fi

echo ""
echo "✅ Node Setup Complete!"
echo "======================"
echo ""
echo "Your Free-S_Code node has been configured with the following settings:"
echo "• Node ID: $NODE_ID"
echo "• Port: $NODE_PORT"
echo "• Wallet: $WALLET_ADDRESS"
echo ""
echo "📚 Next Steps:"
echo "1. Download models to ./models/ directory (or let auto-download handle it)"
echo "2. Start your node: python start_node.py"
echo "3. Register with the network (automatic on first start)"
echo "4. Start earning NetworkTokens!"
echo ""
echo "📊 Monitor your node:"
echo "• Health status: http://localhost:$NODE_PORT/health"
echo "• Logs: tail -f logs/node.log"
echo ""
echo "💰 Earnings Info:"
echo "• You earn NetworkTokens for each inference request served"
echo "• Monthly payouts are sent to your wallet address"
echo "• Higher uptime and performance = higher earnings"
echo ""
echo "🌐 Join the Community:"
echo "• Discord: https://discord.gg/free-s-code"
echo "• GitHub: https://github.com/timdowler/free-s-code"
echo "• Documentation: https://docs.free-s-code.net"
echo ""
echo "Thank you for joining the Free-S_Code network! 🚀"
