import subprocess
import os
import re
import datetime

def get_now():
    """获取当前系统时间，格式：YYYY-MM-DD HH:MM:SS"""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def run_shortcut(name, input_data):
    """
    通用快捷指令执行器。
    """
    try:
        res = subprocess.run(
            ["shortcuts", "run", name, "-i", str(input_data)], 
            capture_output=True, 
            text=True, 
            check=True
        )
        return res.returncode == 0
    except Exception:
        return False

def set_alarm(time_str):
    """
    设定响铃闹钟 (通过 Shortcuts: AriaAlarm)。
    """
    t_match = re.search(r'(\d{1,2}:\d{2})', str(time_str))
    if t_match:
        clean_time = t_match.group(1)
        if run_shortcut("AriaAlarm", clean_time):
            return f"SUCCESS: Alarm set for {clean_time}"
    return "FAILED: 无效的时间格式或快捷指令未响应"

def set_focus(state_arg):
    """
    切换专注模式 (通过 Shortcuts: AriaFocus)。
    """
    s = str(state_arg).lower()
    off_signals = ["off", "关", "退", "完", "下班", "休", "结束", "done", "stop", "finish"]
    action = "off" if any(sig in s for sig in off_signals) else "on"
    
    if run_shortcut("AriaFocus", action):
        return f"SUCCESS: Focus Mode now {action.upper()}"
    return f"FAILED: Unable to set focus mode to {action}"

def set_reminder(content, delay_minutes=0):
    """
    添加提醒事项 (通过 AppleScript 驱动 Reminders.app)。
    """
    try:
        nums = re.findall(r'\d+', str(delay_minutes))
        delay = int(nums[0]) if nums else 0
        clean_content = str(content).replace('>>>', '').replace('/remind', '').strip()
        if ':' in clean_content:
            clean_content = clean_content.split(':')[-1].strip()
        
        if not clean_content or clean_content == "None":
            clean_content = "Aria 定时提醒"

        target_dt = datetime.datetime.now() + datetime.timedelta(minutes=delay)
        script = f'''
        set delaySeconds to {delay} * 60
        set targetDate to (current date) + delaySeconds
        tell application "Reminders"
            make new reminder with properties {{name:"{clean_content}", remind me date:targetDate, body:"Aria v4.3 自动设定"}}
        end tell
        '''
        
        subprocess.run(["osascript", "-e", script], capture_output=True, check=True)
        return f"SUCCESS: Remind '{clean_content}' scheduled at {target_dt.strftime('%H:%M')}"
    except Exception as e:
        return f"ERROR: Reminder set failed - {str(e)}"


def get_sys_status():
    """
    获取 macOS 实时硬件状态。
    """
    try:
        bat_res = subprocess.check_output(["pmset", "-g", "batt"], text=True)
        match = re.search(r'(\d+)%', bat_res)
        battery = match.group(1) if match else "Unknown"
        cpu_cmd = "top -l 1 | grep -E '^CPU' | awk '{print $3}'"
        cpu = subprocess.check_output(cpu_cmd, shell=True, text=True).strip().replace('%', '')
        mem_cmd = "vm_stat | grep 'free' | awk '{print $3}' | sed 's/\\.//'"
        pages_free = int(subprocess.check_output(mem_cmd, shell=True, text=True).strip())
        mem_free = round((pages_free * 4096) / (1024**3), 1)
        
        return f"Battery: {battery}%, CPU: {cpu}%, FreeMem: {mem_free}GB"
    except Exception as e:
        return f"Status Error: {str(e)}"