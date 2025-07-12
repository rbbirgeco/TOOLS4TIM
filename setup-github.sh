#!/bin/bash

echo "🚀 Setting up Neural Coding Assistant for GitHub"
echo "================================================"

# Initialize git repository if not already done
if [ ! -d ".git" ]; then
    echo "📁 Initializing Git repository..."
    git init
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

# Add all files to git
echo "📋 Adding files to Git..."
git add .

# Create initial commit if no commits exist
if [ -z "$(git log --oneline 2>/dev/null)" ]; then
    echo "💾 Creating initial commit..."
    git commit -m "Initial commit: Neural Coding Assistant

🧠 Features:
- Administrative Mesh with council-based routing
- Function Courier for zero-hallucination execution  
- GGUF model support with fallback mode
- FastAPI REST server with OpenAI compatibility
- VS Code integration via Continue extension
- Async worker system for code debugging, analysis, fixing, and cleaning
- Docker containerization support

🏗️ Architecture:
- Administrative Mesh: Task routing and execution management
- Function Courier: Verified function signatures
- Workers: Specialized AI models for coding tasks
- LLM Mesh: Model management and inference
- Agent Memory: Persistent context and learning

🔧 Ready for deployment and development!"
    echo "✅ Initial commit created"
else
    echo "✅ Repository already has commits"
fi

echo ""
echo "🎯 Next Steps:"
echo "=============="
echo ""
echo "1. 🌐 Create GitHub repository:"
echo "   - Go to https://github.com/rbbirgeco"
echo "   - Click 'New repository'"
echo "   - Name: TOOLS4TIM"
echo "   - Description: Neural Coding Assistant with Administrative Mesh Architecture"
echo "   - Keep it Public"
echo "   - DO NOT initialize with README (we have one)"
echo "   - Click 'Create repository'"
echo ""
echo "2. 🔗 Connect local repository to GitHub:"
echo "   git remote add origin https://github.com/rbbirgeco/TOOLS4TIM.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. 📋 Optional - Add repository topics on GitHub:"
echo "   - ai-assistant"
echo "   - coding-assistant" 
echo "   - neural-networks"
echo "   - fastapi"
echo "   - vscode-extension"
echo "   - llm"
echo "   - gguf"
echo "   - administrative-mesh"
echo ""
echo "4. 🛡️ Set up branch protection (recommended):"
echo "   - Go to Settings > Branches"
echo "   - Add rule for 'main' branch"
echo "   - Require pull request reviews"
echo ""
echo "📁 Repository is ready for GitHub!"
echo "🌟 Don't forget to add a star to your own repo! ⭐"
