# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import datetime
import os
import json
import re
import time
from random import sample
import httpx
from telethon import events
from .. import jdbot,chat_id,logger
from ..bot.utils import get_cks
from urllib.parse import unquote

try:
    from .login import user
except:
    from .. import user
    
@user.on(events.NewMessage(pattern=r'^jf', outgoing=True))
async def getyj(event):
    try:
        msg_text= event.raw_text.split(' ')
        if isinstance(msg_text, list) and len(msg_text) == 2:
            text = msg_text[-1]
        else:
            text = None
            
        if text==None:
            await event.edit('请指定要查询的账号,格式: jf ck数')
            return    
        else:        
            await event.edit("开始查询")
        
        #载入设定        
        waitsec=0
        issetconfig=False
        
        if os.path.exists("/ql/data/config/auth.json"):
            configpath="/ql/data/"
            ckfile="/ql/data/config/auth.json"
            
        if os.path.exists("/ql/config/auth.json"):
            configpath="/ql/"
            ckfile="/ql/config/auth.json"
            
        if os.path.exists("/jd/config/config.sh"):
            configpath="/jd/"
            ckfile=""
        
        if ckfile=="":
            await event.edit('不支持V4环境，退出...')
            return
            
        try:
            f = open(configpath+"config/ccbotSetting.json", "r+", encoding='utf-8')
            ccbotSetting = json.loads(f.read())
            f.close()
            for key in ccbotSetting:
                if key=="jf命令配置":
                    issetconfig=True
        except Exception as e:
            await event.edit(f'载入ccbotSetting.json出错,请检查内容!\n'+str(e))
            return
            
        if not issetconfig:
            await event.edit(f'载入ccbotSetting.json成功，但是缺少相应的配置,请检查!')
            return
            
        try:
            for key in ccbotSetting["jf命令配置"]:                
                if key=="多少秒后自动删除":
                    waitsec=int(ccbotSetting["jf命令配置"][key]) 
        except Exception as e:
            await event.edit(f'载入ccbotSetting.json的bd命令配置内容出错,请检查!\n'+str(e))
            return
                
        num = int(text)
        info = f'**【账号🆔{num}】💹佣金收入：**\n'
        
        cookies = get_cks(ckfile)
        if num > len(cookies):
            info += f'查询失败，您共有{len(cookies)}个账号'
        else:
            jfck = cookies[num - 1]
            pin = re.findall(r'(pt_pin=([^; ]+)(?=;?))',jfck)[0][1]
            if re.search('%', pin):
                pin = unquote(pin, 'utf-8')
            logger.error(jfck)
            start = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            info = f'**【账号🆔{pin}】💹佣金收入：**\n'  
            #info += f'【截止到{start}】\n' 

            yesterday = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
            sevendate = (datetime.datetime.now() + datetime.timedelta(days=-7)).strftime("%Y-%m-%d")           

            jfflinfo,jfflclickinfo,jfdata, get_ztmy, get_7my = await asyncio.gather(
                get_flinfo(jfck),
                get_flclickinfo(jfck),
                get_fl(jfck),
                get_fls(jfck, yesterday,yesterday),
                get_fls(jfck, sevendate,yesterday)
            )

            if jfflinfo['code'] == 200 and jfflclickinfo['code'] == 200 and jfdata['code'] == 200 and get_ztmy['code'] == 200 and get_7my['code'] == 200 :
                yj = 0
                count = 0
                keys = ['待付款', '取消']
                for i in jfdata['data']:
                    if all(k not in str(i['validCodeMsg']) for k in keys) and float(i['estimateFee']) > 0:
                        yj += i['estimateFee']
                        count += 1  
                info += f'【今日京粉信息】\n'               
                info += f'    【点击量】{jfflclickinfo["data"]["clickCount"]}\n    【引入UV】{jfflclickinfo["data"]["introduceUv"]}\n    【有效订单量】{jfflclickinfo["data"]["validOrderCount"]}\n'
                info += f'    【有效订单金额】{jfflclickinfo["data"]["validOrderAmount"]}\n    【预估收入】{jfflclickinfo["data"]["predictCommission"]}\n'
                info += f'\n【其他信息】\n'    
                info += f'    【昨日佣金】{get_ztmy["data"]}\n    【七日收入】{get_7my["data"]}\n    【本月预估结算】{jfflinfo["data"]["lastMonthAmount"]}\n    【下月预估结算】{jfflinfo["data"]["thisMonthAmount"]}'
            elif 'no login' in jfdata['data']:
                info += '查询失败，账号已过期'
            elif 'no register' in jfdata['data']:
                info += '查询失败，返利未激活'
            else:
                info += f'查询出错，错误详情\n{jfdata["data"], get_ztmy["data"], get_7my["data"]}'
                
        
        if waitsec==0:
            await event.edit(info)
        else:
            info=info+"\n\n【本条信息将在"+str(waitsec)+"秒钟后自动删除】"
            await event.edit(info)        
            await asyncio.sleep(waitsec)
            await event.delete()
        
    except Exception as e:
        title = "【💥错误💥】"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + e.__traceback__.tb_frame.f_code.co_name
        details = "错误详情：第 " + str(e.__traceback__.tb_lineno) + " 行"
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n{details}")
        logger.error(f"错误--->{str(e)}")


