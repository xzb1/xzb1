import requests

def get_token():
    url: str = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx698858386bd59052&secret=f4387054f1a7872479aedb0a837937bb"
    try:
        access_token = requests.request("GET", url=url).json()['access_token']
        return access_token
    except:
        print('token获取失败')
        exit()

