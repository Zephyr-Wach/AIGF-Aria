# extend/loader.py
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    import assist_mba
    from info import TOOLS_MANIFEST
except ImportError as e:
    print(f"⚠️ [Loader] Failed to import extensions: {e}")
    TOOLS_MANIFEST = {}

from chat_lora.tools import NativeFunctionTool

def load_extensions():
    extension_tools = {}
    print("🔌 [Loader] Injecting capabilities...")
    
    for func_name, meta in TOOLS_MANIFEST.items():
        if hasattr(assist_mba, func_name):
            func_impl = getattr(assist_mba, func_name)
            cmd = meta['cmd']
            tool = NativeFunctionTool(
                name=cmd,
                description=meta['desc'],
                usage=meta.get('usage', ''),
                func_impl=func_impl
            )
            extension_tools[cmd] = tool
    return extension_tools