async def get_fl(cookie):
    try:
        dnow = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime('%Y-%m-%d %H:%M:%S')
        dtnow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        body = {
            "funName": "listOrderSku",
            "unionId": "",
            "param": {
                "startTime": dnow,
                "endTime": dtnow,
                "orderStatus": 0,
                "optType": 1,
                "unionRole": 1
            },
            "page": {
                "pageNo": 1,
                "pageSize": 100
            }
        }
        url = f'https://api.m.jd.com/api?functionId=listOrderSku&_={dtnow}&appid=u&body={body}&loginType=2'
        headers = {
            'Host': 'api.m.jd.com',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-cn',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'cookie': cookie,
            'Referer': 'https://jingfenapp.jd.com',
            'User-Agent': await userAgent()
        }
        async with httpx.AsyncClient(verify=False) as session:
            res = await session.get(url, headers=headers)
        if res.status_code == 200 and res.json().get('code') == 200:
            jforder, estimateFee, validCodeMsg = [], [], []
            dnow = datetime.datetime.now().strftime('%Y-%m-%d')
            dnow_reg = re.compile(dnow)
            jforders = res.json()['result']
            for order in jforders:
                if re.search(dnow_reg, order['orderTime']):
                    jforder.append(order['orderId'])
                    estimateFee.append(order['estimateFee'])
                    validCodeMsg.append(order['validCodeMsg'])
            jflist = []
            mid = map(list, zip(jforder, estimateFee, validCodeMsg))
            for item in mid:
                jfdict = dict(zip(['jforder', 'estimateFee', 'validCodeMsg'], item))
                jflist.append(jfdict)
            return {'code': 200, 'data': jflist}
        else:
            return {'code': 400, 'data': str(res.json())}
    except Exception as e:
        return {'code': 400, 'data': e}


async def get_fls(cookie, startdate,enddate):
    try:        
        body = {"funName": "querySpreadEffectData", "unionId": 2023952562, "param": {"startDate": startdate, "endDate": enddate}}
        url = f"https://api.m.jd.com/api?functionId=union_report&_={int(time.time() * 1000)}&appid=u&body={body}&loginType=2"
        headers = {
            'Host': 'api.m.jd.com',
            'Connection': 'keep-alive',
            'Cookie': cookie,
            'content-type': 'application/json',
            'Accept-Encoding': 'gzip,compress,br,deflate',
            'User-Agent': await userAgent(),
            'Referer': 'https://servicewechat.com/wxf463e50cd384beda/138/page-frame.html'
        }
        async with httpx.AsyncClient(verify=False) as session:
            res = await session.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            response = res.json()["result"]["spreadReportInfoSum"]["cosFee"]
            return {'code': 200, 'data': response}
        else:
            return {'code': 400, 'data': str(res.json())}
    except Exception as e:
        return {'code': 400, 'data': e}

    
async def get_flinfo(cookie):
    try:        
        body = {"funName": "queryYgCommTotal"}
        url = f"https://api.m.jd.com/api?functionId=union_balance_pay&_={int(time.time() * 1000)}&appid=u&body={body}&loginType=2"
        headers = {
            'Host': 'api.m.jd.com',
            'Connection': 'keep-alive',
            'Cookie': cookie,
            'content-type': 'application/json',
            'Accept-Encoding': 'gzip,compress,br,deflate',
            'User-Agent': await userAgent(),
            'Referer': 'https://servicewechat.com/wxf463e50cd384beda/138/page-frame.html'
        }
        async with httpx.AsyncClient(verify=False) as session:
            res = await session.get(url, headers=headers, timeout=10)
        
        if res.status_code == 200:
            response = res.json()["result"]
            return {'code': 200, 'data': response}
        else:
            return {'code': 400, 'data': str(res.json())}
    except Exception as e:
        return {'code': 400, 'data': e}

async def get_flclickinfo(cookie):
    try:        
        dtnow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        body = {"funName":"getIndexStatisticsInfoList","param":{"startTime":dtnow,"endTime":dtnow}}
        url = f"https://api.m.jd.com/api?functionId=union_data_bi_shop&_={int(time.time() * 1000)}&appid=u_jfapp&body={body}&loginType=2"
        headers = {
            'Host': 'api.m.jd.com',
            'Connection': 'keep-alive',
            'Cookie': cookie,
            'content-type': 'application/json',
            'Accept-Encoding': 'gzip,compress,br,deflate',
            'User-Agent': await userAgent(),
            'Referer': 'https://jingfenapp.jd.com/'
        }
        async with httpx.AsyncClient(verify=False) as session:
            res = await session.get(url, headers=headers, timeout=10)
        
        if res.status_code == 200:
            response = res.json()["result"]
            return {'code': 200, 'data': response}
        else:
            return {'code': 400, 'data': str(res.json())}
    except Exception as e:
        return {'code': 400, 'data': e}

async def userAgent():
    """
    随机生成一个UA
    """
    uuid = ''.join(sample('123456789abcdef123456789abcdef123456789abcdef123456789abcdef', 40))
    addressid = ''.join(sample('1234567898647', 10))
    iosVer = ''.join(sample(["14.5.1", "14.4", "14.3", "14.2", "14.1", "14.0.1", "13.7", "13.1.2", "13.1.1"], 1))
    iosV = iosVer.replace('.', '_')
    iPhone = ''.join(sample(["8", "9", "10", "11", "12", "13"], 1))
    ADID = ''.join(sample('0987654321ABCDEF', 8)) + '-' + ''.join(sample('0987654321ABCDEF', 4)) + '-' + ''.join(sample('0987654321ABCDEF', 4)) + '-' + ''.join(sample('0987654321ABCDEF', 4)) + '-' + ''.join(sample('0987654321ABCDEF', 12))
    return f'jdapp;iPhone;10.0.4;{iosVer};{uuid};network/wifi;ADID/{ADID};model/iPhone{iPhone},1;addressid/{addressid};appBuild/167707;jdSupportDarkMode/0;Mozilla/5.0 (iPhone; CPU iPhone OS {iosV} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/null;supportJDSHWK/1'
