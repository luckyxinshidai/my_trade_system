# coding:utf-8
import requests
import json
# import threading
import time
import os




def get_token():
    url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
    values = {'corpid': 'ww246ac5d0385cf007',
              'corpsecret': 'gZxN8qODLYllRCt3sO7GofNIY4Lm3jvb-urWkpacu14',
              }
    req = requests.post(url, params=values)
    data = json.loads(req.text)
    return data["access_token"]


def send_msg(to_send_str):
    url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + get_token()
    values = """{"touser" : "ZhaoShiJie" ,
      "toparty":"1",
      "msgtype":"text",
      "agentid":"1000002",
      "text":{
        "content": "%s"
      },
      "safe":"0"
      }""" % to_send_str

    data = json.loads(values)
    req = requests.post(url, values)


def func_timer():
    old_time = 0
    while 1:
        temp_time_2 = time.time()
        now_time = time.localtime()
        now_time_str = time.strftime("%H %M", now_time)
        now_time_str = now_time_str.split(' ')
        hour = now_time_str[0]
        minute = now_time_str[1]
        if hour == '21' and minute == '47':
            send_msg(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(temp_time_2)))
            exit()
        if temp_time_2 - old_time > 30:
            old_time = temp_time_2
            send_msg(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(old_time)))


if __name__ == '__main__':
    try:
        func_timer()
    except SystemExit:
        send_msg("我将要退出了")
    finally:
        send_msg("受保护的退出")
    # send_msg()
