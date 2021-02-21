import asyncio
import json
import time
from datetime import datetime
import os
import httpx
import websockets
import traceback


async def task_17ce(filename, sem):
    try:
        await sem.acquire()
        url = "https://www.17ce.com/site/checkuser"
        headers = {
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
        payload = {
            'url': 'https://cdn.jsdelivr.net/gh/rcsupermanjob/Storage@latest/' + filename,
            'type': 'cdn',
            'isp': 0
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, data=payload)
            response = response.json()
            if response['rt']:
                ut = response['data']['ut']
                code = response['data']['code']
                websocket = await websockets.connect(
                    f'wss://wsapi.17ce.com:8001/socket/?user=yiqice@qq.com&code={code}&ut={ut}')
                login_text = await websocket.recv()
                login_json = json.loads(login_text)
                if login_json['msg'] == 'login ok':
                    print(datetime.utcnow(), filename, 'start 17ce')
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
                        'Url': 'https://cdn.jsdelivr.net/gh/rcsupermanjob/Storage@latest/' + filename,
                        'UserAgent': "",
                        'areas': [0, 1, 2, 3],
                        'isps': [0, 1, 2, 6, 7, 8, 17, 18, 19, 3, 4],
                        'nodetype': [1, 2],
                        'num': 2,
                        'postfield': "",
                        'pro_ids': [12, 49, 79, 80, 180, 183, 184, 188, 189, 190, 192, 193, 194, 195, 196, 221, 227,
                                    235,
                                    236, 238,
                                    241, 243, 250, 346, 349, 350, 351, 353, 354, 355, 356, 357, 239, 352, 3, 5, 8, 18,
                                    27,
                                    42, 43,
                                    46, 47, 51, 56, 85],
                        'txnid': 1,
                        'type': 1,
                    }
                    await websocket.send(json.dumps(data))
                    while True:
                        recv_text = await websocket.recv()
                        recv_json = json.loads(recv_text)
                        if recv_json['type'] == 'TaskEnd':
                            print(datetime.utcnow(), filename, 'finish 17ce')
                            break
                        if recv_json['type'] == 'TaskErr':
                            break
                        if recv_json['type'] == 'NewData':
                            continue
                else:
                    print(datetime.utcnow(), filename, 'login failed')
            else:
                print(datetime.utcnow(), filename, 'cant request 17ce')
    except Exception as e:
        traceback.print_exc()
    finally:
        sem.release()


async def task_jsdelivr(filename):
    try:
        async with httpx.AsyncClient() as client:
            url = 'https://cdn.jsdelivr.net/gh/rcsupermanjob/Storage@latest/' + filename
            headers = {
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
            response = await client.get(url, headers=headers)
            print(datetime.utcnow(), url, response.status_code, f'{len(response.content) / 8 / 1024} KB')
    except Exception as e:
        traceback.print_exc()
    finally:
        await asyncio.sleep(1)


async def create_task():
    tasks = []
    sem = asyncio.Semaphore(3)
    for path, dir_list, file_list in os.walk("."):
        if path.startswith('./.git') or path.startswith('./.github'):
            continue
        else:
            for file_name in file_list:
                for _ in range(2):
                    tasks.append(task_17ce(os.path.join(path, file_name)[2:], sem))
                    tasks.append(task_jsdelivr(os.path.join(path, file_name)[2:]))
                tasks.append(asyncio.sleep(3))
    await asyncio.gather(*tasks)


loop = asyncio.get_event_loop()
loop.run_until_complete(create_task())
