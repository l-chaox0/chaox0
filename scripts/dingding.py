#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests,datetime,time,hashlib,hmac,base64,re,json

class DingDing:
    def __init__(self,phone,ding_info):
        self.phone = phone
        self.ding_info = ding_info
    def ding_msg(self):
        secret = 'SEC***************************************************'
        access_token = 'access_token=**********************************'
        if self.phone == "all":
            isall = "true"
        else:
            isall = "false"
        timestamp = int(round(time.time() * 1000))
        data = ('\n'.join([str(timestamp),secret])).encode('utf-8')
        secret = secret.encode('utf-8')
        signature = base64.b64encode(hmac.new(secret, data, digestmod=hashlib.sha256).digest())
        reg = re.compile(r"'(.*)'")
        signature = str(re.findall(reg,str(signature))[0])
        url = 'https://oapi.dingtalk.com/robot/send?%s&sign=%s&timestamp=%s' % (access_token, signature, timestamp)
        headers = {"Content-Type": "application/json;charset=utf-8"}
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        json_msg = {
            'msgtype': 'text',
            'text': {
                'content': '\n'.join([nowTime,self.ding_info])
            },
            'at': {
                'atMobiles':
                    self.phone
                ,
                'isAtAll': isall
            }
        }
        msg = json.dumps(json_msg)
        response = requests.post(url,headers = headers,data = msg,timeout = (3,60)).json()
        return response

if __name__ == "__main__":
    msg = 'test'
    phone = [15121111,152222222]
    d1 = DingDing(phone, msg)
    d1.ding_msg()
