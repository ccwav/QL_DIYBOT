from telethon import events
from ..diy.utils import read, write
import asyncio
import re
import os
import json
try:
    from .login import user
except:
    from .. import user
    
@user.on(events.NewMessage(pattern=r'^cb', outgoing=True))
async def CCBeanInfo(event):
    msg_text= event.raw_text.split(' ')
    if isinstance(msg_text, list) and len(msg_text) == 2:
        text = msg_text[-1]
    else:
        text = None  
    
    if text==None:
        await event.edit('请指定要查询的账号,格式: cb 1 或 cb ptpin')
        return  
        
    #载入设定
    scriptpath=""
    waitsec=0
    issetconfig=False
    nocheck=""
    if os.path.exists("/ql/data/config/auth.json"):
        configpath="/ql/data/"
        
    if os.path.exists("/ql/config/auth.json"):
        configpath="/ql/"
        
    if os.path.exists("/jd/config/config.sh"):
        configpath="/jd/"
        
    try:
        f = open(configpath+"config/ccbotSetting.json", "r+", encoding='utf-8')
        ccbotSetting = json.loads(f.read())
        f.close()
        for key in ccbotSetting:
            if key=="cb命令配置":
                issetconfig=True
    except Exception as e:
        await event.edit(f'载入ccbotSetting.json出错,请检查内容!\n'+str(e))
        return
        
    if not issetconfig:
        await event.edit(f'载入ccbotSetting.json成功，但是缺少相应的配置,请检查!')
        return
        
    try:
        for key in ccbotSetting["cb命令配置"]:
            if key=="脚本文件地址":
                scriptpath=ccbotSetting["cb命令配置"][key]
            if key=="多少秒后自动删除":
                waitsec=int(ccbotSetting["cb命令配置"][key])
            if key=="关闭查询项目":
                nocheck=ccbotSetting["cb命令配置"][key]
    except Exception as e:
        await event.edit(f'载入ccbotSetting.json的cb命令配置内容出错,请检查!\n'+str(e))
        return
    
    if scriptpath=="":
        await event.edit(f'ccbotSetting.json中的cb命令配置没有填写脚本文件地址,请检查!')
        return
        
    if not os.path.exists(scriptpath):
        await event.edit(f'ccbotSetting.json中的cb命令配置的脚本文件不存在,请检查!\n'+scriptpath)
        return
        
        
    key="BOTCHECKCODE"
    kv=f'{key}="{text}"'    
    configs = read("str")    
    if kv not in configs:
        if key in configs:
            configs = re.sub(f'{key}=("|\').*("|\')', kv, configs)            
            write(configs)
        else:
            configs = read("str")
            configs += f'\nexport {key}="{text}"\n'            
            write(configs)
            
    key="BEANCHANGE_BOTDISABLELIST"
    kv=f'{key}="{nocheck}"'    
    configs = read("str")    
    if kv not in configs:
        if key in configs:
            configs = re.sub(f'{key}=("|\').*("|\')', kv, configs)           
            write(configs)
        else:
            configs = read("str")
            configs += f'\nexport {key}="{nocheck}"\n'            
            write(configs)
            

    await event.edit('开始查询账号'+text+'的资产，请稍后...')
        
    cmdtext="task "+scriptpath+" now"
    p = await asyncio.create_subprocess_shell(
        cmdtext, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    res_bytes, res_err = await p.communicate()
    res = res_bytes.decode('utf-8') 
    txt=res.split('\n')
    result=""
    if res:
        for line in txt:                
            if "】" in line or "明细" in line:
                result=result+line+'\n'
                    
    if result=="":        
        result='查询失败!'
        
    if waitsec==0:
        await event.edit(result)
    else:
        result=result+"\n【本条信息将在"+str(waitsec)+"秒钟后自动删除】"
        await event.edit(result)        
        await asyncio.sleep(waitsec)
        await event.delete()