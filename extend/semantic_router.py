# extend/semantic_router.py
import os
# 禁止进度条刷屏
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"

from fastembed import TextEmbedding
from typing import Dict
import numpy as np

class SemanticRouter:
    def __init__(self, tools_manifest: Dict):
        # 1. 锁定本地缓存目录，避免重复下载/哈希校验
        cache_path = os.path.join(os.getcwd(), "models", "embedding_cache")
        os.makedirs(cache_path, exist_ok=True)

        print(f"🧠 [Router] Loading model (Cache: {cache_path})...")
        
        # 2. 使用中文优化模型 BAAI/bge-small-zh-v1.5
        self.embedding_model = TextEmbedding(
            model_name="BAAI/bge-small-zh-v1.5", 
            cache_dir=cache_path
        ) 
        
        self.tools = []
        self.descriptions = []
        self.metas = []
        
        for func_name, meta in tools_manifest.items():
            self.tools.append(func_name)
            self.metas.append(meta)
            # 组合关键词
            desc_text = f"{meta['desc']}. {' '.join(meta.get('keywords', []))}"
            self.descriptions.append(desc_text)
            
        print(f"🧠 [Router] Indexing {len(self.tools)} skills...")
        self.tool_embeddings = list(self.embedding_model.embed(self.descriptions))

    def scan(self, query: str, threshold: float = 0.45):
        if not query.strip(): return None, 0

        query_embedding = list(self.embedding_model.embed([query]))[0]
        
        scores = []
        for tool_emb in self.tool_embeddings:
            score = np.dot(query_embedding, tool_emb)
            scores.append(score)
            
        max_score = max(scores)
        best_idx = scores.index(max_score)
        
        best_cmd = self.metas[best_idx]['cmd']
        # 调试日志：显示匹配详情
        print(f"   🔍 [Debug] Query: '{query}' | Match: '{best_cmd}' | Score: {max_score:.4f}")

        if max_score >= threshold:
            return self.metas[best_idx], max_score
        
        return None, max_score