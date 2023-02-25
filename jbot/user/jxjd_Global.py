from telethon import events
from .. import jdbot
from ..diy.utils import read, write
import re
import requests,json

try:
    from .login import user
except:
    from .. import user
    
@user.on(events.NewMessage(pattern=r'^jx', outgoing=True))
async def jcmd(event):
    strText=""
    if event.is_reply is True:
        reply = await event.get_reply_message()
        strText=reply.text
    else:    
        msg_text= event.raw_text.split(' ')
        if isinstance(msg_text, list) and len(msg_text) == 2:
            strText = msg_text[-1]
    
    if strText==None:
        await user.send_message(event.chat_id,'请指定要解析的口令,格式: jx 口令 或对口令直接回复jx ')
        return 
        
    jumpUrl=""
    title=""    
    jiexiurl = "http://api.nolanstore.top/JComExchange"    
    data ={"code": strText}
    headers={"Content-Type": "application/json"}
    issuccess=False
    for num in range(10):  
        try:
            res=requests.post(url=jiexiurl,headers=headers,json=data,timeout=3)
            issuccess=True
        except:
            issuccess=False
        if issuccess:
            break
    resdata=json.loads(res.text)
    if resdata["code"]=="0":  
        title = resdata["data"]['title']
        jumpUrl = resdata["data"]['jumpUrl']
        
    if jumpUrl != "":        
        await user.send_message(event.chat_id,title+"\n"+jumpUrl)
    else:
        await user.send_message(event.chat_id,"解析出错:"+data.get("data"))
    
    