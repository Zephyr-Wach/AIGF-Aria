import json
import random
from pathlib import Path

SRC = Path("DataSet/WeChatMsg.txt")
OUT_TRAIN = Path("data/train.jsonl")
OUT_VAL = Path("data/val.jsonl")

OUT_TRAIN.parent.mkdir(exist_ok=True)

pairs = []
last_me = None

with SRC.open(encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue

        if line.startswith("我:"):
            last_me = line[2:].strip()
        elif line.startswith("她:") and last_me:
            her = line[2:].strip()
            pairs.append({
                "messages": [
                    {"role": "user", "content": last_me},
                    {"role": "assistant", "content": her}
                ]
            })
            last_me = None

random.shuffle(pairs)

split = int(len(pairs) * 0.9)
train, val = pairs[:split], pairs[split:]

with OUT_TRAIN.open("w", encoding="utf-8") as f:
    for x in train:
        f.write(json.dumps(x, ensure_ascii=False) + "\n")

with OUT_VAL.open("w", encoding="utf-8") as f:
    for x in val:
        f.write(json.dumps(x, ensure_ascii=False) + "\n")

print(f"train={len(train)}, val={len(val)}")

