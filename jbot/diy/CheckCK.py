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

@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/cck'))
async def CheckCK(event):
    try:        
        await event.edit('开始检查账号情况，请稍后...')
        
        cmdtext="task /ql/repo/ccwav_QLScript2/bot_jd_CkSeq.js now"        
        p = await asyncio.create_subprocess_shell(
            cmdtext, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        res_bytes, res_err = await p.communicate()
        res = res_bytes.decode('utf-8') 
        txt=res.split('\n')
        strReturn=""
        intcount=0
        if res:
            await event.delete()
            for line in txt: 
                if "分割行" in line:
                    intcount=0
                    if strReturn:                        
                        await jdbot.send_message(chat_id, strReturn)
                    strReturn=""
                else:        
                    if "】" in line or "没有出现" in line or "今日正常" in line  :
                        strReturn=strReturn+line+'\n'
                        intcount=intcount+1
                    if intcount==70:
                        intcount=0
                        if strReturn:                        
                            await jdbot.send_message(chat_id, strReturn)
                        strReturn=""
        else:
            await jdbot.send_message(chat_id, "查询失败!")
            
        if strReturn:
            await jdbot.send_message(chat_id, strReturn)
        
    except Exception as e:
        title = "【💥错误💥】"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + sys._getframe().f_code.co_name
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n\n{tip}")
        logger.error(f"错误--->{str(e)}")


if ch_name:
    jdbot.add_event_handler(CheckCK, events.NewMessage(from_users=chat_id, pattern=BOT_SET['命令别名']['cron']))

