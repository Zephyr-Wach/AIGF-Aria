# Aria v4.3 核心架构说明：ReAct 回旋镖指令系统

## 1. 核心定义

**v4.2** 实现了从“聊天机器人”向“系统代理 (Agent)”的跨越。通过 **ReAct (Reasoning and Acting)** 范式，赋予了 Aria 理解意图并驱动 macOS 系统硬件的能力。

## 2. 技术支柱

### A. 语义路由 (Semantic Router)

- **逻辑**：利用高性能正则簇或向量相似度对用户输入进行实时意图分发。
- **阈值控制**：仅当意图置信度 $Score \ge 0.6$ 时才激活对应的工具说明书。
- **目的**：防止指令系统干扰正常的对话逻辑。

### B. JIT (Just-In-Time) 动态注入

- **策略**：**按需加载 (On-demand Loading)**。
- **实现**：平时保持 System Prompt 纯净，只有在路由触发特定意图（如“闹钟”）时，才将该工具的 `Manifest` 注入 Context。
- **目的**：节省 M4 芯片的统一内存，降低长文本推理延迟。

### C. 回旋镖 (Boomerang) 执行流

1. **生成 (Output)**：LLM 按照指定格式输出 JSON/指令块。
2. **拦截 (Intercept)**：Python 脚本实时截获输出，不展示给用户，直接调用 `shortcuts` 或 `osascript`。
3. **观察 (Observation)**：系统返回执行结果（Success/Error）。
4. **回流 (Loopback)**：将结果喂回 LLM，由其生成最终的自然语言答复。

------

## 3. 硬件适配策略 (MacBook Air M4)

- **权限路由**：
  - **Reflex (反射类)**：直接通过 Python `subprocess` 获取系统状态（CPU、时间）。
  - **Skill (技能类)**：通过 **macOS Shortcuts (快捷指令)** 绕过 M4 严苛的底层权限限制，执行修改闹钟、提醒等写操作。