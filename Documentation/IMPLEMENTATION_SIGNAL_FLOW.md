# Neural Coding Assistant - Implementation Signal Flow

```mermaid
graph TB
    %% User Layer
    User[👤 User Request] --> RestAPI[rest_api.py<br/>🌐 FastAPI Application]
    
    %% API Processing
    RestAPI --> ErrorHandling[error_handling.py<br/>🛡️ with_timeout_and_retry<br/>RetryConfig<br/>CircuitBreaker]
    
    ErrorHandling --> AdminDispatcher[AdministrativeMesh/<br/>admin_dispatcher.py<br/>🎯 dispatch(prompt)]
    
    %% Administrative Processing
    AdminDispatcher --> TaskParser[AdministrativeMesh/<br/>task_parser.py<br/>📝 parse_task(prompt)]
    
    TaskParser --> ConfigSystem[config.py<br/>⚙️ classify_task_by_keywords<br/>TASK_KEYWORDS<br/>FUNCTION_SIGNATURES]
    
    AdminDispatcher --> CouncilRouter[AdministrativeMesh/<br/>council_router.py<br/>🏛️ select_admin(task)]
    
    AdminDispatcher --> AttentionRouter[AdministrativeMesh/<br/>attention_router.py<br/>🎯 get_context_slice(task)]
    
    AttentionRouter --> AgentMemory[(NeuralCodingAssistant/<br/>AgentMemory/<br/>🧠 ContextMap.json<br/>WorkspaceStructure.json)]
    
    AdminDispatcher --> MemoryExpander[AdministrativeMesh/<br/>memory_expander.py<br/>📈 expand_memory(context)]
    
    AdminDispatcher --> FunctionCourier[AdministrativeMesh/<br/>function_courier_parser.py<br/>📋 get_function_signature(type)]
    
    FunctionCourier --> ConfigSystem
    FunctionCourier --> CourierDoc[NeuralCodingAssistant/<br/>Function_Courier.md<br/>📄 Markdown Fallback]
    
    %% Payload and Mesh
    AdminDispatcher --> PayloadAssembly[📦 Payload Dict<br/>code_str, error_msg<br/>context, function_sig]
    
    PayloadAssembly --> MeshManager[LLM_Mesh/<br/>mesh_manager.py<br/>🕸️ MeshManager.handle_task()]
    
    %% Task Routing
    MeshManager --> TaskWorkers{🔀 self.task_workers<br/>Dictionary Mapping}
    
    TaskWorkers --> DebugHandler[🐛 _handle_debug_task<br/>mesh_manager.py:65]
    TaskWorkers --> AnalyzeHandler[🔍 _handle_analyze_task<br/>mesh_manager.py:78]
    TaskWorkers --> FixHandler[🔧 _handle_fix_task<br/>mesh_manager.py:91]
    TaskWorkers --> CleanHandler[🧹 _handle_clean_task<br/>mesh_manager.py:103]
    TaskWorkers --> RefactorHandler[🔄 _handle_refactor_task<br/>mesh_manager.py:115]
    
    %% Worker Implementation
    DebugHandler --> WolframWorker[🧮 _run_wolfram_worker<br/>mesh_manager.py:127<br/>asyncio.create_subprocess_exec]
    AnalyzeHandler --> WolframWorker
    CleanHandler --> WolframWorker
    
    FixHandler --> PytorchCheck{🤖 PyTorch Model<br/>Available?}
    PytorchCheck -->|Yes| LlamaModel[🦙 llama-cpp-python<br/>GGUF Model Loading]
    PytorchCheck -->|No| FallbackFix[🔄 Fallback Response<br/>mesh_manager.py:98]
    
    WolframWorker --> WolframCheck{🧮 Wolfram Engine<br/>subprocess available?}
    WolframCheck -->|Yes| WolframExec[⚡ Wolfram Script<br/>Execution]
    WolframCheck -->|No| WolframFallback[🔄 Exception Handler<br/>mesh_manager.py:73]
    
    RefactorHandler --> LocalLogic[🏠 Local Processing<br/>String manipulation]
    
    %% Results and Logging
    WolframExec --> TaskLifecycle[AdministrativeMesh/<br/>task_lifecycle.py<br/>📝 log_task_event()]
    FallbackFix --> TaskLifecycle
    WolframFallback --> TaskLifecycle
    LocalLogic --> TaskLifecycle
    LlamaModel --> TaskLifecycle
    
    TaskLifecycle --> LogFiles[(📄 task_events.json<br/>Event Logging)]
    
    %% Response Processing
    WolframExec --> ResponseFormatter[📤 OpenAI Compatible<br/>Response Structure]
    FallbackFix --> ResponseFormatter
    WolframFallback --> ResponseFormatter
    LocalLogic --> ResponseFormatter
    LlamaModel --> ResponseFormatter
    
    ResponseFormatter --> StreamingCheck{🌊 payload.stream<br/>== True?}
    StreamingCheck -->|Yes| EventStream[📡 event_stream()<br/>rest_api.py:31<br/>Server-Sent Events]
    StreamingCheck -->|No| JSONResponse[📋 JSON Response<br/>rest_api.py:34<br/>OpenAI Format]
    
    %% Output
    EventStream --> UserResponse[👤 Response to User]
    JSONResponse --> UserResponse
    
    %% Error Paths
    ErrorHandling -->|Timeout| TimeoutResponse[⏰ asyncio.TimeoutError<br/>error_handling.py:45]
    ErrorHandling -->|Retries Failed| RetryFailure[🔄 TaskExecutionError<br/>error_handling.py:58]
    ErrorHandling -->|Circuit Open| CircuitOpen[⚡ Circuit Breaker<br/>error_handling.py:109]
    
    TimeoutResponse --> UserResponse
    RetryFailure --> UserResponse
    CircuitOpen --> UserResponse
    
    %% Optional Microservice Endpoints
    MeshManager -.->|HTTP Mode| DebugEndpoint[LLM_Mesh/endpoints/<br/>debugger_endpoint.py<br/>🌐 :8001/debug]
    MeshManager -.->|HTTP Mode| AnalyzeEndpoint[LLM_Mesh/endpoints/<br/>analyzer_endpoint.py<br/>🌐 :8002/analyze]
    MeshManager -.->|HTTP Mode| FixEndpoint[LLM_Mesh/endpoints/<br/>fixer_endpoint.py<br/>🌐 :8003/fix]
    MeshManager -.->|HTTP Mode| CleanEndpoint[LLM_Mesh/endpoints/<br/>cleaner_endpoint.py<br/>🌐 :8004/clean]
    
    %% External Systems
    WolframExec -.-> WolframEngine[🧮 External Process<br/>wolfram -c "script"]
    LlamaModel -.-> ModelFiles[📁 LLM_Mesh/models/<br/>*.gguf files]
    AgentMemory -.-> FileSystem[💾 File System<br/>JSON Storage]
    
    %% Testing and Validation
    TestSuite[test_comprehensive.py<br/>🧪 Test Framework] -.-> TaskParser
    TestSuite -.-> MeshManager
    TestSuite -.-> ConfigSystem
    TestSuite -.-> ErrorHandling
    
    %% Package Structure
    SetupPy[setup.py<br/>📦 Package Installer] -.-> PackageInit[__init__.py<br/>🏗️ Package Exports]
    
    %% Styling
    classDef apiLayer fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef adminMesh fill:#e8f5e8,stroke:#2e7d32,stroke-width:2px
    classDef llmMesh fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef workers fill:#fce4ec,stroke:#c2185b,stroke-width:2px
    classDef config fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef external fill:#fafafa,stroke:#424242,stroke-width:2px
    classDef testing fill:#e0f2f1,stroke:#00695c,stroke-width:2px
    classDef error fill:#ffebee,stroke:#d32f2f,stroke-width:2px
    
    class RestAPI,ErrorHandling apiLayer
    class AdminDispatcher,TaskParser,CouncilRouter,AttentionRouter,MemoryExpander,FunctionCourier,TaskLifecycle adminMesh
    class MeshManager,TaskWorkers,ResponseFormatter llmMesh
    class DebugHandler,AnalyzeHandler,FixHandler,CleanHandler,RefactorHandler,WolframWorker workers
    class ConfigSystem,PackageInit,SetupPy config
    class WolframEngine,ModelFiles,FileSystem,AgentMemory,LogFiles,CourierDoc external
    class TestSuite testing
    class TimeoutResponse,RetryFailure,CircuitOpen,ErrorHandling error
```

