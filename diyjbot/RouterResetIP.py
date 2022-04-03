#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import sys

from telethon import events

from .. import chat_id, jdbot, logger, ch_name, BOT_SET
from ..bot.utils import cmd, TASK_CMD
import asyncio

@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/routerip$'))
async def RouterResetIP(event):
    try:
        cmdtext="task /ql/scripts/Routerinfo.js now"        
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
            
        cmdtext="task /ql/scripts/AutoRun/RouterResetIP.js now"        
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
            await asyncio.sleep(60)
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

