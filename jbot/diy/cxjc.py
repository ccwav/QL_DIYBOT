    #!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import sys
import asyncio
from telethon import events

from .. import chat_id, jdbot, logger, ch_name, BOT_SET


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/cx$'))
async def cxjc(event):
    try:        
        cmd = "ps -ef"
        f = os.popen(cmd)
        txt = f.readlines() 
        strReturn=""
        intcount=0
        if txt:
            for line in txt:
                if "timeout" in line:
                    continue
                if "/ql/build" in line:
                    continue
                if "/ql/static" in line:
                    continue                  
                if "backend" in line:
                    continue
                if ("node" in line and ".js" in line) or ("python3" in line and ".py" in line):
                    parts = line.split()
                    if len(parts) > 8:
                        pid = parts[1].ljust(15, ' ')
                        cmd_parts = parts[7:]
                        cmd = " ".join(cmd_parts)
                        cmd_split = cmd.split()
                        if len(cmd_split) > 1 and cmd_split[0] == 'node': 
                            pid_name = cmd_split[1].split('/')[-1]
                    else:
                        pid = line.split()[0].ljust(15,' ')
                        pid_name = line.split()[4]
                        
                    if pid_name:    
                        res ="/kill"+pid+'文件名: '+pid_name+'\n'
                        strReturn=strReturn+res
                        intcount=intcount+1
                else:
                    continue
                    

                if intcount==35:
                    intcount=0
                    if strReturn:
                        await jdbot.send_message(chat_id, strReturn)
                    strReturn=""
            if strReturn:
                await jdbot.send_message(chat_id, strReturn)
            else:
                await jdbot.send_message(chat_id,'当前系统未执行任何脚本')
        else:
            await jdbot.delete_messages(chat_id,msg)
            await jdbot.send_message(chat_id,'当前系统未执行任何脚本')
        
    except Exception as e:
        title = "【💥错误💥】"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + sys._getframe().f_code.co_name
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n\n{tip}")
        logger.error(f"错误--->{str(e)}")


if ch_name:
    jdbot.add_event_handler(cxjc, events.NewMessage(from_users=chat_id, pattern=BOT_SET['命令别名']['cron']))

@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'(/kill)'))
async def pidkill(event):
    try:        
        messages = event.raw_text.split("\n")
        for message in messages:
            if "kill" not in message:
                continue                   
            killpid = message.replace("/kill", "")
            
            #先检查是否存在该进程
            cmd = "ps -ef"
            f = os.popen(cmd)
            txt = f.readlines()
            strReturn=""
            matchid=""
            if txt:
                for line in txt:
                    if "timeout" in line:
                        continue
                    if "/ql/build" in line:
                        continue
                    if "/ql/static" in line:
                        continue                  
                    if "backend" in line:
                        continue
                    if ("node" in line and ".js" in line) or ("python3" in line and ".py" in line):
                        parts = line.split()
                        if len(parts) > 8:
                            pid = (parts[1]+"|"+parts[2]).ljust(15, ' ')                          
                        else:
                            pid = line.split()[0].ljust(15,' ')
                        if killpid in pid:
                            matchid=pid
                        strReturn=strReturn+pid+" "
                    else:
                        continue
            else:            
                await jdbot.send_message(chat_id,'当前系统未执行任何脚本')
                
            if killpid not in strReturn:
                await jdbot.send_message(chat_id,'进程结束失败: 当前系统未查询到该pid '+killpid+"\n进程列表:\n"+strReturn)
                return
                
            #存在进程则发起结束进程命令
            if "|" in matchid:                
                cmd = "kill "+matchid.split("|")[1]
                os.system(cmd)
                await asyncio.sleep(1)
                cmd = "kill "+matchid.split("|")[0]
                os.system(cmd)
                await asyncio.sleep(1)
            else:
                cmd = "kill "+killpid
                os.system(cmd)
                await asyncio.sleep(1)
                
            #再次查询该id是否存在确认已经正常结束进程            
            cmd = "ps -ef"
            f = os.popen(cmd)
            txt = f.readlines()
            strReturn=""
            if txt:
                for line in txt:
                    if "timeout" in line:
                        continue
                    if "/ql/build" in line:
                        continue
                    if "/ql/static" in line:
                        continue                  
                    if "backend" in line:
                        continue
                    if ("node" in line and ".js" in line) or ("python3" in line and ".py" in line):
                        parts = line.split()
                        if len(parts) > 8:
                            pid = (parts[1]+"|"+parts[2]).ljust(15, ' ')
                        else:
                            pid = line.split()[0].ljust(15,' ')
                        strReturn=strReturn+pid+" "
                    else:
                        continue
                        
            if killpid in strReturn:
                await jdbot.send_message(chat_id,'进程'+killpid+'强制结束失败!')
            else:
                await jdbot.send_message(chat_id,'进程'+killpid+'已被强制结束!')
                
            
        
    except Exception as e:
        title = "【💥错误💥】"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + sys._getframe().f_code.co_name
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n\n{tip}")
        logger.error(f"错误--->{str(e)}")


if ch_name:
    jdbot.add_event_handler(pidkill, events.NewMessage(from_users=chat_id, pattern=BOT_SET['命令别名']['cron']))