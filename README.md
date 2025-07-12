# Neural Coding Assistant

🧠 An AI-powered coding assistant with administrative mesh architecture that integrates with VS Code through Continue.

## Architecture

```
Neural Coding Assistant/
├── Administrative Mesh/     # Council-based task routing
├── Function Courier/        # Zero-copy function signatures  
├── Workers/                 # Specialized AI workers
├── LLM Mesh/               # Model management
├── Agent Memory/           # Persistent context
└── REST API/               # VS Code integration
```

## Features

- 🎯 **Zero Hallucination**: Function Courier enforces verified signatures
- 🤖 **Multi-Model Council**: Intelligent task routing to specialized models
- ⚡ **Async Workers**: Non-blocking subprocess execution
- 🧠 **Persistent Memory**: Context-aware learning and adaptation
- 🔌 **VS Code Integration**: Seamless Continue extension support
- 🐳 **Containerized**: Docker deployment ready

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the API Server

```bash
# Local development
uvicorn rest_api:app --host 0.0.0.0 --port 8080

# Or using VS Code task (Ctrl+Shift+B)
# Select "Start Assistant REST API"
```

### 3. Configure Continue

Copy the configuration to your Continue settings:

```bash
cp continue_config.json ~/.continue/config.json
```

### 4. Use in VS Code

Open VS Code and use the Continue extension:
- Command Palette → "Continue: Ask Neural Assistant"
- Use custom commands: Debug Code, Analyze Component, Clean Codebase

## Docker Deployment

```bash
# Build container
docker build -t neural-assistant .

# Run container
docker run -p 8080:8080 neural-assistant
```

## System Components

### Administrative Mesh
- **Council Router**: Selects optimal admin model
- **Task Parser**: Classifies and routes requests
- **Memory Expander**: Context-aware memory injection
- **Lifecycle Logger**: Tracks task execution

### Function Courier
- **Signature Parser**: Enforces function contracts
- **Zero-Copy Calls**: Direct memory access patterns
- **Verification**: Prevents function hallucination

### Workers
- **Debugger Worker**: Wolfram Language analysis
- **Analyzer Worker**: Deep contextual inspection  
- **Fixer Worker**: PyTorch-based code generation
- **Cleaner Worker**: Dead code removal
- **Fixer Helper**: Patch merging assistance

### LLM Mesh
- **StarCoder-15B**: 8K context code model
- **Code Llama 7B**: Python specialist, 100K tokens
- **Mistral 7B**: Fast reasoning and analysis

## API Endpoints

- `POST /v1/chat/completions` - OpenAI-compatible chat
- `GET /health` - Health check
- `GET /` - Service information

## Development

### VS Code Tasks
- **Start Assistant REST API**: Launch the main server
- **Install Dependencies**: Install Python packages
- **Docker Build**: Build container image
- **Docker Run**: Run containerized version

### Debug Configurations
- **Run REST API**: Debug the main API server
- **Test Admin Dispatcher**: Test the administrative mesh
- **Bootstrap Workspace**: Initialize the system
- **Test Worker**: Debug individual workers

## Architecture Principles

1. **No Polling**: Direct async execution
2. **No Routing Overhead**: Zero-copy memory patterns  
3. **Function Verification**: Courier-enforced signatures
4. **Stateless Workers**: Clean execution boundaries
5. **Context Awareness**: Memory-driven intelligence

## Contributing

The system is designed for extensibility:

1. Add new workers in `NeuralCodingAssistant/workers/`
2. Update Function_Courier.md with new signatures
3. Configure routing in `AdministrativeMesh/`
4. Test integration through VS Code

## License

Open source - see LICENSE file for details.
