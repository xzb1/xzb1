# -*-coding:utf8;-*-
import json
import time
import requests
from Meizu_cities import cities
from Meizu_city import city


def get_token():
    url: str = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx698858386bd59052&secret=f4387054f1a7872479aedb0a837937bb"
    try:
        access_token = requests.request("GET", url=url).json()['access_token']
        return access_token
    except:
        print('token获取失败')
        exit()


def get_cityid(city_name):
    for i in cities:
        if i['city'] == city_name:
            return i['cityid']


def get_citiesid(city_name):
    for i in city:
        if i['countyname'] == city_name:
            return i['areaid']


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
        weathers = response['weathers'][6]
        keyword1 = f"{city_name}地区{weathers['date']}天气如下："
        keyword2 = f"天气状况:{weathers['weather']}"
        keyword3 = f"最高气温:{weathers['temp_day_c']}°"
        keyword4 = f"最低气温:{weathers['temp_night_c']}°"
        try:
            keyword5 = f"气温预警:{response['alarms'][0]['alarmDesc']}"
        except:
            keyword5 = '暂无天气预警'
        return [keyword1, keyword2, keyword3, keyword4, keyword5]

    if day in ['明天', '明日']:
        weathers = response['weathers'][0]
        keyword1 = f"{city_name}地区{weathers['date']}天气如下："
        keyword2 = f"天气状况:{weathers['weather']}"
        keyword3 = f"最高气温:{weathers['temp_day_c']}°"
        keyword4 = f"最低气温:{weathers['temp_night_c']}°"
        return [keyword1, keyword2, keyword3, keyword4]

    if day in ['后天', '后日']:
        weathers = response['weathers'][1]
        keyword1 = f"{city_name}地区{weathers['date']}天气如下："
        keyword2 = f"天气状况:{weathers['weather']}"
        keyword3 = f"最高气温:{weathers['temp_day_c']}°"
        keyword4 = f"最低气温:{weathers['temp_night_c']}°"
        return [keyword1, keyword2, keyword3, keyword4]

    if day in ['七天']:
        print('暂未提供')


def send(keyword):
    yiyan = requests.get(url='https://api.lovelive.tools/api/SweetNothings').text
    access_token = get_token()
    url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={access_token}"
    template_id = 'x80dmd4J2PHe-83ysz0MZoAg3C2hGmpy9Eq2MSeARRI'
    touser = ['olNUf5v1Ccbl5jr6FaQaPFkqBNGs', 'olNUf5rFSQnQyPh23LyEc5QnWppI']
    headers = {
        'Content-Type': 'application/json'
    }
    for uesr in touser:
        payload = json.dumps({
            "touser": uesr,
            "template_id": template_id,
            "data": {
                "first": {
                    "value": yiyan,
                    "color": "#FF0000"
                },
                "keyword1": {
                    "value": keyword[0],
                    "color": "#0000FF"
                },
                "keyword2": {
                    "value": keyword[1],
                    "color": "#0000FF"
                },

                "keyword3": {
                    "value": keyword[2],
                    "color": "#0000FF"
                },
                "keyword4": {
                    "value": keyword[3],
                    "color": "#0000FF"
                },
                "keyword5": {
                    "value": keyword[4],
                    "color": "#0000FF"
                },
                "keyword6": {
                    "value": "今天丽丽也要元气满满哦！(＠＾０＾＠)",
                    "color": "#FF0000"
                },
            }
        })
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
        time.sleep(5)


if __name__ == "__main__":
    massage = '今天南昌天气'
    day = massage[0:2]
    massage = massage[2:len(massage)]
    city_name = massage.split('天气')[0]
    city_id = get_cityid(city_name)
    if get_cityid(city_name) == None:
        city_id = get_citiesid(city_name)
        if city_id == None:
            print('没找到城市编号')
            exit()

    send(keyword=weather(city_id=city_id, day=day))
