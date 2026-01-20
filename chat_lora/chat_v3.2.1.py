import torch
import json
import os
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

MODEL_PATH = "models/Qwen2.5-3B-Instruct"
LORA_PATH = "lora_aigf_v3.2"
MEMORY_FILE = "aria_memory.json"
DEVICE = "mps"

class AriaChat:
    def __init__(self):
        print(f"✨ 正在唤醒 Aria (V3.2)...")
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
        base_model = AutoModelForCausalLM.from_pretrained(
            MODEL_PATH, torch_dtype=torch.bfloat16
        ).to(DEVICE)
        self.model = PeftModel.from_pretrained(base_model, LORA_PATH)
        self.model.eval()

        self.memory = self.load_memory()
        self.history = self.init_system_prompt()

    def load_memory(self):
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"user_name": "你", "key_events": []}

    def init_system_prompt(self):

        memory_str = f"你的名字叫 Aria。你是用户的亲密伴侣。用户叫{self.memory['user_name']}。"
        if self.memory['key_events']:
            events = "，".join(self.memory['key_events'][-3:]) # 只取最近3条重要记忆
            memory_str += f"你还记得：{events}。"
            
        return [
            {"role": "system", "content": f"{memory_str} 你性格温柔随性，喜欢用表情包。我们现在在家里。说话简短，严禁提及学校、打车等琐事。"}
        ]

    def chat(self):
        print(f"\n--- Aria 已上线 (当前记忆: {self.memory['user_name']}) ---")
        while True:
            user_input = input("\n我：")
            if user_input.lower() in ["exit", "quit"]: break
            
            if "叫我" in user_input:
                new_name = user_input.split("叫我")[-1].strip(" ，。")
                self.memory['user_name'] = new_name
                print(f"💡 Aria 记住了，以后叫你 {new_name}")
                continue

            self.history.append({"role": "user", "content": user_input})
            
            prompt = self.tokenizer.apply_chat_template(self.history, tokenize=False, add_generation_prompt=True)
            inputs = self.tokenizer(prompt, return_tensors="pt").to(DEVICE)

            with torch.no_grad():
                output_ids = self.model.generate(
                    **inputs, max_new_tokens=64, do_sample=True,
                    temperature=0.6, top_p=0.8, repetition_penalty=1.2
                )

            response = self.tokenizer.decode(output_ids[0][len(inputs["input_ids"][0]):], skip_special_tokens=True)
            print(f"Aria：{response}")
            self.history.append({"role": "assistant", "content": response})
            
            if len(self.history) > 11:
                self.history = [self.history[0]] + self.history[-10:]

    def save_and_exit(self):
        with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.memory, f, ensure_ascii=False)
        print("🌙 Aria 去休息了，记忆已保存。")

if __name__ == "__main__":
    aria = AriaChat()
    try:
        aria.chat()
    finally:
        aria.save_and_exit()
