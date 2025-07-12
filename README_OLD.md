# Free-S_Code: Operation Free Source Code

**Motive:** #Eliminate dependency on corporate APIs for AI assisted coding.

🧠 A decentralized AI-powered coding assistant with automated meritocracy and credit loopback system that puts developers first.

## Mission Statement

**Operation: Free-S_Code** is building the world's first CEO-less, corruption-proof AI assistant network where:
- Every user gets a personalized AI that learns their unique workflow
- Developers are automatically rewarded based on actual usage of their contributions
- Computing resources are pooled from the community
- No corporate API dependencies or markup pricing
- Transparent, merit-based reward distribution

## Revolutionary Architecture

```
Free-S_Code Network/
├── Financial Vehicle/          # Credit loopback system
├── Administrative Mesh/        # Council-based task routing
├── Personalized Agents/        # Individual user AI assistants
├── LLM Mesh/                  # Distributed model management
├── Merit Tracking/            # Automated contribution scoring
├── NetworkToken System/       # Earnings & reputation system
└── Decentralized Compute/     # Community-hosted nodes
```

## Core Innovations

- 💰 **Automated Meritocracy**: Developers paid automatically based on usage
- 🏠 **Personal AI Agents**: Each user gets an AI that learns their preferences
- 🔄 **Credit Loopback System**: Subscription fees fund community rewards
- 🌐 **Decentralized Compute**: Users host nodes, reduce network costs
- 📊 **Transparent Economics**: Real-time token costs, no hidden markups
- �️ **Zero Corporate Dependency**: Community-owned and operated
- 🎯 **NetworkTokens**: Earn by contributing, hold for interest rewards

## The Financial Vehicle & Credit Loopback System

### 🏦 Automated Meritocracy Model

**Revenue Sources:**
1. **Monthly Subscription**: $30/month → Developer payouts, Network upkeep, R&D, Pooled HYSA
2. **Pay-Per-Use**: Raw token processing costs with zero markup - transparent real-time pricing

**NetworkToken System:**
- 🚫 **Not Securities**: Cannot be bought, sold, or traded between individuals
- ✅ **Earned by Contributing**: Code contributions, hosting nodes, quality feedback
- 💰 **Interest Rewards**: Hold tokens to earn from pooled High Yield Savings Account
- 📈 **Value Growth**: Token cash-out value increases with network deposits
- ⚖️ **Voting Rights**: Proportional to contributions and weighted by actual usage

### 💡 How It Works

1. **Users Pay Standard Subscription** ($30/mo) + usage-based token processing
2. **Funds Go To Community Pool** → Developer rewards, infrastructure, R&D
3. **Developers Earn NetworkTokens** based on how much their code is actually used
4. **Interest Accrues** in pooled HYSA, distributed to token holders monthly
5. **Home Node Operators** earn credits and reduce network overhead costs
6. **Transparent Banking** - real-time audit of all financial flows available online

## Personal AI Assistant Features

### 🧠 Individualized Learning

Each user gets their own AI that learns:
- **Coding Preferences**: Vanilla Java vs React+Vite, directory layouts, organization patterns
- **Workflow Patterns**: Which agent routing combinations work best for your style
- **Success Metrics**: What changes get celebrated vs reverted to backup
- **Personal Context**: Your project history, coding style, preferred solutions

### 🔒 Privacy & Data

- **Local Data Collection**: Your personal model trains only on your data
- **Optional Global Contribution**: Anonymous data sharing for network improvement
- **Rewards for Sharing**: Earn NetworkTokens for contributing to global knowledge base
- **Your Data, Your Control**: Complete ownership and control of personal training data

## Quick Start

### 1. Install Dependencies

```bash
# Quick setup with testing
./quick-setup.sh

# Or manual installation
pip install -r requirements.txt
```

### 2. Run the Free-S_Code Network Node

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
