#!/bin/bash

# Quick activation script for development
echo "🔌 Activating Neural Coding Assistant virtual environment..."

if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Virtual environment activated"
    echo "💡 You can now run: python rest_api.py or uvicorn rest_api:app --reload"
    echo "💡 To deactivate, type: deactivate"
else
    echo "❌ Virtual environment not found. Run ./start.sh first to create it."
fi
