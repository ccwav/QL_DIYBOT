from telethon import events
from .. import jdbot,chat_id, logger
from ..diy.utils import read, write
import asyncio
import re
import os
import json
try:
    from .login import user
except:
    from .. import user
    
@user.on(events.NewMessage(pattern=r'^setbd', outgoing=True))
async def SetBeanDetailInfo(event):
    try:
        msg_text= event.raw_text.split(' ')
        if len(msg_text) == 2:
            text = msg_text[-1]
        else:
            text = None
            
        if text==None:
            await event.edit('请输入正确的格式: setbd 屏蔽京豆数量')
            return    
            
        key="BOTShowTopNum"
        kv=f'{key}="{text}"'
        change=""
        configs = read("str")    
        if kv not in configs:
            if key in configs:
                configs = re.sub(f'{key}=("|\').*("|\')', kv, configs)                
                write(configs)
            else:
                configs = read("str")
                configs += f'export {key}="{text}"\n'                
                write(configs)
            change = f'已替换屏蔽京豆数为{text}' 
        else:
            change = f'设定没有改变,想好再来.' 
            
        await event.edit(change)
        
    except Exception as e:
        title = "【💥错误💥】"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + e.__traceback__.tb_frame.f_code.co_name
        details = "错误详情：第 " + str(e.__traceback__.tb_lineno) + " 行"
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n{details}\n{traceback.format_exc()}\n{tip}")
        logger.error(f"错误--->{str(e)}")
        
@user.on(events.NewMessage(pattern=r'^bd', outgoing=True))
async def CCBeanDetailInfo(event):
    msg_text= event.raw_text.split(' ')
    if len(msg_text) == 2:
        text = msg_text[-1]
    else:
        text = None  
    
    if text==None:
        await event.edit('请指定要查询的账号,格式: bd 1 或 bd ptpin')
        return 
        
    
    #载入设定
    scriptpath=""
    waitsec=0
    issetconfig=False
    showtopnum=0
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
            if key=="bd命令配置":
                issetconfig=True
    except Exception as e:
        await event.edit(f'载入ccbotSetting.json出错,请检查内容!\n'+str(e))
        return
        
    if not issetconfig:
        await event.edit(f'载入ccbotSetting.json成功，但是缺少相应的配置,请检查!')
        return
        
    try:
        for key in ccbotSetting["bd命令配置"]:
            if key=="脚本文件地址":
                scriptpath=ccbotSetting["bd命令配置"][key]
            if key=="多少秒后自动删除":
                waitsec=int(ccbotSetting["bd命令配置"][key])
            if key=="近期京豆展示的条数":
                showtopnum=int(ccbotSetting["bd命令配置"][key])    
    except Exception as e:
        await event.edit(f'载入ccbotSetting.json的bd命令配置内容出错,请检查!\n'+str(e))
        return
    
    if scriptpath=="":
        await event.edit(f'ccbotSetting.json中的bd命令配置没有填写脚本文件地址,请检查!')
        return
        
    if not os.path.exists(scriptpath):
        await event.edit(f'ccbotSetting.json中的bd命令配置的脚本文件不存在,请检查!\n'+scriptpath)
        return
        
    key="BOTCHECKCODE"
    kv=f'{key}="{text}"'    
    configs = read("str")    
    intcount=0
    if kv not in configs:
        if key in configs:
            configs = re.sub(f'{key}=("|\').*("|\')', kv, configs)            
            write(configs)
        else:
            configs = read("str")
            configs += f'\nexport {key}="{text}"\n'            
            write(configs)
            
    key="BOTShowJinQiNum"
    kv=f'{key}="{showtopnum}"'    
    configs = read("str")    
    intcount=0
    if kv not in configs:
        if key in configs:
            configs = re.sub(f'{key}=("|\').*("|\')', kv, configs)            
            write(configs)
        else:
            configs = read("str")
            configs += f'\nexport {key}="{showtopnum}"\n'            
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
            if "近期豆子" in line:
                result=result+'\n'                
            if "【" in line and "🔔" not in line:
                result=result+line+'\n'            
    else:
        result='查询失败!\n'
        
    if waitsec==0:
        await event.edit(result)
    else:
        result=result+"\n【本条信息将在"+str(waitsec)+"秒钟后自动删除】"
        await event.edit(result)        
        await asyncio.sleep(waitsec)
        await event.delete()
    