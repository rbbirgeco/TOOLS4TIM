#!/bin/bash

echo "🔧 Neural Coding Assistant - Quick Setup"
echo "========================================"

# Clean start - remove existing venv if it has issues
if [ -d "venv" ]; then
    echo "🗑️  Removing existing virtual environment..."
    rm -rf venv
fi

# Create new virtual environment
echo "🔧 Creating fresh virtual environment..."
python3 -m venv venv

# Activate it
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install minimal dependencies first
echo "📦 Installing minimal core dependencies..."
pip install --upgrade pip setuptools wheel

# Install core web framework
echo "📦 Installing FastAPI and Uvicorn..."
pip install fastapi uvicorn[standard] pydantic

# Install utilities
echo "📦 Installing utilities..."
pip install aiofiles python-multipart httpx pytest pytest-asyncio

# Test basic system without GGUF models
echo "🧪 Testing basic system..."
python -c "
import fastapi
import uvicorn
import pydantic
print('✅ Core dependencies working!')
print('🚀 System ready to run in fallback mode')
"

echo ""
echo "✅ Basic setup complete!"
echo "💡 You can now run: source venv/bin/activate && python rest_api.py"
echo "⚠️  Running in fallback mode (no GGUF models) - responses will be mock data"
echo ""
echo "🔧 To install full GGUF support later, run:"
echo "   source venv/bin/activate && pip install llama-cpp-python"
