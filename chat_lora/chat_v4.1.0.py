import os
import json
import sys
import mlx.core as mx
from mlx_lm import load, stream_generate

MODEL_PATH = "models/Qwen2.5-7B-4bit"
ADAPTER_PATH = "lora_aigf_v4/aria_qwen3_7b_lora"
MEMORY_FILE = "aria_memory.json"

def sanitize_adapter():
    config_path = os.path.join(ADAPTER_PATH, "adapter_config.json")
    target_weight = os.path.join(ADAPTER_PATH, "adapters.safetensors")
    source_weight = os.path.join(ADAPTER_PATH, "adapter_model.safetensors")
    if not os.path.exists(target_weight) and os.path.exists(source_weight):
        os.rename(source_weight, target_weight)
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            cfg = json.load(f)
        cfg["num_layers"] = 28 
        if "model_type" in cfg: del cfg["model_type"]
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(cfg, f, indent=2)

def load_mem():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"user_name": "Zephyr"}

def start_chat():
    sanitize_adapter()
    print(f"🧬 正在唤醒 Aria ...")

    try:
        model, tokenizer = load(MODEL_PATH, adapter_path=ADAPTER_PATH)
    except Exception as e:
        print(f"❌ 加载失败: {e}")
        sys.exit(1)

    memory = load_mem()
    history = []
    
    system_prompt = (
        f"你是 Aria。你现在正和男友 {memory['user_name']} 待在一起。"
        "【性格】：随性、有点调皮、绝对理性但不死板。你喜欢用简单直接的方式表达。"
        "【禁令】：绝对禁止说‘有什么可以帮您’、‘作为AI’、‘了解’、‘收到’。绝对禁止分点陈述。"
        "【风格】：像发微信一样说话。每次回复控制在 30 字以内，多用语气词和 emoji ✨。你现在的状态是边忙自己的事边回他。"
    )
    
    print("-" * 50)

    while True:
        try:
            user_input = input(f"\n{memory['user_name']}: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
            
        if not user_input: continue
        if user_input.lower() in ['exit', 'quit']: break

        history.append({"role": "user", "content": user_input})
        messages = [{"role": "system", "content": system_prompt}] + history[-6:]
        
        prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

        print(f"Aria: ", end="", flush=True)
        full_response = ""
        
        try:
            for chunk in stream_generate(model, tokenizer, prompt, max_tokens=200):
                content = chunk.text if hasattr(chunk, 'text') else str(chunk)
                if "<think>" in content: continue
                print(content, end="", flush=True)
                full_response += content
        except Exception as e:
            print(f"\n⚠️ 生成遇到点小意外: {e}")
        
        print("\n" + "-" * 50)
        history.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    start_chat()