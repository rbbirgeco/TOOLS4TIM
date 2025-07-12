# 🌐 Free-S_Code Distributed Models

## Models Are Now Network-Hosted! 

Free-S_Code has migrated to a **distributed model hosting architecture**. Models are no longer stored locally - they're hosted across a network of community nodes.

## 🚀 Available Models

### Code Generation & Analysis
- **StarCoder-15B**: Advanced code generation and analysis
  - Specialties: Python, JavaScript, Rust, code optimization
  - Context: 8,192 tokens
  - Cost: $0.002 per 1K tokens

- **DeepSeek Coder-33B**: Large model for complex code analysis  
  - Specialties: Code analysis, refactoring, architecture
  - Context: 16,384 tokens
  - Cost: $0.003 per 1K tokens

### Python & Debugging
- **Code Llama-7B**: Python-specialized with massive context
  - Specialties: Python, debugging, documentation
  - Context: 100,000 tokens
  - Cost: $0.001 per 1K tokens

### General Reasoning  
- **Mistral-7B**: Fast reasoning and general assistance
  - Specialties: Reasoning, analysis, planning
  - Context: 32,768 tokens
  - Cost: $0.0008 per 1K tokens

## 💡 How to Use

No downloads required! Just request models through the API:

```python
from LLM_Mesh.distributed_models import get_model_response

# Automatic model selection and routing
result = await get_model_response(
    model_name="code-llama-7b",
    prompt="def fibonacci(n):",
    task_type="python"
)
```

## 🌐 Network Benefits

- **No Local Storage**: Save 68GB+ of disk space
- **Always Updated**: Models are kept current by node operators
- **High Availability**: Multiple nodes host each model
- **Better Performance**: Access to GPU-accelerated nodes
- **Fair Pricing**: Pay only for actual compute used

## 🤝 Join the Network

Become a model hosting node operator:

```bash
./setup-node-operator.sh
```

Earn NetworkTokens by providing AI compute to the community!

## 📊 Network Status

Check real-time model availability:

```python
from LLM_Mesh.distributed_models import model_registry

# Get all available models
models = model_registry.get_model_info()
print(f"Available models: {list(models.keys())}")

# Check specific model status
llama_info = model_registry.get_model_info("code-llama-7b")
print(f"Code Llama nodes: {llama_info['available_hosts']}")
```

---

**Note**: The `/models/` directories have been removed as they contained 68GB of model files that are now distributed across the network. This makes the repository much lighter while providing better model access!

For migration details, see: [MIGRATION_TO_DISTRIBUTED.md](../Documentation/MIGRATION_TO_DISTRIBUTED.md)

### WizardCoder Python 34B (Q3_K_S)
- **File**: `wizardcoder-python-34b-v1.0.Q3_K_S.gguf`
- **Task**: Advanced refactoring, complex transformations
- **Quantization**: Q3_K_S (3-bit small)
- **Specialty**: Large-scale refactoring, complex Python projects

### Mistral 7B Instruct v0.2 (Q4_K_M)
- **File**: `mistral-7b-instruct-v0.2.Q4_K_M.gguf`
- **Task**: Code cleanup and optimization
- **Quantization**: Q4_K_M (4-bit medium)
- **Specialty**: Code optimization, dead code removal, efficiency

## Model Loading Strategy

1. **Lazy Loading**: Models are loaded on first use and cached
2. **Memory Management**: Q2_K for large models, Q4_K for workers
3. **Async Inference**: Non-blocking execution via thread pools
4. **Fallback**: Graceful degradation if models fail to load

## Task → Model Routing

| Task Type | Model | Reasoning |
|-----------|-------|-----------|
| `debug` | StarCoder2-15B | Best for multi-language debugging |
| `analyze` | DeepSeek Coder 6.7B | Deep code understanding |
| `fix` | CodeLlama 7B | Proven code generation capabilities |
| `clean` | Mistral 7B | Fast optimization and cleanup |
| `fix_helper` | WizardCoder 13B | Python patch merging |
| `refactor` | WizardCoder 34B | Large-scale transformations |

## Performance Considerations

- **Context Windows**: 4096 tokens default, expandable per model
- **Thread Usage**: 4 CPU threads per model
- **Memory**: Q2_K ~8GB, Q4_K ~4GB, Q3_K ~3GB per model
- **Inference Speed**: Optimized for balance between quality and speed
