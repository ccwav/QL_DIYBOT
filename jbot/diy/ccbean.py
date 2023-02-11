#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import sys
import re
from telethon import events, Button

from .. import chat_id, jdbot, logger, ch_name, BOT_SET
from ..bot.utils import cmd, TASK_CMD,split_list, press_event
from .utils import read, write
import asyncio
import json

@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/ccbean'))
async def CCBeanInfo(event):
    try:
        msg_text = event.raw_text.split(' ')
        
        msg = await jdbot.send_message(chat_id, '正在查询，请稍后')
        if isinstance(msg_text, list) and len(msg_text) == 2:
            text = msg_text[-1]
        else:
            text = None  
            
        if text==None:
            SENDER = event.sender_id
            btn = []
            for i in range(11):
                btn.append(Button.inline(str(i+1), data=str(i+1)))
            btn.append(Button.inline('取消', data='cancel'))
            btn = split_list(btn, 3)            
            async with jdbot.conversation(SENDER, timeout=90) as conv:
                info='请选择要查询的账号:'
                msg = await jdbot.edit_message(msg, info, buttons=btn, link_preview=False)
                convdata = await conv.wait_event(press_event(SENDER))
                res = bytes.decode(convdata.data)
                if res == 'cancel':
                    msg = await jdbot.edit_message(msg, '对话已取消')
                    conv.cancel()
                else:
                    text = res
                    msg = await jdbot.edit_message(msg, '开始查询账号'+text+'的资产，请稍后...')
                    
        if text==None:
            await jdbot.delete_messages(chat_id, msg)
            return 
        
        #载入设定
        scriptpath=""
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
            
                
        await jdbot.delete_messages(chat_id, msg)
        msg = await jdbot.send_message(chat_id, '开始查询账号'+text+'的资产，请稍后...')
        
        cmdtext="task "+scriptpath+" now"      
        p = await asyncio.create_subprocess_shell(
            cmdtext, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        res_bytes, res_err = await p.communicate()
        res = res_bytes.decode('utf-8') 
        txt=res.split('\n')
        strReturn=""
        if res:
            for line in txt:                
                if "】" in line or "明细" in line:
                    strReturn=strReturn+line+'\n'
                    
        if strReturn:
            await jdbot.delete_messages(chat_id, msg)
            await jdbot.send_message(chat_id, strReturn)
        else:
            await jdbot.delete_messages(chat_id, msg)
            await jdbot.send_message(chat_id,'查询失败!')
        
    except Exception as e:
        title = "【💥错误💥】"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + sys._getframe().f_code.co_name
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n\n{tip}")
        logger.error(f"错误--->{str(e)}")


if ch_name:
    jdbot.add_event_handler(CCBeanInfo, events.NewMessage(from_users=chat_id, pattern=BOT_SET['命令别名']['cron']))

