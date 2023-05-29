import os
import random
import time
import requests

default_dir = "data/electricity/"

url="https://api.oioweb.cn/api/qq/nickname"

def getMeg():
    msg_list = os.listdir(default_dir)
    select = random.randint(0, len(msg_list) - 1)
    offer = msg_list[select].split("_")[0]
    raw_datetime = msg_list[select].split("_")[1]
    datetime = raw_datetime[:4] + "/" + raw_datetime[4:6] + "/" + raw_datetime[6:8] + \
               " " + raw_datetime[8:10] + ":" + raw_datetime[10:12] + ":" + raw_datetime[12:14]
    param = {
        "qq": offer
    }
    qq_info=requests.get(url=url, params=param).json()['result']
    with open(default_dir + msg_list[select], "r", encoding='utf-8') as f:
        return qq_info['nickname'], qq_info['qlogo'], datetime, f.read()


def setMsg(offer, msg):
    localtime = time.localtime()
    datetime = str(localtime.tm_year).rjust(4, '0') + str(localtime.tm_mon).rjust(2, '0') \
               + str(localtime.tm_mday).rjust(2, '0') + str(localtime.tm_hour).rjust(2, '0') \
               + str(localtime.tm_min).rjust(2, '0') + str(localtime.tm_sec).rjust(2, '0')
    with open(default_dir + "_".join([offer, datetime]) + ".txt", "w", encoding='utf-8') as f:
        f.write(msg)
