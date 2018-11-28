import requests
import time
import random
from functools import partial
import asyncio
import argparse
import json
import threading
import ctypes
import struct
import socket
from datetime import datetime


#                                  名称                                id    票数  涨幅  平均每秒涨幅  与第一名差距
# 0              镇江市公共交通有限公司  a3a97dbd743f4e79a5e7248b47b19be3  232271     3          0.13             0
# 1                镇江华润燃气有限公司  cc3a48cfd527468a95791c762009950b  218265     3          0.12         14006
# 2                  中国移动镇江分公司  ccc0bc4fe4f942ac85d0a3c92667fe3a  195620     2          0.10         36651
# 3                    国网镇江供电公司  235ee61c3a514f7c9c59944753f2e03c  190160     3          0.10         42111
# 4                    镇江江天汽运集团  b38a56888c714f8fa672389e43acccd9  150680     3          0.11         81591
# 5                  中国联通镇江分公司  bdcd6c454531422dad62d61ea74d9029  129752     3          0.11        102519
# 6            中化道达尔镇江南徐加油站  0be041598e49485fb17e0f09d353c729  125888     4          0.10        106383
# 7                中石化镇江石油分公司  373e4cbf1b13459a933fb7ab24b12141  123926     4          0.10        108345
# 8                  江苏有线镇江分公司  57bf803aab9841bbbc7c5de47051e24a  123651     3          0.11        108620
# 9                  中国石油镇江分公司  173902f21dd644adbc264768991856d6  123096     3          0.09        109175
# 10                 中国电信镇江分公司  c492d45766ab4592a724c62303e22191  117402     3          0.43        114869
# 11   中国铁路上海局集团有限公司镇江站  66f1ec2a152843eab84db99c89206f70  115358     3          0.11        116913
# 12                   镇江市自来水公司  63ac022e185544e09442db014acb3a13  115300     3          0.11        116971
# 13             中国邮政集团镇江分公司  d05d6f2cb1ad41849e5469ac42a9fd25  113967     6          0.45        118304


def get_ip_list():
    a = []
    a.extend(list(range(ctypes.c_uint32(607649792).value, ctypes.c_uint32(608174079).value))),  # 36.56.0.0-36.63.255.255
    a.extend(list(range(ctypes.c_uint32(1038614528).value, ctypes.c_uint32(1039007743).value))),  # 61.232.0.0-61.237.255.255
    a.extend(list(range(ctypes.c_uint32(1783627776).value, ctypes.c_uint32(1784676351).value))),  # 106.80.0.0-106.95.255.255
    a.extend(list(range(ctypes.c_uint32(2035023872).value, ctypes.c_uint32(2035154943).value))),  # 121.76.0.0-121.77.255.255
    a.extend(list(range(ctypes.c_uint32(2078801920).value, ctypes.c_uint32(2079064063).value))),  # 123.232.0.0-123.235.255.255
    a.extend(list(range(ctypes.c_uint32(-1950089216).value, ctypes.c_uint32(-1948778497).value))),  # 139.196.0.0-139.215.255.255
    a.extend(list(range(ctypes.c_uint32(-1425539072).value, ctypes.c_uint32(-1425014785).value))),  # 171.8.0.0-171.15.255.255
    a.extend(list(range(ctypes.c_uint32(-1236271104).value, ctypes.c_uint32(-1235419137).value))),  # 182.80.0.0-182.92.255.255
    a.extend(list(range(ctypes.c_uint32(-770113536).value, ctypes.c_uint32(-768606209).value))),  # 210.25.0.0-210.47.255.255
    a.extend(list(range(ctypes.c_uint32(-569376768).value, ctypes.c_uint32(-564133889).value))),  # 222.16.0.0-222.95.255.255
    return a


ip_list = get_ip_list()


def make_proxy():
    # 代理服务器
    proxyHost = "http-dyn.abuyun.com"
    proxyPort = "9020"

    # 代理隧道验证信息
    proxyUser = "H5F9YXW56V5Q107D"
    proxyPass = "9340E6B100E48DF7"

    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host" : proxyHost,
    "port" : proxyPort,
    "user" : proxyUser,
    "pass" : proxyPass,
    }

    proxies = {
        "http"  : proxyMeta,
        "https" : proxyMeta,
    }
    return proxies


def get_id_list():
    url = "https://api.17zhenjiang.com/yqzj/external/externalService?service=voteOptionTop&params={%22voteId%22:%22vote_5590c73f277347fcb4edcbc0554d2497%22,%20%22themeId%22:%22ff80808166d2fe760166ece1de5c021e%22,%20%22page%22:%221%22,%20%22rows%22:%2220%22}"
    response = requests.get(url, proxies=make_proxy())
    content = json.loads(response.content.decode('utf8'))
    id_list = list(map(lambda x: {
        "title": x['title'],
        "id": str(x['id']),
        "voteNumber": str(x['voteNumber'])
    }, content['data']['rows']))
    for id_item in id_list:
        if id_item["title"] == "镇江市公共交通有限公司":
            break
    return id_list[3:], id_item


# to_vote_id_list, zj_id = get_id_list()
zj_id = {
    "title": "镇江市公共交通有限公司",
    "id": "a3a97dbd743f4e79a5e7248b47b19be3"
}


