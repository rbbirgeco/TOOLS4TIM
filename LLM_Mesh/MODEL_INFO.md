# LLM Model Configuration

## Administrative Models (Council)
Located in `LLM_Mesh/models/administrative/`

### Llama-2 70B Chat (Q2_K)
- **File**: `llama-2-70b-chat.ggmlv3.q2_K.bin`
- **Use Case**: Large context administrative decisions (>16K tokens)
- **Quantization**: Q2_K (2-bit)
- **Specialty**: Long context reasoning, large codebase analysis

### DeepSeek LLM 67B Chat (Q2_K)
- **File**: `deepseek-llm-67b-chat.Q2_K.gguf`
- **Use Case**: Deep reasoning, mathematical analysis, chain-of-thought
- **Quantization**: Q2_K (2-bit)
- **Specialty**: Complex problem solving, architectural decisions

### Qwen 1.5 72B Chat (Q2_K)
- **File**: `qwen1.5-72b-chat-q2_k.gguf`
- **Use Case**: Tool usage, debugging coordination, step-by-step tasks
- **Quantization**: Q2_K (2-bit)
- **Specialty**: Multi-step workflows, debugging orchestration

## Worker Models
Located in `LLM_Mesh/models/worker/`

### StarCoder2 15B (Q4_K_M)
- **File**: `starcoder2-15b-Q4_K_M.gguf`
- **Task**: Debug code analysis
- **Quantization**: Q4_K_M (4-bit medium)
- **Specialty**: Multi-language debugging, error analysis

### DeepSeek Coder 6.7B Instruct (Q4_K_S)
- **File**: `deepseek-coder-6.7b-instruct.Q4_K_S.gguf`
- **Task**: Deep code analysis
- **Quantization**: Q4_K_S (4-bit small)
- **Specialty**: Code understanding, architecture analysis

### CodeLlama 7B Instruct (Q4_K_M)
- **File**: `codellama-7b-instruct.Q4_K_M.gguf`
- **Task**: Code fixing and generation
- **Quantization**: Q4_K_M (4-bit medium)
- **Specialty**: Code completion, bug fixing, Python/C++

### WizardCoder Python 13B (Q4_K_S)
- **File**: `wizardcoder-python-13b-v1.0.Q4_K_S.gguf`
- **Task**: Python-specific assistance, patch merging
- **Quantization**: Q4_K_S (4-bit small)
- **Specialty**: Python code, patch application

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
