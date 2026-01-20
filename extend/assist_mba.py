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

        remind_time = (datetime.datetime.now() + datetime.timedelta(minutes=delay)).strftime("%Y-%m-%d %H:%M:%S")
        
        script = f'tell application "Reminders" to make new reminder with properties {{name:"{content}", body:"Aria", remind me date:date "{remind_time}"}}'
        
        # 🔥 修改点：capture_output=True, text=True
        subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
        return f"✅ Remind set: {content} at {remind_time}"
    except Exception as e: return f"Error: {e}"

def set_alarm(time_str):
    try:
        clean_time = re.sub(r'[^\d:]', '', str(time_str))
        now = datetime.datetime.now()
        target = datetime.datetime.strptime(clean_time, "%H:%M").replace(year=now.year, month=now.month, day=now.day)
        
        if target < now: target += datetime.timedelta(days=1)
        fmt = target.strftime("%Y-%m-%d %H:%M:%S")
        
        script = f'tell application "Reminders" to make new reminder with properties {{name:"⏰ Alarm: {clean_time}", remind me date:date "{fmt}", priority:1}}'
        
        # 🔥 修改点：capture_output=True, text=True
        subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
        
        return f"⏰ Alarm set for {fmt}"
    except Exception as e: 
        return f"Usage: HH:MM (Error: {e})"

def complete_task(keyword):
    clean_kw = keyword.replace('"', '').replace("'", "").strip()
    script = f'tell application "Reminders" to set completed of (reminders whose name contains "{clean_kw}") to true'
    subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    return f"✅ Marked '{clean_kw}' as done."