#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import sys

from telethon import events

from .. import chat_id, jdbot, logger, ch_name, BOT_SET
from ..bot.utils import cmd, TASK_CMD
import asyncio
import time
import json

@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/routerinfo$'))
async def RouterInfo(event):
    try:
        #载入设定
        scriptpath=""
        issetconfig=False
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
                if key=="路由器命令配置":
                    issetconfig=True
        except Exception as e:
            await event.edit(f'载入ccbotSetting.json出错,请检查内容!\n'+str(e))
            return
            
        if not issetconfig:
            await event.edit(f'载入ccbotSetting.json成功，但是缺少相应的配置,请检查!')
            return
            
        try:
            for key in ccbotSetting["路由器命令配置"]:
                if key=="查询信息脚本文件地址":
                    scriptpath=ccbotSetting["路由器命令配置"][key]
                    
        except Exception as e:
            await event.edit(f'载入ccbotSetting.json的cb命令配置内容出错,请检查!\n'+str(e))
            return
        
        if scriptpath=="":
            await event.edit(f'ccbotSetting.json中的cb命令配置没有填写查询信息脚本文件地址,请检查!')
            return
            
        if not os.path.exists(scriptpath):
            await event.edit(f'ccbotSetting.json中的cb命令配置的查询信息脚本文件不存在,请检查!\n'+scriptpath)
            return
    
    
        cmdtext="task "+scriptpath+" now"
        p = await asyncio.create_subprocess_shell(
            cmdtext, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        res_bytes, res_err = await p.communicate()
        res = res_bytes.decode('utf-8') 
        txt=res.split('\n')
        strReturn=""
        if res:
            for line in txt:                
                if "名称" in line or "地址" in line or "内存" in line :
                    strReturn=strReturn+line+'\n'
                    
        if strReturn:
            await jdbot.send_message(chat_id, strReturn)
        else:
            await jdbot.send_message(chat_id,'未能获取路由器信息!')
        
    except Exception as e:
        title = "【💥错误💥】"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + sys._getframe().f_code.co_name
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n\n{tip}")
        logger.error(f"错误--->{str(e)}")


if ch_name:
    jdbot.add_event_handler(RouterInfo, events.NewMessage(from_users=chat_id, pattern=BOT_SET['命令别名']['cron']))

@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/routerip$'))
async def RouterResetIP(event):
    try:
        #载入设定
        scriptpath1=""
        scriptpath2=""
        issetconfig=False
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
                if key=="路由器命令配置":
                    issetconfig=True
        except Exception as e:
            await event.edit(f'载入ccbotSetting.json出错,请检查内容!\n'+str(e))
            return
            
        if not issetconfig:
            await event.edit(f'载入ccbotSetting.json成功，但是缺少相应的配置,请检查!')
            return
            
        try:
            for key in ccbotSetting["路由器命令配置"]:
                if key=="查询信息脚本文件地址":
                    scriptpath1=ccbotSetting["路由器命令配置"][key]
                if key=="重拨路由脚本文件地址":
                    scriptpath2=ccbotSetting["路由器命令配置"][key]
                    
        except Exception as e:
            await event.edit(f'载入ccbotSetting.json的cb命令配置内容出错,请检查!\n'+str(e))
            return
        
        if scriptpath1=="":
            await event.edit(f'ccbotSetting.json中的cb命令配置没有填写查询信息脚本文件地址,请检查!')
            return
            
        if not os.path.exists(scriptpath1):
            await event.edit(f'ccbotSetting.json中的cb命令配置的查询信息脚本文件不存在,请检查!\n'+scriptpath1)
            return
            
        if scriptpath2=="":
            await event.edit(f'ccbotSetting.json中的cb命令配置没有填写重拨路由脚本文件地址,请检查!')
            return
            
        if not os.path.exists(scriptpath2):
            await event.edit(f'ccbotSetting.json中的cb命令配置的重拨路由脚本文件不存在,请检查!\n'+scriptpath1)
            return    
            
        cmdtext="task "+scriptpath1+" now"
        p = await asyncio.create_subprocess_shell(
            cmdtext, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        res_bytes, res_err = await p.communicate()
        res = res_bytes.decode('utf-8') 
        txt=res.split('\n')
        strReturn=""
        if res:
            for line in txt:                
                if "名称" in line or "地址" in line :
                    strReturn=strReturn+line+'\n'
                    
        if strReturn:
            await jdbot.send_message(chat_id, strReturn+"开始通知路由器重新拨号,请断网重连后自行查看IP是否变更,祝您生活愉快....")
            await asyncio.sleep(5)
        else:
            await jdbot.send_message(chat_id,'未能获取路由器信息!')
            return
            
        cmdtext="task "+scriptpath2+" now"
        p = await asyncio.create_subprocess_shell(
            cmdtext, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        res_bytes, res_err = await p.communicate()
        res = res_bytes.decode('utf-8') 
        txt=res.split('\n')
        strReturn=""
        if res:
            for line in txt:                
                if "结果" in line :
                    strReturn=strReturn+line+'\n'                    
        if strReturn:
            await asyncio.sleep(20)
            await jdbot.send_message(chat_id, strReturn)
        else:
            await jdbot.send_message(chat_id,'路由器没有返回信息，重拨失败!')
        
    except Exception as e:
        title = "【💥错误💥】"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + sys._getframe().f_code.co_name
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n\n{tip}")
        logger.error(f"错误--->{str(e)}")


if ch_name:
    jdbot.add_event_handler(RouterResetIP, events.NewMessage(from_users=chat_id, pattern=BOT_SET['命令别名']['cron']))
