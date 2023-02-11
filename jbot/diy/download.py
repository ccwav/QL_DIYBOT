#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from asyncio import exceptions

import os
import re
import requests
import sys
from telethon import events, Button

from .. import chat_id, jdbot, CONFIG_DIR, SCRIPTS_DIR, OWN_DIR, logger, BOT_DIR, ch_name, BOT
from ..bot.utils import press_event, backup_file, Remove_file, add_cron, cmd, DIY_DIR, TASK_CMD, split_list
import json
from ..diy.utils import mycronup, read, write


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^https?://.*(js|py|sh)$'))
async def mydownload(event):
    try:
        SENDER = event.sender_id
        furl = event.raw_text
        if '下载代理' in BOT.keys() and str(BOT['下载代理']).lower() != 'false' and 'github' in furl:
            furl = f'{str(BOT["下载代理"])}/{furl}'
        try:
            resp = requests.get(furl).text
            if "</html>" in resp:
                await jdbot.send_message(chat_id, f"接收到的[链接]({furl})是一个页面并非raw数据，会话结束")
                return
        except Exception as e:
            await jdbot.send_message(chat_id, f"下载失败\n{e}")
            return
            
        runcmd=""    
        async with jdbot.conversation(SENDER, timeout=60) as conv:
            fname = furl.split('/')[-1]
            filename=fname
            fname_cn = ''
            if furl.endswith(".js"):
                fname_cn = re.findall(r"(?<=new\sEnv\(').*(?=')", resp, re.M)
                if fname_cn != []:
                    fname_cn = fname_cn[0]
                else:
                    fname_cn = ''
                    
            btn = []
            
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
                    if key=="文件存放配置":
                        issetconfig=True
            except Exception as e:
                await jdbot.send_message(chat_id,f'载入ccbotSetting.json出错,请检查内容!\n'+str(e))
                return
                
            if not issetconfig:
                await jdbot.send_message(chat_id, f'载入ccbotSetting.json成功，但是缺少相应的配置,请检查!')
                return
            
            getfileSettinglist=ccbotSetting["文件存放配置"]
        
            countbtn=3
            for fileSetting in getfileSettinglist: 
                if fileSetting["按钮名字"]=="配置档":
                    countbtn=int(fileSetting["每行按钮数"])
                else:
                    btn.append(Button.inline(fileSetting["按钮名字"], data=fileSetting["按钮名字"]+"|"+fileSetting["存放路径"]))          
            btn.append(Button.inline('取消', data='取消|cancel'))
            btn = split_list(btn, countbtn)
        
            cmdtext = False
            msg = await conv.send_message(f'成功下载{fname_cn}脚本\n现在，请做出你的选择：', buttons=btn)
            convdata = await conv.wait_event(press_event(SENDER))                
            res = bytes.decode(convdata.data)
            isbackup="1"
            noaskaddcron="0"
            
            for fileSetting in getfileSettinglist: 
                if fileSetting["按钮名字"]=="配置档":
                    continue
                if fileSetting["按钮名字"]==res.split("|")[0]:
                    isbackup=fileSetting["备份原脚本"]                    
                    for key in fileSetting:
                        if "执行命令" in key:
                            if runcmd!="" :     
                                runcmd=runcmd+"\n"
                            runcmd=runcmd+fileSetting[key].replace("文件名",filename)
                        if "不问是否定时" in key:  
                            noaskaddcron=fileSetting[key]
            isrun="0"
            res=res.split("|")[1]
            if "task " in res:
                isrun="1"
                res=res.replace("task ","")
                
            markup = [Button.inline('是', data='yes'),
                      Button.inline('否', data='no')]
            if res == 'cancel':
                msg = await jdbot.edit_message(msg, '对话已取消')
                conv.cancel()
                return
            else:
                res2=""
                if noaskaddcron=="0":
                    msg = await jdbot.edit_message(msg, '是否尝试自动加入定时', buttons=markup)
                    convdata2 = await conv.wait_event(press_event(SENDER))
                    res2 = bytes.decode(convdata2.data)
                
                if isbackup=="1":
                    backup_file(f'{res}/{filename}')
                else:
                    Remove_file(f'{res}/{filename}')
                    
                if isrun=="1":    
                    cmdtext = f'{TASK_CMD} {res}/{filename} now'
                    
                with open(f'{res}/{filename}', 'w+', encoding='utf-8') as f:
                    f.write(resp)
                
                if res2 == 'yes':
                    await add_cron(jdbot, conv, resp, filename, msg, SENDER, markup, res)
                else:
                    await jdbot.edit_message(msg, f'{filename}已保存到{res}文件夹')
                conv.cancel()
        if cmdtext:
            if runcmd!="":     
                runcmd=cmdtext+"\n"+runcmd
            else:
                runcmd=cmdtext
            
        if runcmd!="":             
            msg=await jdbot.send_message(chat_id,"开始执行命令列表"+":\n"+runcmd)
            cmdlist=runcmd.split("\n")
            for RunCommound in cmdlist: 
                await cmd(RunCommound)
                
            await jdbot.edit_message(msg, '任务执行完毕，祝君愉快.')
        
    except exceptions.TimeoutError:
        await jdbot.edit_message(msg, '选择已超时，对话已停止，感谢你的使用')
    except Exception as e:
        title = "【💥错误💥】"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + sys._getframe().f_code.co_name
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n\n{tip}")
        logger.error(f"错误--->{str(e)}")


if ch_name:
    jdbot.add_event_handler(mydownload, events.NewMessage(from_users=chat_id, pattern=BOT['命令别名']['cron']))

