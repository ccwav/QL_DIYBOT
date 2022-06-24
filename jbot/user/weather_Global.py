from telethon import events
from .login import user
import requests
import json

@user.on(events.NewMessage(pattern=r'.*天气.*', outgoing=True))
async def weatherInfo(event):
    
    message = event.message.text.split("天气")[0]
    if message==None:
        await event.edit('请输入正确的格式如:深圳天气')
        return
            
    url='https://www.tianqiapi.com/api/?version=v6&appid=74169348&appsecret=ti3VzXtb&city=%s'%message   
    try:
        weather_data=json.loads(requests.get(url).text)        
    except Exception as e:
        await user.send_message(event.chat_id,"获取天气信息错误:"+e)
        return
        
    if weather_data and (weather_data['city']==message or (weather_data['city']!="北京")):
        await user.send_message(event.chat_id,'当前城市：'+weather_data['city']+'\n更新时间：'+weather_data['update_time']+'\n建议：'+weather_data['air_tips']+'\n温度：'+weather_data['tem']+'℃\n风速：'+weather_data['win_speed']+'\n风力：'+weather_data['win_meter']+'\n风向：'+weather_data['win']+'\n天气：'+weather_data['wea'])
    else:
        await user.send_message(event.chat_id,'获取天气信息错误,可能输入的城市有误或不被支持!')    
    