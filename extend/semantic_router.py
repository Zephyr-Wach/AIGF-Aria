import os
import sys
# 禁止进度条刷屏
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"

from fastembed import TextEmbedding
from typing import Dict
import numpy as np

class SemanticRouter:
    def __init__(self, tools_manifest: Dict):
        # 检测是否开启调试模式
        self.is_debug = "--debug" in sys.argv
        
        cache_path = os.path.join(os.getcwd(), "models", "embedding_cache")
        os.makedirs(cache_path, exist_ok=True)

        if self.is_debug:
            print(f"🧠 [Router] Loading model (Cache: {cache_path})...")
        
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
            desc_text = f"{meta['desc']}. {' '.join(meta.get('keywords', []))}"
            self.descriptions.append(desc_text)
            
        if self.is_debug:
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
        
        if self.is_debug:
            print(f"   🔍 [Debug] Query: '{query}' | Match: '{best_cmd}' | Score: {max_score:.4f}")

        if max_score >= threshold:
            return self.metas[best_idx], max_score
        
        return None, max_score