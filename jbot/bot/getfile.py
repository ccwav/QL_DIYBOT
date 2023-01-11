from telethon import events, Button
from asyncio import exceptions
from .. import jdbot, chat_id, SCRIPTS_DIR, CONFIG_DIR, logger
from .utils import press_event, backup_file, Remove_file, add_cron, cmd, DIY_DIR, TASK_CMD, split_list
import json

@jdbot.on(events.NewMessage(from_users=chat_id))
async def bot_get_file(event):
    """定义文件操作"""
    try:        
        btn = []
        f = open("/ql/config/getfileSetting.json", "r+", encoding='utf-8')
        getfileSettinglist = json.loads(f.read())
        f.close()
        countbtn=3
        for fileSetting in getfileSettinglist: 
            if fileSetting["按钮名字"]=="配置档":
                countbtn=int(fileSetting["每行按钮数"])
            else:
                btn.append(Button.inline(fileSetting["按钮名字"], data=fileSetting["存放路径"]))          
        btn.append(Button.inline('取消', data='cancel'))
        btn = split_list(btn, countbtn)   
        
        SENDER = event.sender_id
        if event.message.file:
            markup = []
            filename = event.message.file.name
            cmdtext = None
            async with jdbot.conversation(SENDER, timeout=180) as conv:
                msg = await conv.send_message('请选择您要放入的文件夹或操作：\n')
                markup = btn
                
                msg = await jdbot.edit_message(msg, '请选择您要放入的文件夹或操作：', buttons=markup)
                convdata = await conv.wait_event(press_event(SENDER))
                
                res = bytes.decode(convdata.data)
                isbackup="1"                
                for fileSetting in getfileSettinglist: 
                    if fileSetting["按钮名字"]=="配置档":
                        continue
                    if fileSetting["存放路径"]==res:
                        isbackup=fileSetting["备份原脚本"]
                        
                isrun="0"
                if "task " in res:
                    isrun="1"
                    res=res.replace("task ","")
                    
                markup = [Button.inline('是', data='yes'),
                          Button.inline('否', data='no')]
                if res == 'cancel':
                    msg = await jdbot.edit_message(msg, '对话已取消')
                    conv.cancel()
                else:
                    msg = await jdbot.edit_message(msg, '是否尝试自动加入定时', buttons=markup)
                    convdata2 = await conv.wait_event(press_event(SENDER))
                    res2 = bytes.decode(convdata2.data)
                    
                    if isbackup=="1":
                        backup_file(f'{res}/{filename}')
                    else:
                        Remove_file(f'{res}/{filename}')
                        
                    if isrun=="1":    
                        cmdtext = f'{TASK_CMD} {res}/{filename} now'
                    await jdbot.download_media(event.message, res)
                    with open(f'{res}/{filename}', 'r', encoding='utf-8') as f:
                        resp = f.read()
                    if res2 == 'yes':
                        await add_cron(jdbot, conv, resp, filename, msg, SENDER, markup, res)
                    else:
                        await jdbot.edit_message(msg, f'{filename}已保存到{res}文件夹')
                    conv.cancel()    
            if cmdtext:
                await cmd(cmdtext)
    except exceptions.TimeoutError:
        msg = await jdbot.send_message(chat_id, '选择已超时，对话已停止')
    except Exception as e:
        await jdbot.send_message(chat_id, f'something wrong,I\'m sorry\n{str(e)}')
        logger.error(f'something wrong,I\'m sorry\n{str(e)}')