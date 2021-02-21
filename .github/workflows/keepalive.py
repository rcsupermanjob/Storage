import asyncio
import json
import time
import os
import httpx
import websockets
import traceback

headers_1 = {
    'authority': 'cdn.jsdelivr.net',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not\\A"Brand";v="99"',
    'sec-ch-ua-mobile': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Mobile Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

headers_2 = {
    'authority': 'www.17ce.com',
    'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not\\A"Brand";v="99"',
    'accept': '*/*',
    'x-requested-with': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?1',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Mobile Safari/537.36',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://www.17ce.com',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.17ce.com/',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8', }


async def connect_17ce(wss_url, source_url):
    async with websockets.connect(wss_url) as websocket:
        login_text = await websocket.recv()
        login_json = json.loads(login_text)
        if login_json['msg'] == 'login ok':
            print(source_url, 'start 17ce')
        else:
            print(source_url, 'login failed')
        data = {
            'AutoDecompress': False,
            'Cookie': "",
            'FollowLocation': 3,
            'GetMD5': True,
            'GetResponseHeader': True,
            'Host': "",
            'MaxDown': 1048576,
            'NoCache': False,
            'PingCount': 10,
            'PingSize': 32,
            'Referer': "",
            'Request': "GET",
            'SnapShot': False,
            'Speed': 0,
            'SrcIP': "",
            'TestType': "CDN",
            'TimeOut': 10,
            'Trace': False,
            'Url': source_url,
            'UserAgent': "",
            'areas': [0, 1, 2, 3],
            'isps': [0, 1, 2, 6, 7, 8, 17, 18, 19, 3, 4],
            'nodetype': [1, 2],
            'num': 2,
            'postfield': "",
            'pro_ids': [12, 49, 79, 80, 180, 183, 184, 188, 189, 190, 192, 193, 194, 195, 196, 221, 227, 235, 236, 238,
                        241, 243, 250, 346, 349, 350, 351, 353, 354, 355, 356, 357, 239, 352, 3, 5, 8, 18, 27, 42, 43,
                        46, 47, 51, 56, 85],
            'txnid': 1,
            'type': 1,
        }
        await websocket.send(json.dumps(data))
        while True:
            recv_text = await websocket.recv()
            recv_json = json.loads(recv_text)
            print(recv_json)
            if recv_json['type'] == 'TaskEnd':
                print(source_url, 'finish 17ce')
                break
            if recv_json['type']  == 'TaskErr':
                break


def request(filename):
    try:
        for _ in range(3):
            url_1 = 'https://cdn.jsdelivr.net/gh/rcsupermanjob/Storage@latest/' + filename
            response = client.get(url_1, headers=headers_1)
            print(url_1, response.status_code, f'{len(response.content) / 8 / 1024} KB')
            url_2 = "https://www.17ce.com/site/checkuser"
            payload = {
                'url': url_1,
                'type': 'cdn',
                'isp': 0
            }
            response = client.post(url_2, headers=headers_2, data=payload).json()
            if response['rt']:
                ut = response['data']['ut']
                code = response['data']['code']
                asyncio.get_event_loop().run_until_complete(
                    connect_17ce(f'wss://wsapi.17ce.com:8001/socket/?user=yiqice@qq.com&code={code}&ut={ut}', url_1))
            else:
                print(url_1, 'cant request 17ce')
            time.sleep(5)
    except Exception as e:
        traceback.print_exc()

client = httpx.Client()
for path, dir_list, file_list in os.walk("."):
    if path != '.git' or path != './github':
        for file_name in file_list:
            request(os.path.join(path, file_name)[2:])
