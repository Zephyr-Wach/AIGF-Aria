# extend/info.py

# type: "reflex" -> 脊髓反射，系统直接执行并把结果喂给 LLM (如查时间、查状态)
# type: "skill"  -> 大脑技能，把说明书给 LLM，让 LLM 决定怎么用 (如定闹钟、发提醒)

TOOLS_MANIFEST = {
    "get_now": {
        "cmd": "/time",
        "desc": "查询当前时间",
        "keywords": ["几点", "时间", "日期", "time", "date", "clock"],
        "type": "reflex" 
    },
    "get_sys_status": {
        "cmd": "/status",
        "desc": "查看系统状态(CPU/内存/电量)",
        "keywords": ["卡不卡", "cpu", "内存", "电量", "battery", "status"],
        "type": "reflex"
    },
    "set_reminder": {
        "cmd": "/remind",
        "desc": "添加倒计时或延时提醒任务",
        "usage": "/remind 内容 [分钟数]",
        # ⚡️ 重点：增加时间偏移量关键词，接管相对时间意图
        "keywords": ["提醒", "记一下", "remind", "后", "分钟", "小时", "等会", "待会", "min", "hour"],
        "type": "skill"
    },
    "set_alarm": {
        "cmd": "/alarm",
        "desc": "设定具体的绝对时间闹钟",
        "usage": "/alarm HH:MM",
        "keywords": ["闹钟", "叫我", "alarm", "wake", "早起", "睡觉"],
        "type": "skill"
    },
    "complete_task": {
        "cmd": "/done",
        "desc": "标记任务完成",
        "usage": "/done 关键词",
        "keywords": ["做完了", "完成", "搞定", "done", "finish", "已办"],
        "type": "skill"
    }
}