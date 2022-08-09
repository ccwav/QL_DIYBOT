from telethon import events, Button
from .. import jdbot, chat_id, LOG_DIR, logger, BOT_SET, ch_name
from ..bot.quickchart import QuickChart, QuickChartFunction
from ..bot.beandata import get_bean_data
from ..bot.utils import V4,split_list, press_event
from uuid import uuid4
from .login import user

BEAN_IMG = f'{LOG_DIR}/bot/bean-{uuid4()}.jpg'

@user.on(events.NewMessage(pattern=r'^bc', outgoing=True))
async def my_chartinfo(event):
    msg_text= event.raw_text.split(' ')
    if isinstance(msg_text, list) and len(msg_text) == 2:
        text = msg_text[-1]
    else:
        text = None  
    
    if text==None:
        await event.edit('请指定要查询的账号,格式: bc 1 或 bc ptpin')
        return    
    else:
        await event.edit('开始查询账号'+text+'的资产，请稍后...')
    
    if text and int(text):
        res = get_bean_data(int(text))
        if res['code'] != 200:
            await event.delete()
            await user.send_message(event.chat_id,f'something wrong,I\'m sorry\n{str(res["data"])}')
        else:
            aver = (res["data"][0][0]+res["data"][0][1]+res["data"][0][2]+res["data"][0][3]+res["data"][0][4]+res["data"][0][5]+res["data"][0][6])//7
            nickname=res['data'][4]
            createChart(res['data'][0],res['data'][1],f'       {nickname} · 近七天平均收入{aver}豆⚡',res['data'][3],text)
            await event.delete()
            await user.send_message(event.chat_id,f'您的账号{text}收支情况',file=BEAN_IMG)
    

def createChart(income,out,Title,label,text):
    qc = QuickChart()
    qc.width=1000
    qc.height=500
    qc.background_color="#22252a"
    qc.config = {
     "data": {
      "datasets": [{
        "backgroundColor": QuickChartFunction('getGradientFillHelper(\'vertical\', ["#faab2c", "#f48847", "#ef5d68"])'),
        "data": income,
        "label": "收入",
        "type": "bar"
       },
       {
        "backgroundColor": QuickChartFunction('getGradientFillHelper(\'vertical\', ["#777777", "#747474"])'),
        "data": out,
        "label": "支出",
        "type": "bar"
       }
      ],
      "labels": label
     },
     "options": {
      "plugins": {
       "datalabels": {
        "display": True,
        "color": "#eee",
        "align": "top",
        "offset": -4,
        "anchor": "end",
        "font": {
         "family": "Helvetica Neue",
         "size": 16
        }
       }
      },
      "legend": {
       "position": "bottom",
       "align": "end",
       "display": True
      },
      "layout": {
       "padding": {
        "left": 10,
        "right": 20,
        "top": 30,
        "bottom": 15
       }
      },
      "responsive": True,
      "title": {
       "display": True,
       "position": "bottom",
       "text": Title,
       "fontSize": 20,
       "fontColor": "#aaa"
      },
      "tooltips": {
       "intersect": True,
       "mode": "index"
      },
      "scales": {
       "xAxes": [{
        "gridLines": {
         "display": True,
         "color": ""
        },
        "ticks": {
         "display": True,
         "fontSize": 16,
         "fontColor": "#999"
        }
       }],
       "yAxes": [{
        "gridLines": {
         "display": True,
         "color": ""
        },
        "ticks": {
         "display": True,
         "fontSize": 14,
         "fontColor": "#999"
        }
       }]
      }
     },
     "type": "bar"
    }
    qc.to_file(BEAN_IMG)