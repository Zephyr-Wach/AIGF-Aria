import json

# 输入输出路径
INPUT_FILE = "data/train_v3.jsonl"
OUTPUT_FILE = "data/train_v3.2.jsonl"

# 剧情黑名单：只要包含这些，直接整条干掉
BLACKLIST = ["学校", "食堂", "老师", "论文", "室友", "宿舍", "打车", "撞车", 
             "跑步", "洗漱", "早饭", "感冒", "口罩", "万象汇", "学长", "考试"]

clean_count = 0
with open(INPUT_FILE, 'r', encoding='utf-8') as f_in, \
     open(OUTPUT_FILE, 'w', encoding='utf-8') as f_out:
    
    for line in f_in:
        item = json.loads(line)
        content = str(item)
        
        # 过滤黑名单
        if any(word in content for word in BLACKLIST):
            continue
            
        # 过滤过长的回复（防止模型讲故事）
        assistant_msg = next((m['content'] for m in item['messages'] if m['role'] == 'assistant'), "")
        if len(assistant_msg) > 45:
            continue
            
        f_out.write(json.dumps(item, ensure_ascii=False) + "\n")
        clean_count += 1

print(f"V3.2 数据集构建完成，剩余数据: {clean_count} 条")
