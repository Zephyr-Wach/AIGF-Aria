# Aria v4.2 Architecture: Boomerang ReAct Execution System

## 1. Core Definition

**v4.2** marks the transition from a "Chatbot" to a "System Agent." By implementing the **ReAct (Reasoning and Acting)** paradigm, Aria has gained the capability to understand intent and drive macOS hardware via structured tool calls.

## 2. Technical Pillars

### A. Semantic Router

- **Mechanism**: Uses high-performance regex clusters or embedding similarity to dispatch user intent in real-time.
- **Threshold Control**: Tool manifests are only activated when the intent confidence score $Score \ge 0.6$.
- **Objective**: To protect the LLM's reasoning integrity by preventing command interference during normal conversation.

### B. JIT (Just-In-Time) Injection

- **Strategy**: **On-demand Loading**.
- **Implementation**: Keeps the System Prompt clean by only injecting specific `Tool Manifests` when the router triggers a specific intent (e.g., "Alarm").
- **Objective**: To conserve unified memory on the M4 chip and reduce inference latency in long-context scenarios.

### C. Boomerang Execution Flow

1. **Output**: LLM generates a task-specific JSON or command block.
2. **Intercept**: The Python script intercepts the output (hiding it from the user) and executes the call via `shortcuts` or `osascript`.
3. **Observation**: The system returns the execution result (Success/Error Code).
4. **Loopback**: The observation is fed back into the LLM, which then generates the final natural language response.

------

## 3. Hardware Adaptation (MacBook Air M4)

- **Privilege Routing**:
  - **Reflex**: Directly fetches system status (CPU, Time) via Python `subprocess`.
  - **Skill**: Executes write operations (Alarms, Reminders) via **macOS Shortcuts** to bypass the strict low-level permission barriers of the M4 chip.