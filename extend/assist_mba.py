import datetime
import subprocess
import psutil
import re

def get_now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_sys_status():
    cpu = psutil.cpu_percent(interval=0.1)
    mem = psutil.virtual_memory().percent
    try:
        bat_res = subprocess.check_output(["pmset", "-g", "batt"]).decode('utf-8')
        match = re.search(r"(\d+)%", bat_res)
        battery = f"{match.group(1)}%" if match else "Unknown"
    except:
        battery = "N/A"
    return f"CPU: {cpu}% | RAM: {mem}% | Battery: {battery}"

def set_reminder(content, delay_minutes=0):
    try:
        if isinstance(content, str):
            content = content.replace('"', '').replace("'", "").strip()
        try:
            delay = float(str(delay_minutes).strip())
        except:
            delay = 0

        t = datetime.datetime.now() + datetime.timedelta(minutes=delay)
        
        # 🍎 终极方案：直接构造 AppleScript 属性，避免字符串解析错误
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
        return f"✅ 已设定: {content} (于 {t.strftime('%Y-%m-%d %H:%M:%S')})"
    except Exception as e: return f"Error: {e}"

def set_alarm(time_str):
    try:
        clean_time = re.sub(r'[^\d:]', '', str(time_str))
        now = datetime.datetime.now()
        target = datetime.datetime.strptime(clean_time, "%H:%M").replace(year=now.year, month=now.month, day=now.day)
        
        if target < now: target += datetime.timedelta(days=1)
        
        # 🍎 同样使用属性构造法
        script = f'''
        tell application "Reminders"
            set targetDate to current date
            set day of targetDate to {target.day}
            set month of targetDate to {target.month}
            set year of targetDate to {target.year}
            set hours of targetDate to {target.hour}
            set minutes of targetDate to {target.minute}
            set seconds of targetDate to 0
            
            make new reminder with properties {{name:"⏰ 闹钟: {clean_time}", remind me date:targetDate, priority:1}}
        end tell
        '''
        
        subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
        return f"⏰ 闹钟设定成功: {target.strftime('%Y-%m-%d %H:%M:%S')}"
    except Exception as e: 
        return f"Usage: HH:MM (Error: {e})"

def complete_task(keyword):
    clean_kw = keyword.replace('"', '').replace("'", "").strip()
    script = f'tell application "Reminders" to set completed of (reminders whose name contains "{clean_kw}") to true'
    subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    return f"✅ Marked '{clean_kw}' as done."