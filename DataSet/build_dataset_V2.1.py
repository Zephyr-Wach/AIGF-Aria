import json
from pathlib import Path

SRC = Path("DataSet/WeChatMsg.txt")
OUT_TRAIN = Path("data/train_v3.jsonl")

def build_merged_dataset():
    raw_msgs = []
    # 1. 预处理：按人头合并连续发言
    with SRC.open(encoding="utf-8") as f:
        current_role = None
        current_content = []
        
        for line in f:
            line = line.strip()
            if not line or ":" not in line: continue
            
            role_tag = "user" if line.startswith("我:") else "assistant"
            content = line.split(":", 1)[1].strip()
            
            if role_tag == current_role:
                # 同一个人连续发言，用逗号或空格拼起来
                current_content.append(content)
            else:
                # 换人说话了，保存上一段
                if current_role:
                    raw_msgs.append({"role": current_role, "content": " ".join(current_content)})
                current_role = role_tag
                current_content = [content]
        
        if current_role:
            raw_msgs.append({"role": current_role, "content": " ".join(current_content)})

    # 2. 构造多轮滑动窗口
    processed_data = []
    MAX_CONTEXT_TURNS = 5 
    
    for i in range(len(raw_msgs)):
        if raw_msgs[i]["role"] == "assistant":
            start = max(0, i - MAX_CONTEXT_TURNS)
            context = raw_msgs[start : i + 1]
            
            # 确保对话以 user 开头
            while context and context[0]["role"] != "user":
                context.pop(0)
            
            if len(context) > 1:
                processed_data.append({"messages": context})

    with OUT_TRAIN.open("w", encoding="utf-8") as f:
        for entry in processed_data:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    
    print(f"合并后构建完成：合并后得到 {len(processed_data)} 组连贯对话")

if __name__ == "__main__":
    build_merged_dataset()
