import requests
import json
import time
import os
import pandas as pd
from io import StringIO
from datetime import datetime


pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)


def get_rank():
    url = "https://api.17zhenjiang.com/yqzj/external/externalService?service=voteOptionTop&params={%22voteId%22:%22vote_5590c73f277347fcb4edcbc0554d2497%22,%20%22themeId%22:%22ff80808166d2fe760166ece1de5c021e%22,%20%22page%22:%221%22,%20%22rows%22:%2220%22}"
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
    try:
        response = requests.get(url, proxies=proxies)
        content = json.loads(response.content.decode('utf8'))
    except Exception:
        return []
    rank_list = list(map(lambda x: {
        "title": x['title'],
        "id": str(x['id']),
        "voteNumber": str(x['voteNumber'])
    }, content['data']['rows']))
    return rank_list


def main():
    vote_info = {}
    while True:
        rank_list = get_rank()
        if len(rank_list) > 0:
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            now = time.time()
            os.system("cls")
            csv_content = ["名称,id,票数,涨幅,平均每秒涨幅,与第一名差距"]
            for item in rank_list:
                minus = 0
                avg_minus = 0
                if item['title'] in vote_info:
                    minus = int(item['voteNumber']) - int(vote_info[item['title']]["last_vote"])
                    avg_minus = (int(item['voteNumber']) - int(vote_info[item['title']]['start_vote_number'])) / (now - vote_info[item['title']]['start_time'])
                    vote_info[item['title']]['last_vote'] = item['voteNumber']
                else:
                    vote_info[item['title']] = {
                        'start_vote_number': item['voteNumber'],
                        'start_time': now,
                        'last_vote': item['voteNumber']
                    }

                item["minus"] = str(minus)
                item["avg_minus"] = f'{avg_minus:.2f}'
                item["to_no1"] = str(int(rank_list[0]['voteNumber']) - int(item['voteNumber']))
                csv_content.append(','.join(item.values()))
            df = pd.read_csv(StringIO('\n'.join(csv_content)))
            print(now_str)
            print(df)
        time.sleep(1)


if __name__ == '__main__':
    main()