def get_rank(p):
    url = "https://api.17zhenjiang.com/yqzj/external/externalService?service=voteOptionTop&params={%22voteId%22:%22vote_5590c73f277347fcb4edcbc0554d2497%22,%20%22themeId%22:%22ff80808166d2fe760166ece1de5c021e%22,%20%22page%22:%221%22,%20%22rows%22:%2220%22}"
    try:
        if p:
            response = requests.get(url, proxies=make_proxy())
        else:
            response = requests.get(url)
        content = json.loads(response.content.decode('utf8'))
    except Exception:
        return None
    rank_dict = {}
    for i, x in enumerate(content['data']['rows']):
        rank_dict[x['title']] = {
            "rank": i + 1,
            "title": x['title'],
            "id": str(x['id']),
            "voteNumber": str(x['voteNumber'])
        }
    return rank_dict


def random_imei():
    return '%030x' % random.randrange(16**32)


def random_phone():
    a = [1, 8, 3]
    a.extend([random.randint(0, 9) for i in range(8)])
    return ''.join(map(str, a))


def random_ip():
    return socket.inet_ntoa(struct.pack('>I', random.choice(ip_list)))


def make_url(vote0, vote1, vote2):
    imei = random_imei()
    phone = random_phone()
    url = ("https://api.17zhenjiang.com/yqzj/external/externalService?service=doVote&params="
           "{"
           "%22voteId%22:%22vote_5590c73f277347fcb4edcbc0554d2497%22,"
           "%22voteType%22:%221%22,"
           "%22token%22:%22affc793103274d30a7eea11efc2acbd2%22,"
          f"%22phone%22:%22{phone}%22,"
           "%22yzm%22:%22%22,"
          f"%22imei%22:%22{imei}%22,"
           "%22player%22:["
           "{"
           "%22themeId%22:%22ff80808166d2fe760166ece1de5c021e%22,"
           "%22playerIds%22:["
          f"%22{vote0['id']}%22,"
          f"%22{vote1['id']}%22,"
          f"%22{vote2['id']}%22"
           "],"
           "%22mustOf%22:1,"
           "%22titleName%22:%22%E9%95%87%E6%B1%9F%E5%B8%822018%E5%B9%B4%E6%B6%88%E8%B4%B9%E7%83%AD%E7%82%B9%E8%AF%84%E8%AE%AE%E6%8A%95%E7%A5%A8%22,"
           "%22minOptions%22:3,"
           "%22radioChex%22:1"
           "}]}")
    return url


def make_headers():
    ip = random_ip()
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
        'CLIENT-IP': ip,
        'X-FORWARDED-FOR': ip
    }
    return headers


def send_vote(i, vote0, vote1, vote2, p):
    try:
        start = time.time()
        headers = make_headers()
        url = make_url(vote0, vote1, vote2)
        if p:
            response = requests.get(url, headers=headers, proxies=make_proxy())
        else:
            response = requests.get(url, headers=headers)
        end = time.time()
        result = json.loads(response.text)
        print(f"第{i}票：{result['message']} 耗时{end-start:.3f}秒")
    except Exception:
        print(f"第{i}票：超时")


def vote(i, p):
    vote0 = zj_id
    # vote1, vote2 = random.sample(to_vote_id_list, 2)
    threading.Thread(target=send_vote, args=(i, vote0, vote0, vote0, p)).start()


async def vote_forever(gap, p):
    i = 0
    while True:
        i += 1
        loop.call_soon(vote, i, p)
        await asyncio.sleep(random.uniform(gap * 0.8, gap * 1.2))


async def vote_in_range(seconds, vote_num):
    multi = 1
    while vote_num > seconds * multi:
        multi *= 10
    multi *= 10
    time_list = list(range(int(seconds * multi)))
    vote_time = sorted(random.sample(time_list, vote_num))
    vote_gap = list(map(lambda x, y: (y - x) / multi, vote_time[:-1], vote_time[1:]))
    for i, gap in enumerate(vote_gap):
        loop.call_soon(vote, i+1)
        print(f"sleep {gap}")
        await asyncio.sleep(gap)
    loop.call_soon(vote, i+2)


async def monitor_vote(minus, p):
    target_name = "镇江市公共交通有限公司"
    vote_id = 1
    while True:
        rank_dict = get_rank(p)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if rank_dict is not None:
            target = rank_dict[target_name]
            if target["rank"] == 1:
                minus_to_2 = int(target["voteNumber"]) - int(list(rank_dict.values())[1]["voteNumber"])
                if minus_to_2 > minus:
                    print(f"{now} 与第二名差距{minus_to_2}票，不需要投票")
                else:
                    print(f"{now} 与第二名差距{minus_to_2}票，投票{minus - minus_to_2}")
                    for vote_id in range(vote_id, vote_id + (minus - minus_to_2) // 3):
                        vote(vote_id, p)
                        await asyncio.sleep(0.1)
            elif target["rank"] != 1:
                minus_to_1 = int(list(rank_dict.values())[0]["voteNumber"]) - int(target["voteNumber"])
                print(f"{now} 与第一名差距{minus_to_1}票，投票{minus_to_1 + minus}")
                for vote_id in range(vote_id, vote_id + (minus_to_1 + minus) // 3):
                    vote(vote_id, p)
                    await asyncio.sleep(0.1)
        else:
            print(f"{now} 获取投票信息失败!")
        await asyncio.sleep(3)


async def start_vote(p):
    # if v == 0:
        # await vote_forever(t)
    # else:
        # await vote_in_range(t, v)
    # await vote_forever(1, p)
    await monitor_vote(14000, p)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--p', default='True', type=str)
    args = parser.parse_args()
    print(args.p)
    loop.run_until_complete(start_vote(bool(args.p)))
    loop.close()


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    main()
