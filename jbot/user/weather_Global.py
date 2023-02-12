from telethon import events
import requests
import json
import os
import asyncio
try:
    from .login import user
except:
    from .. import user
    
@user.on(events.NewMessage(pattern=r'.*天气$', outgoing=True))
async def weatherInfo(event):

    #载入设定
    waitsec=0
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
            if key=="天气命令配置":
                issetconfig=True
    except Exception as e:
        await event.edit(f'载入ccbotSetting.json出错,请检查内容!\n'+str(e))
        return
        
    if not issetconfig:
        await event.edit(f'载入ccbotSetting.json成功，但是缺少相应的配置,请检查!')
        return
        
    try:
        for key in ccbotSetting["天气命令配置"]:                
            if key=="多少秒后自动删除":
                waitsec=int(ccbotSetting["天气命令配置"][key]) 
    except Exception as e:
        await event.edit(f'载入ccbotSetting.json的bd命令配置内容出错,请检查!\n'+str(e))
        return 
                
    message = event.message.text.split("天气")[0]
    if message==None:
        await event.edit('请输入正确的格式如:深圳天气')
        return
    
    url='http://hm.suol.cc/API/tq.php?msg='+message+'&n=1'
    try:
        weather_data=requests.get(url).text
    except Exception as e:
        await event.edit("获取天气信息错误:"+e)
        return
    strweatherinfo=""
    strotherinfo=""
    lncount=0
    weatherinfos=weather_data.split("\n")
    for weatherline in weatherinfos:
        lncount=lncount+1
        if "：" in weatherline:
            Title=weatherline.split("：")[0]
            if Title=="预警信息":
                strweatherinfo+=weatherline.replace("预警信息：","")+"\n"
            else:
                strweatherinfo+="【"+Title+"】 "+weatherline.split("：")[1]+"\n"
        else:
            if lncount==1:
                strweatherinfo+="【位置】 "+weatherline+"\n"
            else:
                if strotherinfo!="":
                    strotherinfo+="\n"
                strotherinfo+=weatherline
                
    
    if strotherinfo!="":
        strweatherinfo+="【温馨提示】"+strotherinfo
        
    if strweatherinfo =="" :
        strweatherinfo='获取天气信息错误,可能输入的城市有误或不被支持!'
        
    if waitsec==0:
        await event.edit(strweatherinfo)
    else:
        strweatherinfo=strweatherinfo+"\n\n【本条信息将在"+str(waitsec)+"秒钟后自动删除】"
        await event.edit(strweatherinfo)        
        await asyncio.sleep(waitsec)
        await event.delete()