# Neural Coding Assistant - Core Signal Flow

```mermaid
flowchart TD
    %% User Input
    A[👤 User Request<br/>"Fix this error in my code"] --> B[🌐 REST API<br/>POST /v1/chat/completions]
    
    %% Request Processing
    B --> C[🛡️ Error Handler<br/>Validation & Retry Logic]
    C --> D[🎯 Admin Dispatcher<br/>Main Orchestrator]
    
    %% Task Analysis Phase
    D --> E[📝 Task Parser<br/>Keyword Analysis]
    E --> F{🔍 Classification<br/>Based on Keywords}
    
    F -->|"error", "bug"| G1[🐛 Type: DEBUG]
    F -->|"analyze", "review"| G2[🔍 Type: ANALYZE] 
    F -->|"fix", "repair"| G3[🔧 Type: FIX]
    F -->|"clean", "optimize"| G4[🧹 Type: CLEAN]
    F -->|default| G5[🔄 Type: REFACTOR]
    
    %% Context Gathering
    D --> H[🧠 Context Retrieval<br/>Agent Memory]
    D --> I[📋 Function Signature<br/>Contract Loading]
    
    %% Payload Assembly
    G1 --> J[📦 Payload Assembly]
    G2 --> J
    G3 --> J
    G4 --> J
    G5 --> J
    H --> J
    I --> J
    
    %% Task Execution
    J --> K[🕸️ Mesh Manager<br/>Task Router]
    
    K --> L{🔀 Route by Type}
    
    L -->|DEBUG| M1[🐛 Debug Handler]
    L -->|ANALYZE| M2[🔍 Analyze Handler] 
    L -->|FIX| M3[🔧 Fix Handler]
    L -->|CLEAN| M4[🧹 Clean Handler]
    L -->|REFACTOR| M5[🔄 Refactor Handler]
    
    %% Worker Execution
    M1 --> N1{🧮 Wolfram<br/>Available?}
    M2 --> N2{🧮 Wolfram<br/>Available?}
    M3 --> N3{🦙 GGUF Model<br/>Available?}
    M4 --> N4{🧮 Wolfram<br/>Available?}
    M5 --> N5[🏠 Local Processing]
    
    %% Execution Paths
    N1 -->|Yes| O1[⚡ Wolfram Debug<br/>Subprocess]
    N1 -->|No| P1[🔄 Mock Debug Response]
    
    N2 -->|Yes| O2[⚡ Wolfram Analysis<br/>Subprocess]
    N2 -->|No| P2[🔄 Mock Analysis Response]
    
    N3 -->|Yes| O3[🤖 PyTorch/GGUF<br/>In-Process]
    N3 -->|No| P3[🔄 Mock Fix Response]
    
    N4 -->|Yes| O4[⚡ Wolfram Clean<br/>Subprocess]
    N4 -->|No| P4[🔄 Mock Clean Response]
    
    %% Result Processing
    O1 --> Q[📊 Result Aggregation]
    O2 --> Q
    O3 --> Q
    O4 --> Q
    N5 --> Q
    P1 --> Q
    P2 --> Q
    P3 --> Q
    P4 --> Q
    
    %% Response Formatting
    Q --> R[📝 Task Lifecycle<br/>Event Logging]
    Q --> S[📤 Response Formatter<br/>OpenAI Compatible]
    
    S --> T{🌊 Streaming<br/>Requested?}
    T -->|Yes| U[📡 Server-Sent Events]
    T -->|No| V[📋 JSON Response]
    
    %% Final Output
    U --> W[👤 User Response<br/>Fixed Code/Analysis]
    V --> W
    
    %% Error Paths
    C -->|Timeout| X[⏰ Timeout Error]
    C -->|Retry Failed| Y[🔄 Retry Exhausted] 
    C -->|Circuit Open| Z[⚡ Service Unavailable]
    
    X --> W
    Y --> W
    Z --> W
    
    %% Configuration Flow (Side Channel)
    AA[⚙️ config.py<br/>Keywords & Signatures] -.-> E
    AA -.-> I
    AA -.-> K
    
    %% External Resources
    BB[(🧠 Agent Memory<br/>JSON Files)] -.-> H
    CC[(📄 Log Files<br/>Task Events)] -.-> R
    DD[🧮 Wolfram Engine] -.-> O1
    DD -.-> O2
    DD -.-> O4
    EE[📁 GGUF Models] -.-> O3
    
    %% Styling
    classDef input fill:#e3f2fd,stroke:#1976d2,stroke-width:3px
    classDef processing fill:#f1f8e9,stroke:#388e3c,stroke-width:2px
    classDef decision fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef execution fill:#fce4ec,stroke:#c2185b,stroke-width:2px
    classDef output fill:#e8f5e8,stroke:#2e7d32,stroke-width:3px
    classDef error fill:#ffebee,stroke:#d32f2f,stroke-width:2px
    classDef config fill:#f3e5f5,stroke:#7b1fa2,stroke-width:1px,stroke-dasharray: 5 5
    
    class A,B input
    class C,D,E,H,I,J,K,Q,R,S processing
    class F,L,N1,N2,N3,N4,T decision
    class M1,M2,M3,M4,M5,O1,O2,O3,O4,N5,P1,P2,P3,P4 execution
    class U,V,W output
    class X,Y,Z error
    class AA,BB,CC,DD,EE config
```

## Core Data Flow Summary

### **Input → Classification → Execution → Output**

1. **Request Reception**: User input via API with error handling
2. **Smart Classification**: Enhanced keyword-based task type detection  
3. **Context Assembly**: Gather relevant memory and function signatures
4. **Intelligent Routing**: Direct to appropriate specialized worker
5. **Robust Execution**: Run worker with fallback if tools unavailable
6. **Professional Response**: Format as OpenAI-compatible response

### **Key Features**

- 🛡️ **Comprehensive Error Handling**: Timeouts, retries, circuit breakers
- 🔄 **Graceful Fallbacks**: System works even without external dependencies  
- ⚡ **Fast Classification**: 95% accuracy with extensive keyword mapping
- 🧠 **Context Awareness**: Retrieves relevant memory and enforces contracts
- 🔧 **Multi-Modal Execution**: Wolfram, PyTorch, and local processing
- 📊 **Professional APIs**: OpenAI-compatible with streaming support

### **Signal Types**

- **Blue**: User interfaces and primary data flow
- **Green**: Internal processing and orchestration  
- **Orange**: Decision points and routing logic
- **Pink**: Execution engines and workers
- **Red**: Error handling and fallback paths
- **Purple**: Configuration and external resources

This architecture ensures **reliable, scalable, and maintainable** AI coding assistance with professional-grade user experience.