## Implementation Details

### **File Structure Mapping**

| Component | File Location | Key Functions |
|-----------|---------------|---------------|
| **API Layer** | `rest_api.py` | `route_chat()`, `event_stream()` |
| **Error Handling** | `error_handling.py` | `with_timeout_and_retry()`, `CircuitBreaker` |
| **Task Dispatch** | `AdministrativeMesh/admin_dispatcher.py` | `dispatch()`, `get_mesh_manager()` |
| **Classification** | `AdministrativeMesh/task_parser.py` | `parse_task()` |
| **Configuration** | `config.py` | `TASK_KEYWORDS`, `FUNCTION_SIGNATURES` |
| **Mesh Routing** | `LLM_Mesh/mesh_manager.py` | `handle_task()`, `_handle_*_task()` |
| **Signatures** | `AdministrativeMesh/function_courier_parser.py` | `get_function_signature()` |
| **Testing** | `test_comprehensive.py` | Test classes and validation |

### **Key Implementation Features**

- 🔧 **Modular Design**: Each file has single responsibility
- 🛡️ **Error Resilience**: Comprehensive error handling at every layer
- ⚙️ **Configuration Driven**: Centralized settings in `config.py`
- 🧪 **Test Coverage**: Automated validation of all components
- 📦 **Package Ready**: Professional Python package structure
- 🔄 **Fallback Logic**: Graceful degradation when dependencies unavailable

### **Signal Flow Characteristics**

- **Async Throughout**: All I/O operations are non-blocking
- **Type Safety**: Pydantic models for API validation
- **Logging**: Comprehensive event tracking for debugging
- **Extensible**: Easy to add new task types and workers
- **Deployable**: Supports both monolith and microservice modes

This implementation provides a **production-ready foundation** for AI-powered coding assistance with clear upgrade paths and professional reliability.
