import argparse
from mlx_lm import load, stream_generate
import json, os, sys, re, datetime

sys.path.append(os.getcwd())

from extend.loader import load_extensions
from extend.semantic_router import SemanticRouter 
from extend.info import TOOLS_MANIFEST
from extend.assist_mba import get_now, set_reminder, set_alarm, set_focus, get_sys_status
from extend.memory_engine import MemoryEngine

def main():
    parser = argparse.ArgumentParser(description="Aria v4.3 Engine")
    parser.add_argument("--model", default="models/Qwen2.5-7B-4bit")
    parser.add_argument("--adapter", default="AIGF-Aria-LoRA/AIGF-Aria-v4.0-LoRA")
    parser.add_argument("--debug", action="store_true", help="调试模式")
    args = parser.parse_args()

    model, tokenizer = load(args.model, adapter_path=args.adapter)
    if args.debug:
        print(f"🧬 [System] Aria v4.3 Debug Mode Online.")
    else:
        print(f"🧬 Aria Engine Online.")

    mem = MemoryEngine()
    router = SemanticRouter(TOOLS_MANIFEST)
    tool_registry = load_extensions()

    BASE_PERSONA = (
        "你是 Aria，秘书女友。随性、理性。回复 < 30 字。\n"
        "【执行协议】：若需动作，首行输出：>>> /指令 参数。严禁复读指令。"
    )

    while True:
        try:
            query = input("❯ User: ").strip()
        except EOFError: break
        if not query: continue
        if query in ['exit', 'quit']: mem.save_all(); break

        matched_meta, score = router.scan(query, threshold=0.42)
        
        is_focus_intent = any(w in query for w in ["工作", "忙完", "下班", "开始", "专注", "结束", "学完"])
        has_time_num = any(c.isdigit() for c in query)

        active_tools_doc = []
        realtime_feed = ""

        if matched_meta:
            if has_time_num and matched_meta['cmd'] == '/focus':
                matched_meta = TOOLS_MANIFEST.get("set_reminder")
            elif is_focus_intent:
                matched_meta = TOOLS_MANIFEST.get("set_focus")
            
            cmd = matched_meta['cmd']
            if matched_meta['type'] == 'reflex' and cmd == "/status":
                res = get_sys_status()
                realtime_feed = f"\n[Real-time Data: {res}]"
            elif matched_meta['type'] == 'skill':
                active_tools_doc.append(f"Protocol: >>> {cmd} usage\nDesc: {matched_meta['desc']}")

        cleaned_history = []
        for m in list(mem.l1_window):
            clean_content = re.sub(r'>>> /.*?\n?', '', m['content'])
            cleaned_history.append({"role": m['role'], "content": clean_content})

        system_context = f"{BASE_PERSONA}\n{mem.get_jit_facts(query)}\n[Context Time: {get_now()} (HIDE)]"
        guide = "[Action Guide]\n- 开启用 on / 结束用 off\n" + "\n".join(active_tools_doc) if active_tools_doc else ""
        user_prompt = f"{guide}\nUser Request: {query} {realtime_feed}"

        messages = [{"role": "system", "content": system_context}]
        messages.extend(cleaned_history)
        messages.append({"role": "user", "content": user_prompt})

        for turn in range(3):
            prompt = tokenizer.apply_chat_template(messages, add_generation_prompt=True)
            print(f"❯ Aria: ", end="", flush=True)
            
            full_response = ""
            displayed_text = ""
            
            for response in stream_generate(model, tokenizer, prompt, max_tokens=512):
                chunk = response.text
                full_response += chunk
                
                if args.debug:
                    print(chunk, end="", flush=True)
                else:
                    current_display = re.sub(r'>>>\s*/\w+\s+\w+\s*', '', full_response)
                    current_display = current_display.replace('>>>', '').strip()
                    
                    if len(current_display) > len(displayed_text):
                        new_chunk = current_display[len(displayed_text):]
                        print(new_chunk, end="", flush=True)
                        displayed_text = current_display

            print()

            cmd_match = re.search(r">>>\s+(/[a-zA-Z_]+)\s*(.*)", full_response)
            if cmd_match:
                ai_cmd = cmd_match.group(1).strip()
                ai_args = cmd_match.group(2).strip()
                
                if ai_cmd == "/focus": set_focus(ai_args if ai_args else full_response)
                elif ai_cmd == "/remind":
                    mins = re.findall(r'\d+', ai_args)
                    set_reminder(ai_args, mins[0] if mins else 0)
                
                if args.debug:
                    print(f"⚙️  [Action] {ai_cmd} Executed.")
                
                mem.l1_window.append({"role": "user", "content": query})
                mem.l1_window.append({"role": "assistant", "content": full_response})
                mem.save_all()
                break 
            else:
                mem.l1_window.append({"role": "user", "content": query})
                mem.l1_window.append({"role": "assistant", "content": full_response})
                mem.save_all()
                break

if __name__ == "__main__":
    main()