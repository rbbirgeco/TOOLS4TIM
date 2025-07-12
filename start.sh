#!/bin/bash

# Neural Coding Assistant - Easy Start Script

echo "🧠 Neural Coding Assistant - Starting System"
echo "==========================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

# Create and activate virtual environment
VENV_DIR="venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv $VENV_DIR
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "� Activating virtual environment..."
source $VENV_DIR/bin/activate

# Upgrade pip and install basic tools
echo "⬆️  Upgrading pip and build tools..."
pip install --upgrade pip setuptools wheel

# Install dependencies with fallback approach
if [ -f "requirements.txt" ]; then
    echo "📦 Installing dependencies in virtual environment..."
    
    # Try installing everything at once first
    pip install -r requirements.txt
    
    # If that fails, try installing core packages individually
    if [ $? -ne 0 ]; then
        echo "⚠️  Batch install failed, trying individual packages..."
        
        # Install core packages first
        echo "� Installing FastAPI and core web framework..."
        pip install fastapi uvicorn[standard] pydantic
        
        echo "📦 Installing basic utilities..."
        pip install aiofiles python-multipart httpx
        
        echo "📦 Installing testing framework..."
        pip install pytest pytest-asyncio
        
        echo "📦 Installing numpy..."
        pip install numpy
        
        # Try llama-cpp-python last (most likely to fail)
        echo "📦 Attempting to install llama-cpp-python..."
        pip install llama-cpp-python || echo "⚠️  llama-cpp-python installation failed - will use fallback mode"
    fi
    
    echo "✅ Core dependencies installed"
else
    echo "⚠️  requirements.txt not found, skipping dependency installation"
fi

# Run system test
echo "🧪 Running system test..."
python test_system.py

# Start the REST API server
echo "🚀 Starting Neural Coding Assistant API server..."
echo "📡 Server will be available at http://localhost:8080"
echo "🔗 Configure Continue extension to use: http://localhost:8080"
echo "💡 Virtual environment is active - use 'deactivate' to exit"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start uvicorn server (now in virtual environment)
uvicorn rest_api:app --host 0.0.0.0 --port 8080 --reload
