# Project Structure

This document outlines the complete structure of the Neural Coding Assistant project.

## 📁 Root Directory

```
Free-S_Code/
├── 📄 README.md                    # Main project documentation
├── 📄 LICENSE                      # MIT License
├── 📄 CONTRIBUTING.md              # Contribution guidelines
├── 📄 requirements.txt             # Python dependencies
├── 📄 requirements-minimal.txt     # Minimal dependencies for fallback mode
├── 📄 Dockerfile                   # Docker containerization
├── 📄 .gitignore                   # Git ignore rules
├── 📄 rest_api.py                  # Main FastAPI server
├── 📄 test_system.py               # System integration tests
├── 🔧 start.sh                     # Full system startup script
├── 🔧 quick-setup.sh               # Quick setup for development
├── 🔧 activate.sh                  # Virtual environment activation
├── 🔧 setup-github.sh              # GitHub repository setup
├── 📁 .vscode/                     # VS Code configuration
├── 📁 AdministrativeMesh/          # Council-based task routing
├── 📁 NeuralCodingAssistant/       # Core system components
└── 📁 LLM_Mesh/                    # Model management and endpoints
```

## 🧠 AdministrativeMesh/

**Council-based task routing and execution management**

```
AdministrativeMesh/
├── 📄 __init__.py                  # Package initialization
├── 📄 admin_dispatcher.py          # Main task dispatcher
├── 📄 council_router.py            # Administrative model selection
├── 📄 task_parser.py               # Request classification
├── 📄 attention_router.py          # Context memory routing
├── 📄 memory_expander.py           # Memory context expansion
├── 📄 function_courier_parser.py   # Function signature verification
├── 📄 mesh_manager.py              # Async worker coordination
├── 📄 task_lifecycle.py            # Execution logging
├── 📄 vote_system.py               # Council voting mechanism
├── 📄 planner_agent.py             # Multi-step task planning
└── 📄 plan_registry.json           # Task planning registry
```

## 🤖 NeuralCodingAssistant/

**Core system with specialized workers and memory**

```
NeuralCodingAssistant/
├── 📄 Function_Courier.md          # Zero-copy function signatures
├── 📄 scaffold.py                  # System bootstrapping
├── 📁 Functions/                   # Function documentation
│   ├── 📄 Debugger.md
│   ├── 📄 Analyzer.md  
│   ├── 📄 Fixer.md
│   ├── 📄 Cleaner.md
│   └── 📄 Gitter.md
├── 📁 workers/                     # Specialized AI workers
│   ├── 📄 debugger_worker.py       # Code debugging
│   ├── 📄 analyzer_worker.py       # Code analysis
│   ├── 📄 fixer_worker.py          # Code fixing
│   ├── 📄 fixer_helper.py          # Patch merging
│   └── 📄 Cleaner.py               # Code cleanup
├── 📁 orchestrator/                # System orchestration
│   └── 📄 admin_dispatcher.py      # Orchestrator interface
└── 📁 AgentMemory/                 # Persistent context and learning
    ├── 📄 Roadmap.json             # Project roadmap
    ├── 📄 Components.json          # UI components
    ├── 📄 ContextMap.json          # Context routing
    └── 📁 Architecture/            # System architecture
        ├── 📄 Architecture.json     # System design
        ├── 📄 Diagram.json         # Signal flow
        └── 📄 BuildTips.json       # Implementation tips
```

## 🔗 LLM_Mesh/

**Model management and API endpoints**

```
LLM_Mesh/
├── 📄 mesh_manager.py              # Model router
├── 📄 MODEL_INFO.md               # Model documentation
├── 📁 models/                      # AI model storage
│   ├── 📁 administrative/          # Council models
│   │   ├── 🤖 deepseek-llm-67b-chat.Q2_K.gguf
│   │   ├── 🤖 llama-2-70b-chat.ggmlv3.q2_K.bin
│   │   └── 🤖 qwen1.5-72b-chat-q2_k.gguf
│   └── 📁 worker/                  # Specialized worker models
│       ├── 🤖 codellama-7b-instruct.Q4_K_M.gguf
│       ├── 🤖 deepseek-coder-6.7b-instruct.Q4_K_S.gguf
│       ├── 🤖 mistral-7b-instruct-v0.2.Q4_K_M.gguf
│       ├── 🤖 starcoder2-15b-Q4_K_M.gguf
│       ├── 🤖 wizardcoder-python-13b-v1.0.Q4_K_S.gguf
│       └── 🤖 wizardcoder-python-34b-v1.0.Q3_K_S.gguf
└── 📁 endpoints/                   # FastAPI endpoints
    ├── 📄 debugger_endpoint.py     # Debug endpoint
    ├── 📄 analyzer_endpoint.py     # Analysis endpoint
    ├── 📄 fixer_endpoint.py        # Code fixing endpoint
    └── 📄 cleaner_endpoint.py      # Cleanup endpoint
```

## ⚙️ .vscode/

**VS Code configuration and integration**

```
.vscode/
├── 📄 tasks.json                   # Build and run tasks
├── 📄 launch.json                  # Debug configurations
└── 📄 continue_config.json         # Continue extension config
```

## 🏗️ Key Architecture Components

### 1. **Administrative Mesh**
- **Purpose**: Council-based task routing and execution management
- **Components**: Dispatcher, Router, Parser, Memory, Lifecycle
- **Models**: Large administrative models for decision making

### 2. **Function Courier**
- **Purpose**: Zero-hallucination function signature enforcement
- **Implementation**: Markdown-based function definitions
- **Verification**: Regex parsing and signature validation

### 3. **Workers**
- **Purpose**: Specialized AI models for specific coding tasks
- **Types**: Debug, Analyze, Fix, Clean, Patch Helper
- **Models**: GGUF quantized models optimized for code tasks

### 4. **LLM Mesh**
- **Purpose**: Model management and inference coordination
- **Features**: Async execution, model caching, fallback handling
- **Support**: GGUF/GGML models via llama-cpp-python

### 5. **Agent Memory**
- **Purpose**: Persistent context and learning storage
- **Components**: Architecture docs, roadmap, context maps
- **Format**: JSON-based structured data

## 🚀 Quick Navigation

- **🔧 Setup**: Start with `quick-setup.sh`
- **📚 Documentation**: Read `README.md`
- **🤝 Contributing**: See `CONTRIBUTING.md`
- **🐛 Issues**: Check error logs in `task_log.json`
- **⚡ API**: Main server in `rest_api.py`
- **🧠 Models**: Configuration in `LLM_Mesh/MODEL_INFO.md`

## 📊 File Size Guidelines

- **Small** (< 1MB): Configuration, code, documentation
- **Medium** (1-100MB): Model configs, test data
- **Large** (> 100MB): GGUF models (excluded from git)
- **Excluded**: Virtual environments, logs, temporary files
