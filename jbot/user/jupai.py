from telethon import events
from .login import user
import requests
import urllib.parse
from uuid import uuid4
from .. import LOG_DIR

@user.on(events.NewMessage(pattern=r'^jp', outgoing=True))
async def bot_bean(event):
    if event.is_reply is True:
        reply = await event.get_reply_message()
        text=reply.text
    else:
        msg_text= event.raw_text.split(' ')
        if isinstance(msg_text, list) and len(msg_text) == 2:
            text = msg_text[-1]
        else:
            text = None  
        
    if text==None:
        await event.edit('格式:jp 内容')
        return    
    else:
        await event.edit('开始生成图片，请稍后...')

    JP_IMG = f'{LOG_DIR}/bot/jp-{uuid4()}.png'
    params = { "msg": text }
    encoded = urllib.parse.urlencode(params)
    image_url = f"http://juapi.org/api/zt.php?{encoded}"
    response = requests.get(image_url)    
    open(JP_IMG, "wb").write(response.content)
    await event.delete()
    await user.send_message(event.chat_id,file=JP_IMG)

        
    
           

    
    



