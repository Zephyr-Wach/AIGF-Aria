# extend/info.py

# type: "reflex" -> 脊髓反射，系统直接执行并把结果喂给 LLM (如查时间、查状态)
# type: "skill"  -> 大脑技能，把说明书给 LLM，让 LLM 决定怎么用 (如定闹钟、发提醒)

TOOLS_MANIFEST = {
    "get_now": {
        "cmd": "/time",
        "desc": "查询当前精确时间",
        "keywords": ["几点", "时间", "日期", "clock"],
        "type": "reflex" 
    },
    "get_sys_status": {
        "cmd": "/status",
        "desc": "查看系统状态(CPU/内存/电量)",
        "keywords": ["卡不卡", "cpu", "内存", "电量", "status"],
        "type": "reflex"
    },
    "set_reminder": {
        "cmd": "/remind",
        "desc": "添加倒计时提醒 (Reminders.app)",
        "usage": "/remind 内容 [分钟数]",
        "keywords": ["提醒", "后", "分钟", "小时"],
        "type": "skill"
    },
    "set_alarm": {
        "cmd": "/alarm",
        "desc": "设定响铃闹钟 (Clock.app)",
        "usage": "/alarm HH:MM",
        "keywords": ["闹钟", "叫我", "起床", "唤醒"],
        "type": "skill"
    }
}