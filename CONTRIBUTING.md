# Contributing to Neural Coding Assistant

We welcome contributions to the Neural Coding Assistant! This document provides guidelines for contributing to the project.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/TOOLS4TIM.git
   cd TOOLS4TIM
   ```
3. **Set up the development environment**:
   ```bash
   ./quick-setup.sh
   ```

## Development Setup

### Quick Setup (Recommended)
```bash
./quick-setup.sh
source venv/bin/activate
python rest_api.py
```

### Full Setup with GGUF Models
```bash
./start.sh
# Or manually:
source venv/bin/activate
pip install llama-cpp-python
```

## Project Structure

```
Neural Coding Assistant/
├── AdministrativeMesh/     # Council-based task routing
├── NeuralCodingAssistant/  # Core system components
├── LLM_Mesh/              # Model management
├── rest_api.py            # Main API server
└── requirements.txt       # Dependencies
```

## How to Contribute

### 1. Bug Reports
- Use GitHub Issues to report bugs
- Include system information (OS, Python version)
- Provide steps to reproduce
- Include error messages and logs

### 2. Feature Requests
- Open a GitHub Issue with the "enhancement" label
- Describe the feature and its use case
- Explain how it fits with the existing architecture

### 3. Code Contributions

#### Adding New Workers
1. Create worker file in `NeuralCodingAssistant/workers/`
2. Update `Function_Courier.md` with new function signature
3. Add routing in `AdministrativeMesh/mesh_manager.py`
4. Test with both GGUF and fallback modes

#### Adding New Models
1. Add model info to `LLM_Mesh/MODEL_INFO.md`
2. Update model paths in `AdministrativeMesh/mesh_manager.py`
3. Update task routing in `council_router.py`

#### Improving Administrative Mesh
1. Enhance task parsing in `task_parser.py`
2. Improve context injection in `attention_router.py`
3. Add new admin models in `council_router.py`

## Code Style

- **Python**: Follow PEP 8
- **Comments**: Use docstrings for functions and classes
- **Imports**: Group standard library, third-party, and local imports
- **Error Handling**: Always include graceful fallbacks

## Testing

```bash
# Run system tests
python test_system.py

# Run specific component tests
python -m pytest tests/ -v

# Test API endpoints
curl http://localhost:8080/health
```

## Pull Request Process

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the code style guidelines

3. **Test your changes**:
   ```bash
   ./quick-setup.sh
   python test_system.py
   ```

4. **Commit with descriptive messages**:
   ```bash
   git commit -m "Add: New debugging worker for TypeScript"
   ```

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request** on GitHub

## Architecture Principles

When contributing, keep these principles in mind:

1. **No Hallucination**: Function Courier enforces verified signatures
2. **Stateless Workers**: Clean execution boundaries
3. **Async by Default**: Non-blocking operations
4. **Graceful Fallbacks**: System works even if components fail
5. **Zero-Copy Patterns**: Efficient memory usage

## Areas for Contribution

### High Priority
- [ ] Additional programming language support
- [ ] More specialized worker models
- [ ] Enhanced error handling and recovery
- [ ] Performance optimizations

### Medium Priority
- [ ] Web interface for system monitoring
- [ ] Plugin system for custom workers
- [ ] Distributed deployment support
- [ ] Advanced context management

### Low Priority
- [ ] Alternative model backends
- [ ] Custom prompt templates
- [ ] Metrics and analytics
- [ ] Documentation improvements

## Questions?

- Open an issue on GitHub
- Check existing documentation in `/docs`
- Review the architecture in `NeuralCodingAssistant/AgentMemory/`

Thank you for contributing to the Neural Coding Assistant! 🧠✨
