# 🦾 Aria: J.A.R.V.I.S. Protocol

<div align="center">

[![System Status](https://img.shields.io/badge/System-ONLINE-success?style=flat-square)](https://github.com/Zephyr-Wach/AIGF-Aria)
[![Architecture](https://img.shields.io/badge/Architecture-Hybrid_(Local_%2B_Cloud)-blueviolet?style=flat-square)](https://github.com/ml-explore/mlx)
[![Class](https://img.shields.io/badge/Class-Cognitive_Daemon-orange?style=flat-square)](LICENSE)

**Just A Rather Intelligent Agent.**
*Your general-purpose cognitive operating system.*

[English](README_EN.md) | [简体中文](../README.md)

</div>

---

## 📡 Project Status 

**Currently, Aria exists primarily as a "Personality Patch" (LoRA).** She is a finely-tuned weight adapter designed to transform the generic Qwen model into an intellectual partner with **critical thinking, geek aesthetics, and logical resonance**. The long-term goal of this repository (`AIGF-Aria`) is to build a J.A.R.V.I.S.-like local agent framework around this personality core. **At present, the LoRA weights are stable (The Soul), while the Agent toolchain (The Body) is under active development.** 

> "The soul is online. Constructing the shell."

---

## 🗺️ Development Roadmap

### Phase 1: Soul Injection (The Foundation)
*Establishing the persona and base loops.*

- [x] **Milestone 1.1: Environment & Base Loop**
    - [x] Task: Setup environment and dependencies.
    - [x] Task: Implement basic loop based on local models.
    - [x] Task: Define basic System Prompt structure.

### Phase 2: Sensory Extension (The Tools)
*Connecting Aria to the local filesystem and workflow, and memory.*

- [x] **Milestone 2.1: Command Router**
    - [x] Task: Refactor Main Loop to support `/command` parsing.
    - [x] Task: Create abstract `Tool` interface class.
- [ ] **Milestone 2.2: Memory Persistence**
    - [ ] Task: Implement `save_history()` and `load_history()` (JSON/DB).
    - [ ] Task: Implement Context Window management (Last-N turns).
    - [ ] **Challenge:** Ensure continuity of consciousness across system restarts.

### Phase 3: Cyber Symbiosis (Autonomy)
*Granting Aria agency, and vision.*

- [ ] **Milestone 3.1: Active Triggers**
    - [ ] Task: Implement Idle Detection (Trigger after 30m inactivity).
    - [ ] Task: Implement Time-based Greetings (Morning/Night).
- [ ] **Milestone 3.2: Visual Cortex**
    - [ ] Task: Integrate Vision Model (e.g., Qwen-VL).
    - [ ] Task: Create `/look` command to analyze screen content.

---

## 📈 Changelog

| Version  | Core Dilemma                                                 | Solution & Improvement                                       | Status       |
| :------- | :----------------------------------------------------------- | :----------------------------------------------------------- | :----------- |
| **v1.0** | Repeater effect; illogical dialogue.                         | Established JSONL structured data processing pipeline.       | ❌ Deprecated |
| **v2.0** | **Narrative Hallucinations**: Frequent mentions of car crashes/exams. | Introduced `device_map` adaptation; attempted initial data cleaning. | ⚠️ Suspended  |
| **v3.1** | **Overfitting**: 5 Epochs caused loss of logic.              | Reduced training intensity; reconsidered Rank weights.       | ⚠️ Suspended  |
| **v3.2** | **Lucid State**: Balance point between nuance and logic.     | **Physical Blacklist Filtering + Ultra-low Rank (8)**.       | **Stable**   |
| **v4.1** | Upgrade from 3B to 7B based on v3.2.                         | Quantized 7B model for MacBook Air optimization.             | **Stable**   |
| **v4.2** | Intent recognition & tool execution                          | [Semantic Router + JIT Dynamic Injection + ReAct Architecture](../docs/Aria_v4.2_Architecture_EN.md) | ✅            |
| **v4.3** | Long-term memory processing                                  | [Three-Tier Tiered Storage Architecture](../docs/Aria_v4.3_Memory_System_EN.md) | ✅            |

---

## 📥 Model Weights

Aria's LoRA weights are hosted on Hugging Face. These weights are trained on **Qwen2.5-3B-Instruct**, specifically optimized for daily conversational nuance and emotional expression.

| Model Version          | Base Model                                                   | LoRA Adapter                                                 |
| :--------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| **Aria-v3.2 (Stable)** | [Qwen2.5-3B-Instruct](https://huggingface.co/Qwen/Qwen2.5-3B-Instruct) | [zephyr-zw666/AIGF-Aria-v3.2-LoRA](https://huggingface.co/zephyr-zw666/AIGF-Aria-v3.2-LoRA) |
| **Aria-v4.0 (Stable)** | [zephyr-zw666/Qwen2.5-7B-4bit](https://huggingface.co/zephyr-zw666/Qwen2.5-7B-4bit) | [zephyr-zw666/AIGF-Aria-v4.0-LoRA](https://huggingface.co/zephyr-zw666/AIGF-Aria-v4.0-LoRA) |

---

## 🛠️ Replication Protocol

If you wish to train your own instance of Aria, refer to the directory structure and workflow below.

### 1. Directory Structure

```text
TrainAIGF/
├── README.md                  # Project Documentation
├── environment.yml            # Conda Environment Config
├── AIGF-Aria-LoRA/            # Saved LoRA Weights
│   ├── AIGF-Aria-v3.2-LoRA
│   └── AIGF-Aria-v4.0-LoRA
├── DataSet/                   # Raw Dataset & Build Scripts
│   ├── WeChatMsg_example.txt  # [Example] Format reference
│   └── build_dataset_V3.2.py  # Data cleaning script
├── chat_lora/                 # Inference/Chat Scripts
│   ├── chat_v3.2.1.py
│   └── chat_v4.1.0.py
├── data/                      # Formatted Training Data (.jsonl)
│   └── train_v3.2_example.jsonl
├── models/                    # Base Models
│   ├── Qwen2.5-3B-Instruct
│   └── Qwen2.5-7B-4bit
└── train_lora/                # Training/Fine-tuning Scripts
    ├── train_v3.2.py
    ├── train_v4.0_14b.py
    └── train_v4.0_7b.py
```

### 2. Protocol Steps (Step-by-Step)

1. **Data Acquisition:**

   - Download chat history between you and the target persona. Refer to `DataSet/WeChatMsg_example.txt` for the required format.

2. **Data Processing:**

   - Run `DataSet/build_dataset_V3.2.py`.
   - **⚠️ CRITICAL WARNING:** The script includes a blacklist mechanism. You **MUST** modify this to filter out high-frequency special terms or private information. Failure to do so will cause the LoRA to "overfit" (memorize) specific logs, reducing generalization.

3. **Base Model Preparation:**

   - **3B Model:** Recommended for training on MacBook Air (M-Series). Download `Qwen2.5-3B-Instruct`.

   - **7B/8B Model Warning:**

     > A MacBook Air (16GB RAM) **cannot** train 7B/8B models locally due to VRAM limitations (OOM). I trained these on a cloud computing platform and pulled the weights locally. To run 7B/8B base models locally for inference, they must be **4-bit quantized** first.

   - **14B Model Warning:** Not recommended. Qwen2.5-14B's logic often enters infinite "Thinking" loops, making it unsuitable for casual chat interaction.

4. **Environment Configuration:**

   - Modify the file paths in the scripts under the `train_lora` directory to match your local environment.

5. **Initialization:**

   - Use the trained LoRA weights combined with the base model and run the `chat_lora` script to awaken Aria.