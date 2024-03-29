from telethon import events, Button
import requests
from asyncio import exceptions
from .. import jdbot, chat_id, logger, SCRIPTS_DIR, CONFIG_DIR, logger, BOT_SET, ch_name
from .utils import press_event, backup_file, Remove_file, add_cron, cmd, DIY_DIR, TASK_CMD, split_list
import json
import os

@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/dl'))
async def bot_url_file(event):
    '''接收github链接后执行程序'''
    msg_text = event.raw_text.split(' ')
    try:
        if isinstance(msg_text,list) and len(msg_text) == 2:
            url = msg_text[-1]
        else:
            url = None
        SENDER = event.sender_id
        if not url:
            await jdbot.send_message(chat_id, '请正确使用dl命令，需加入下载链接')
            return
        else:
            msg = await jdbot.send_message(chat_id, '请稍后正在下载文件')
            
        if '下载代理' in BOT_SET.keys() and str(BOT_SET['下载代理']).lower() != 'false' and 'github' in url:
            url = f'{str(BOT_SET["下载代理"])}/{url}'
            
        filename = url.split('/')[-1]
        resp = requests.get(url).text
        
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
        
        
        if resp:
            markup = []            
            cmdtext = None
            runcmd = ""
            
            async with jdbot.conversation(SENDER, timeout=30) as conv:
                await jdbot.delete_messages(chat_id, msg)
                msg = await conv.send_message('请选择您要放入的文件夹或操作：\n')
                markup = btn                
                msg = await jdbot.edit_message(msg, '请选择您要放入的文件夹或操作：', buttons=markup)
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
        msg = await jdbot.send_message(chat_id, '选择已超时，对话已停止')
    except Exception as e:
        await jdbot.send_message(chat_id, f'something wrong,I\'m sorry\n{str(e)}')
        logger.error(f'something wrong,I\'m sorry\n{str(e)}')

if ch_name:
    jdbot.add_event_handler(bot_url_file, events.NewMessage(
        from_users=chat_id, pattern=BOT_SET['命令别名']['dl']))
