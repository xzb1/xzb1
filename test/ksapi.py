# coding:utf8
# import os
#
# os.chdir('/zs/wx')
import hashlib
import time

import requests
import xmltodict
from flask import Flask, request, abort

from log import log

# token
WECHAT_TOKEN = 'yZdk8Z'
app = Flask(__name__)


def we():
    wea = weather(city_id=101240101, day='今天')
    var = ''
    for i in wea:
        var = var + i + '\n'
    return var


def boast():
    key = 'c46aee67be0d7d28474c869ab89982d6'
    url = f'http://api.tianapi.com/caihongpi/index?key={key}'
    response = requests.get(url).json()
    if response['code'] == 200:
        var = response['newslist'][0]['content']
    else:
        var = 'api获取失败'
    return var


def flatterer():
    key = 'c46aee67be0d7d28474c869ab89982d6'
    url = f'http://api.tianapi.com/tiangou/index?key={key}'
    response = requests.get(url).json()
    if response['code'] == 200:
        var = response['newslist'][0]['content']
    else:
        var = 'api获取失败'
    return var


def spare():
    return '暂时未开发，等着丽丽提建议哦'


def weather(city_id, day):
    url = f"https://aider.meizu.com/app/weather/listWeather?cityIds={city_id}"
    response = requests.request("GET", url).json()['value'][0]
    city_name = response['city']
    realtime_weathers = response['realtime']
    if day in ['实时', '现在']:
        print(f"{city_name}{realtime_weathers['time']}天气：")
        print(f"天气状况:{realtime_weathers['weather']}")
        print(f"温度:{realtime_weathers['temp']}°")

    if day in ['今天', '今日']:
        weathers = response['weathers'][0]
        keyword1 = f"{city_name}地区{weathers['date']}天气如下："
        keyword2 = f"天气状况:{weathers['weather']}"
        keyword3 = f"最高气温:{weathers['temp_day_c']}°"
        keyword4 = f"最低气温:{weathers['temp_night_c']}°"
        try:
            keyword5 = f"气温预警:{response['alarms'][0]['alarmDesc']}"
            return [keyword1, keyword2, keyword3, keyword4, keyword5]
        except:
            return [keyword1, keyword2, keyword3, keyword4]

    if day in ['明天', '明日']:
        weathers = response['weathers'][1]
        keyword1 = f"{city_name}地区{weathers['date']}天气如下："
        keyword2 = f"天气状况:{weathers['weather']}"
        keyword3 = f"最高气温:{weathers['temp_day_c']}°"
        keyword4 = f"最低气温:{weathers['temp_night_c']}°"
        return [keyword1, keyword2, keyword3, keyword4]

    if day in ['后天', '后日']:
        weathers = response['weathers'][2]
        keyword1 = f"{city_name}地区{weathers['date']}天气如下："
        keyword2 = f"天气状况:{weathers['weather']}"
        keyword3 = f"最高气温:{weathers['temp_day_c']}°"
        keyword4 = f"最低气温:{weathers['temp_night_c']}°"
        return [keyword1, keyword2, keyword3, keyword4]

    if day in ['七天']:
        print('暂未提供')


@app.route('/api', methods=['GET', 'POST'])
def wechat():
    if request.method == 'GET':
        # 第一次接入服务器
        signature = request.args.get('signature')
        timestamp = request.args.get('timestamp')
        nonce = request.args.get('nonce')
        echostr = request.args.get('echostr')
        li = [WECHAT_TOKEN, timestamp, nonce]
        # 列表排序重组加密
        li.sort()
        # 拼接字符
        tem_str = "".join(li)
        # sha1加密,以下步骤很重要
        s1 = hashlib.sha1()
        s1.update(tem_str.encode('utf8'))
        sigin = s1.hexdigest()
        # 签名值对比，相同证明请求来自微信
        # 错误返回403页面

        if signature != sigin:
            abort(403)
        else:
            return echostr

    if request.method == 'POST':
        logger = log()
        # 表示微信服务器转发消息到本地服务器
        xml_str = request.data

        if not xml_str:
            return abort(403)
        # 对xml字符串进行解析
        xml_dict1 = xmltodict.parse(xml_str).get('xml')
        print(xml_dict1)
        # 提取消息类型
        msg_type = xml_dict1.get('MsgType')
        if msg_type == 'event':
            logger.info(f"发送者:{xml_dict1.get('FromUserName')}，点击了:{xml_dict1.get('EventKey')}")

            if xml_dict1.get('EventKey') == 'weather':
                content = we()

            if xml_dict1.get('EventKey') == 'boast':
                content = boast()

            if xml_dict1.get('EventKey') == 'flatterer':
                content = flatterer()

            if xml_dict1.get('EventKey') == 'spare':
                content = spare()

            resp_dict = {
                "xml": {
                    'ToUserName': xml_dict1.get('FromUserName'),
                    'FromUserName': xml_dict1.get('ToUserName'),
                    'CreateTime': int(time.time()),
                    'MsgType': 'text',
                    'Content': content,
                }
            }
            resp_xml_str = xmltodict.unparse(resp_dict)
            return resp_xml_str

        if msg_type == 'text':
            # 这是文本消息
            # 构造返回值，由为微信服务器回复消息
            # 重点：以下参数值一个不能少，一个字母不能错，大小写不能错，键名必须完全一样
            resp_dict = {
                "xml": {
                    'ToUserName': xml_dict1.get('FromUserName'),
                    'FromUserName': xml_dict1.get('ToUserName'),
                    'CreateTime': int(time.time()),
                    'MsgType': 'text',
                    'Content': xml_dict1.get('Content'),
                }
            }
        resp_xml_str = xmltodict.unparse(resp_dict)
        # print(resp_xml_str)
        # # 返回消息字符串
        if xml_dict1.get('Content') is not None:
            logger.info(f'[发送人：{xml_dict1.get("FromUserName")},发送内容：{xml_dict1.get("Content")}]')
        return resp_xml_str


if __name__ == "__main__":
    app.run(debug=True, port=5700)

# if __name__ == '__main__':
#     server = pywsgi.WSGIServer(('0.0.0.0', 5700), app)
#     server.serve_forever()
