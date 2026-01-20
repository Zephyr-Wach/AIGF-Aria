import subprocess
import os
import re
import datetime

# --- 基础反射技能 ---

def get_now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def set_reminder(content, delay_minutes=0):
    try:
        if isinstance(content, str):
            content = content.replace('"', '').replace("'", "").strip()
        try:
            delay = float(str(delay_minutes).strip())
        except:
            delay = 0

        t = datetime.datetime.now() + datetime.timedelta(minutes=delay)
        # 属性构造法保证 100% 兼容性
        script = f'''
        tell application "Reminders"
            set targetDate to current date
            set day of targetDate to {t.day}
            set month of targetDate to {t.month}
            set year of targetDate to {t.year}
            set hours of targetDate to {t.hour}
            set minutes of targetDate to {t.minute}
            set seconds of targetDate to {t.second}
            make new reminder with properties {{name:"{content}", body:"Aria 提醒", remind me date:targetDate}}
        end tell
        '''
        subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
        return f"✅ 已设定提醒: {content} (于 {t.strftime('%Y-%m-%d %H:%M:%S')})"
    except Exception as e: return f"Error: {e}"
    

# --- 🚀 核心：快捷指令通用调用器 ---
def run_shortcut(name, input_data):
    try:
        # 强制静默运行并捕获输出
        res = subprocess.run(["shortcuts", "run", name, "-i", str(input_data)], capture_output=True, text=True)
        return res.returncode == 0
    except:
        return False

# --- 🛠️ 战术技能实现 ---

def set_alarm(time_str):
    """设置响铃闹钟 (通过 Shortcuts: AriaAlarm)"""
    clean_time = re.sub(r'[^\d:]', '', str(time_str))
    if run_shortcut("AriaAlarm", clean_time):
        return f"⏰ 系统闹钟已设定在 {clean_time}"
    return "❌ 闹钟设定失败，请检查快捷指令 AriaAlarm"

def set_focus(state):
    """切换专注模式 (通过 Shortcuts: AriaFocus)"""
    # 识别：开/on -> on, 关/off -> off
    action = "on" if any(x in str(state).lower() for x in ["on", "开", "入", "专注"]) else "off"
    if run_shortcut("AriaFocus", action):
        return f"🌙 专注模式已{'开启' if action == 'on' else '关闭'}"
    return "❌ 专注模式切换失败"

