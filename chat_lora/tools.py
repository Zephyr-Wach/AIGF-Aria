# chat_lora/tools.py
from abc import ABC, abstractmethod
import os

class AriaTool(ABC):
    def __init__(self, name, description, usage=""):
        self.name = name
        self.description = description
        self.usage = usage

    @abstractmethod
    def execute(self, args: str, context: dict) -> str:
        pass

class HelpTool(AriaTool):
    def __init__(self, registry):
        super().__init__('/help', "List commands")
        self.registry = registry
    def execute(self, args, context):
        return "\n".join([f"{k}: {v.description}" for k, v in self.registry.items()])

class ClearTool(AriaTool):
    def __init__(self): super().__init__('/clear', "Reset memory")
    def execute(self, args, context):
        if os.path.exists(context.get('memory_file', '')):
            os.remove(context['memory_file'])
        return "Memory wiped."

class StatsTool(AriaTool):
    def __init__(self): super().__init__('/stats', "Session stats")
    def execute(self, args, context): return f"Context turns: {len(context.get('messages', []))}"

class NativeFunctionTool(AriaTool):
    def __init__(self, name, description, usage, func_impl):
        super().__init__(name, description, usage)
        self.func = func_impl
    def execute(self, args, context):
        try:
            if not args and self.func.__code__.co_argcount == 0: return str(self.func())
            if self.name == '/remind': # 特殊处理
                parts = args.rsplit(' ', 1)
                # 兼容处理：如果最后一部分是数字，则分离；否则全部当内容
                if len(parts) > 1 and parts[1].replace('.','',1).isdigit():
                    return str(self.func(parts[0], float(parts[1])))
                return str(self.func(args))
            return str(self.func(args))
        except Exception as e: return f"Error: {e}"