# type: "reflex" -> 脊髓反射，系统直接执行并把结果喂给 LLM (如查时间、查状态)
# type: "skill"  -> 大脑技能，把说明书给 LLM，让 LLM 决定怎么用 (如定闹钟、发提醒)

TOOLS_MANIFEST = {
    "get_now": {
        "cmd": "/time",
        "desc": "查询当前的精确时刻与日期",
        "keywords": ["几点", "时间", "日期", "现在时刻", "clock"],
        "type": "reflex" 
    },
    "get_sys_status": {
        "cmd": "/status",
        "desc": "查看 MacBook 硬件运行状态(CPU/内存/电量)",
        "keywords": ["卡不卡", "cpu", "内存", "电量", "负载", "status"],
        "type": "reflex"
    },
    "set_alarm": {
        "cmd": "/alarm",
        "desc": "设定具体的响铃闹钟(通常用于起床或固定时刻)",
        "usage": "HH:MM",
        "keywords": ["闹钟", "叫醒", "起床", "设定闹钟"],
        "type": "skill"
    },
    "set_reminder": {
        "cmd": "/remind",
        "desc": "创建一个未来的定时通知(Notification)或倒计时，仅用于稍后叫我做事",
        "usage": "内容 分钟数",
        "keywords": ["提醒我", "定时", "通知", "叫我", "分钟后"],
        "type": "skill"
    },
    "set_focus": {
        "cmd": "/focus",
        "desc": "切换系统的专注/勿扰模式。进入沉浸状态用 on，结束当前状态并恢复普通模式用 off。",
        "usage": "on(开启)/off(关闭)",
        "keywords": ["专注", "工作", "学习", "做完", "结束", "状态"],
        "type": "skill"
    },
}