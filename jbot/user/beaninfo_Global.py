from telethon import events, Button
from .login import user

from .. import jdbot
from ..bot.utils import cmd, TASK_CMD,split_list, press_event
from ..diy.utils import read, write
import asyncio
import re
@user.on(events.NewMessage(pattern=r'^bd', outgoing=True))
async def CCBeanDetailInfo(event):
    msg_text= event.raw_text.split(' ')
    if isinstance(msg_text, list) and len(msg_text) == 2:
        text = msg_text[-1]
    else:
        text = None  
    
    if text==None:
        await event.edit('请指定要查询的账号,格式: cb 1 或 cb ptpin')
        return    
        
    key="BOTCHECKCODE"
    kv=f'{key}="{text}"'
    change=""
    configs = read("str")    
    intcount=0
    if kv not in configs:
        if key in configs:
            configs = re.sub(f'{key}=("|\').*("|\')', kv, configs)
            change += f"【替换】环境变量:`{kv}`\n"  
            write(configs)
        else:
            configs = read("str")
            configs += f'export {key}="{text}"\n'
            change += f"【新增】环境变量:`{kv}`\n"  
            write(configs)
                

    await event.edit('开始查询账号'+text+'的资产，请稍后...')
        
    cmdtext="task /ql/repo/ccwav_QLScript2/bot_jd_bean_info.js now"        
    p = await asyncio.create_subprocess_shell(
        cmdtext, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    res_bytes, res_err = await p.communicate()
    res = res_bytes.decode('utf-8') 
    txt=res.split('\n')
    strReturn="" 
    await event.delete()
    if res:
        for line in txt:                
            if "京豆" in line and "🔔" not in line:
                strReturn=strReturn+line+'\n'
            if intcount==35:
                intcount=0
                if strReturn:                    
                    await user.send_message(event.chat_id, strReturn)
                    strReturn="" 
    else:
        await user.send_message(event.chat_id,'查询失败!')
        
    if strReturn:        
        await user.send_message(event.chat_id, strReturn)
    