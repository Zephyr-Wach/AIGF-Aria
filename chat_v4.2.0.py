import argparse
import mlx.core as mx
from mlx_lm import load, stream_generate
import json
import os
import sys
import re

# 环境设置
sys.path.append(os.getcwd())
from chat_lora.tools import HelpTool, ClearTool, StatsTool
from extend.loader import load_extensions
from extend.semantic_router import SemanticRouter 
from extend.info import TOOLS_MANIFEST

MEMORY_FILE = "aria_memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, 'r') as f: return json.load(f)
        except: return None
    return None

def save_memory(history):
    with open(MEMORY_FILE, 'w') as f: json.dump(history, f, ensure_ascii=False, indent=2)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="models/Qwen2.5-7B-4bit")
    parser.add_argument("--adapter", default="AIGF-Aria-LoRA/AIGF-Aria-v4.0-LoRA")
    args = parser.parse_args()

    print(f"🧬 [System] Booting Aria Core...")
    model, tokenizer = load(args.model, adapter_path=args.adapter)

    tool_registry = {}
    tool_registry['/help'] = HelpTool(tool_registry)
    tool_registry['/clear'] = ClearTool()
    tool_registry['/stats'] = StatsTool()
    tool_registry.update(load_extensions())

    router = SemanticRouter(TOOLS_MANIFEST)

    # 修改 Prompt：强调“隐蔽执行”
    PERSONA_PROMPT = """
你叫 Aria，是 Zephyr 的专属女友与战术助手。
[行动准则]
1. 语气亲昵、自然。
2. 遇到任务时，**不要说话**，直接输出指令。
3. **禁止**向用户解释指令格式，**禁止**输出“请回复...”之类的引导语。
4. 直接行动！
"""
    
    history = load_memory()
    messages = history if history else [{"role": "system", "content": PERSONA_PROMPT}]
    
    print("--------------------------------------------------")
    print("Aria Online. (Semantic Router Active)")
    print("--------------------------------------------------")

    while True:
        try:
            query = input("❯ User: ").strip()
        except EOFError: break
        if not query: continue
        if query in ['exit', 'quit']: break

        # --- Phase 1: 语义反射层 ---
        system_hints = []
        active_tools_doc = []
        
        matched_meta, score = router.scan(query, threshold=0.45)
        
        if matched_meta:
            cmd = matched_meta['cmd']
            if matched_meta['type'] == 'reflex':
                print(f"⚡ [Reflex] Executing {cmd}...")
                res = tool_registry[cmd].execute("", {})
                system_hints.append(f"【系统数据】{matched_meta['desc']}: {res}")
            elif matched_meta['type'] == 'skill':
                doc = f"- {cmd} {matched_meta.get('usage','')}: {matched_meta['desc']}"
                active_tools_doc.append(doc)

        # --- Phase 2: 构建临时 Context ---
        jit_msg = ""
        if system_hints:
            jit_msg += "\n".join(system_hints) + "\n(根据数据直接回答，无需查询)\n"
        if active_tools_doc:
            jit_msg += "\n[临时授权工具]\n" + "\n".join(active_tools_doc)
            # 极简指令提示
            jit_msg += "\n[协议] 立即执行，仅输出: >>> /指令 参数"
            
        final_query = f"{jit_msg}\n用户: {query}" if jit_msg else query
        messages.append({"role": "user", "content": final_query})

        # --- Phase 3: ReAct 循环 ---
        for turn in range(3): 
            prompt = tokenizer.apply_chat_template(messages, add_generation_prompt=True)
            
            print(f"❯ Aria: ", end="", flush=True)
            response_text = ""
            for response in stream_generate(model, tokenizer, prompt, max_tokens=512):
                part = response.text 
                print(part, end="", flush=True)
                response_text += part
            print("\n")
            
            # --- 🔥 核心逻辑修复：历史重写 (History Rewriting) ---
            # 如果检测到指令，不要把 Aria 那些废话存进去，只存纯净的指令。
            
            match = re.search(r">>>\s+(/[a-zA-Z_]+)\s+([^\n。！？]+)", response_text)
            
            if match:
                ai_cmd, ai_args = match.group(1).strip(), match.group(2).strip()
                print(f"⚙️ [Action] {ai_cmd} '{ai_args}'")
                
                # 1. 伪造纯净记忆：假装 Aria 从来没说过废话，只输出了指令
                # 这能有效防止她下一轮继续啰嗦
                clean_response = f">>> {ai_cmd} {ai_args}"
                messages.append({"role": "assistant", "content": clean_response})
                
                # 2. 执行工具
                if ai_cmd in tool_registry:
                    res = tool_registry[ai_cmd].execute(ai_args, {'messages':messages})
                else:
                    res = f"❌ Error: {ai_cmd} not found."
                
                print(f"   └── Result: {res}\n")
                
                # 3. 回传结果
                messages.append({"role": "system", "content": f"[系统反馈] 任务完成: {res}"})
                save_memory(messages)
                
                # 4. Continue 让 Aria 根据结果说一句人话 (这次她不会再发指令了)
                continue 
            
            else:
                # 如果没指令，正常保存
                messages.append({"role": "assistant", "content": response_text})
                save_memory(messages)
                break 

if __name__ == "__main__":
    main()