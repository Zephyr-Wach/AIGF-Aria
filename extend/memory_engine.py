import json
import os
from collections import deque
from datetime import datetime

class MemoryEngine:
    def __init__(self, base_path="data/memory", l1_max=20, l1_trigger=15):
        self.base_path = base_path
        if not os.path.exists(base_path):
            os.makedirs(base_path)
            
        self.l1_file = os.path.join(base_path, "l1_active.json")
        self.l2_file = os.path.join(base_path, "l2_facts.json")
        self.l3_file = os.path.join(base_path, "l3_history.log")
        
        self.l1_window = deque(maxlen=l1_max)
        self.l2_data = self._load_json(self.l2_file, {"permanent_core": {"user_name": "男友"}, "temporary_facts": []})
        self._load_l1()

    def _load_json(self, path, default):
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except: pass
        return default

    def _load_l1(self):
        data = self._load_json(self.l1_file, [])
        for msg in data:
            self.l1_window.append(msg)

    def save_all(self):
        """持久化活跃窗口与事实库"""
        with open(self.l1_file, 'w', encoding='utf-8') as f:
            json.dump(list(self.l1_window), f, ensure_ascii=False, indent=2)
        with open(self.l2_file, 'w', encoding='utf-8') as f:
            json.dump(self.l2_data, f, ensure_ascii=False, indent=2)

    def append_l3(self, tag, content):
        """全量日志存档"""
        with open(self.l3_file, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [{tag}] {content}\n")

    def get_jit_facts(self, query):
        """JIT 事实检索：根据关键词从 L2 提取注入 Prompt"""
        facts = []
        core = self.l2_data.get("permanent_core", {})
        for k, v in core.items():
            facts.append(f"{k}: {v}")
            
        temps = self.l2_data.get("temporary_facts", [])
        for f in temps:
            if any(tag in query.lower() for tag in f.get('tags', [])):
                facts.append(f"[Fact]: {f['content']}")
        
        return "\n【长期记忆库】\n" + "\n".join(facts) if facts else ""

    def summarize_and_extract(self, model, tokenizer):
        """15/20 轮滚动压缩算法"""
        if len(self.l1_window) < 20:
            return
            
        print("🧬 [Memory] L1 capacity reached. Rolling compression triggered.")
        to_archive = [self.l1_window.popleft() for _ in range(10)]
        self.append_l3("L1_ROLLING_ARCHIVE", json.dumps(to_archive, ensure_ascii=False))
        
        # 预留摘要逻辑
        self.l1_window.appendleft({"role": "assistant", "content": "【前情提要：已将较早对话归档至 L3 日志库】"})
        self.save_all()