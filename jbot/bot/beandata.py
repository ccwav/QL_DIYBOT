import requests
import datetime
import time
import json
from datetime import timedelta
from datetime import timezone
from .utils import CONFIG_SH_FILE, get_cks, AUTH_FILE, QL,logger
SHA_TZ = timezone(
    timedelta(hours=8),
    name='Asia/Shanghai',
)
requests.adapters.DEFAULT_RETRIES = 5
session = requests.session()
session.keep_alive = False

url = "https://api.m.jd.com/api"


def gen_body(page):
    body = {
        "beginDate": datetime.datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(SHA_TZ).strftime("%Y-%m-%d %H:%M:%S"),
        "endDate": datetime.datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(SHA_TZ).strftime("%Y-%m-%d %H:%M:%S"),
        "pageNo": page,
        "pageSize": 20,
    }
    return body


def gen_params(page):
    body = gen_body(page)
    params = {
        "functionId": "jposTradeQuery",
        "appid": "swat_miniprogram",
        "client": "tjj_m",
        "sdkName": "orderDetail",
        "sdkVersion": "1.0.0",
        "clientVersion": "3.1.3",
        "timestamp": int(round(time.time() * 1000)),
        "body": json.dumps(body)
    }
    return params

def get_beans_7days(ck):
    try:
        day_7 = True
        page = 0
        headers = {            
            "Content-Type": "application/x-www-form-urlencoded;",           
            "User-Agent": "Mozilla/5.0 (Linux; Android 12; SM-G9880) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36 EdgA/106.0.1370.47",
            "Cookie": ck
        }
        days = []
        for i in range(0, 7):
            days.append(
                (datetime.date.today() - datetime.timedelta(days=i)).strftime("%Y-%m-%d"))
        beans_in = {key: 0 for key in days}
        beans_out = {key: 0 for key in days}
        
        while day_7:
            page = page + 1            
            url="https://bean.m.jd.com/beanDetail/detail.json?page="+str(page)
            resp = session.get(url,headers=headers, timeout=100).text           
            amount=0
            res = json.loads(resp)
            if res['code'] == "0":
                for i in res['jingDetailList']:
                    amount=int(i['amount'])
                    for date in days:                        
                        if str(date) in i['date'] and amount > 0:
                            beans_in[str(date)] = beans_in[str(
                                date)] + amount
                            break
                        elif str(date) in i['date'] and amount < 0:
                            beans_out[str(date)] = beans_out[str(
                                date)] + amount
                            break
                    if i['date'].split(' ')[0] not in str(days):                                                
                        day_7 = False
            else:
                return {'code': 400, 'data': res}
        return {'code': 200, 'data': [beans_in, beans_out, days]}
    except Exception as e:
        logger.error(str(e))
        return {'code': 400, 'data': str(e)}

def get_total_beans(ck):
    try:
        headers = {
            "Accept": "application/json,text/plain, */*",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-cn",
            "Connection": "keep-alive",
            "Cookie": ck,
            "Referer": "https://wqs.jd.com/my/jingdou/my.shtml?sceneval=2",
            "User-Agent": "Mozilla/5.0 (Linux; Android 12; SM-G9880) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36 EdgA/106.0.1370.47"
        }
        jurl = "https://wq.jd.com/user/info/QueryJDUserInfo?sceneval=2"
        resp = session.get(jurl, headers=headers, timeout=100).text
        res = json.loads(resp)       
        return res['base']['jdNum'],res['base']['nickname'],'http://storage.360buyimg.com/i.imageUpload/b6adc6e4bbaa31363437393935323238323435_mid.jpg'
    except Exception as e:
        logger.error(str(e))

def get_bean_data(i):
    try:
        if QL:
            ckfile = AUTH_FILE
        else:
            ckfile = CONFIG_SH_FILE
        cookies = get_cks(ckfile)
        if cookies:
            ck = cookies[i-1]
            beans_res = get_beans_7days(ck)
            beantotal,nickname,pic = get_total_beans(ck)
            if beans_res['code'] != 200:
                return beans_res
            else:
                beans_in, beans_out = [], []
                beanstotal = [int(beantotal), ]
                for i in beans_res['data'][0]:
                    beantotal = int(
                        beantotal) - int(beans_res['data'][0][i]) - int(beans_res['data'][1][i])
                    beans_in.append(int(beans_res['data'][0][i]))
                    beans_out.append(int(str(beans_res['data'][1][i]).replace('-', '')))
                    beanstotal.append(beantotal)
            return {'code': 200, 'data': [beans_in[::-1], beans_out[::-1], beanstotal[::-1], beans_res['data'][2][::-1],nickname,pic]}
    except Exception as e:
        logger.error(str(e))