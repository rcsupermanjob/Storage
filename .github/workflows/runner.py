import asyncio
import json
import os
import random
import sys
import traceback
from datetime import datetime

import httpx
import parse
import websockets
import httpcore


async def task_17ce(filename, sem):
    try:
        await sem.acquire()
        await asyncio.sleep(random.randint(1, 5))
        async with httpx.AsyncClient(timeout=90) as client:
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
            response = await client.post(url=url, headers=headers, data=payload)
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
                print(datetime.utcnow(), filename,
                      'cant request 17ce', response)
    except httpcore.CloseError:
        print(datetime.utcnow(), filename, '17ce too fast')
    except (httpx.ReadTimeout, httpx.ConnectTimeout):
        print(datetime.utcnow(), filename, '17ce timeout')
    except Exception as e:
        traceback.print_exc()
    finally:
        await asyncio.sleep(random.randint(1, 5))
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
            response = await client.get(url=url, headers=headers)
            print(datetime.utcnow(), url, response.status_code,
                  f'{len(response.content) / 8 / 1024} KB')
    except httpcore.CloseError:
        print(datetime.utcnow(), filename, 'jsdelivr too fast')
    except (httpx.ReadTimeout, httpx.ConnectTimeout):
        print(datetime.utcnow(), filename, 'jsdelivr timeout')
    except Exception as e:
        traceback.print_exc()
    finally:
        await asyncio.sleep(1)


async def task_ce8(filename, sem):
    try:
        await sem.acquire()
        await asyncio.sleep(random.randint(1, 5))
        async with httpx.AsyncClient(timeout=90) as client:
            url = 'https://www.ce8.com/http/https://cdn.jsdelivr.net/gh/rcsupermanjob/Storage@latest/' + filename
            params = {
                'isp': 'telecom_mobile_unicom_tt_edu_mix'
            }
            headers = {
                'Connection': 'keep-alive',
                'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not\\A"Brand";v="99"',
                'sec-ch-ua-mobile': '?1',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Mobile Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-User': '?1',
                'Sec-Fetch-Dest': 'document',
                'Referer': url,
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            }
            response = await client.get(url=url, headers=headers, params=params)
            response = response.text
            token = parse.search('var token = "{}"', response)
            if token:
                print(datetime.utcnow(), filename, 'ce8 start')
                url = 'https://check1.ce8.com/api/check/site_all'
                headers = {
                    'Connection': 'keep-alive',
                    'Accept': '*/*',
                    'Access-Control-Request-Method': 'POST',
                    'Access-Control-Request-Headers': 'content-type',
                    'Origin': 'https://www.ce8.com',
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Mobile Safari/537.36',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Site': 'same-site',
                    'Sec-Fetch-Dest': 'empty',
                    'Referer': 'https://www.ce8.com/',
                    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
                }
                await client.options(url=url, headers=headers)
                data = {
                    'token': token[0],
                    'url': 'https://cdn.jsdelivr.net/gh/rcsupermanjob/Storage@latest/' + filename
                }
                headers = {
                    'Connection': 'keep-alive',
                    'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not\\A"Brand";v="99"',
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'sec-ch-ua-mobile': '?1',
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Mobile Safari/537.36',
                    'Content-Type': 'application/json; charset=UTF-8',
                    'Origin': 'https://www.ce8.com',
                    'Sec-Fetch-Site': 'same-site',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Dest': 'empty',
                    'Referer': 'https://www.ce8.com/',
                    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
                }
                count = 3
                while count > 0:
                    response = await client.post(url=url, headers=headers, json=data)
                    response = response.json()
                    count -= 1
                    await asyncio.sleep(20)
                    if 'data' in response and response['data']:
                        if len(response['data']) > 0:
                            print(datetime.utcnow(), filename, 'ce8 finish')
                            break
                        else:
                            print(datetime.utcnow(), filename, 'ce8 data null')
                    else:
                        print(datetime.utcnow(), filename, 'ce8 result failed')
            else:
                print(datetime.utcnow(), filename, 'ce8 token failed')
    except httpcore.CloseError:
        print(datetime.utcnow(), filename, 'ce8 too fast')
    except (httpx.ReadTimeout, httpx.ConnectTimeout):
        print(datetime.utcnow(), filename, 'ce8 timeout')
    except Exception as e:
        traceback.print_exc()
    finally:
        await asyncio.sleep(random.randint(1, 5))
        sem.release()


async def task_chinaz(filename, sem):
    try:
        await sem.acquire()
        await asyncio.sleep(random.randint(1, 5))
        async with httpx.AsyncClient(timeout=90) as client:
            url = 'http://tool.chinaz.com/speedtest/https://cdn.jsdelivr.net/gh/rcsupermanjob/Storage@latest/' + filename
            data = {
                'host': 'https://cdn.jsdelivr.net/gh/rcsupermanjob/Storage@latest/' + filename,
                'linetype': '电信,多线,联通,移动'
            }
            headers = {
                'Proxy-Connection': 'keep-alive',
                'Cache-Control': 'max-age=0',
                'Upgrade-Insecure-Requests': '1',
                'Origin': 'http://tool.chinaz.com',
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Mobile Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Referer': url,
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
            }
            response = httpx.post(url, headers=headers, data=data).text.replace('\n', '').replace('\r', '').replace(' ',
                                                                                                                    '')
            enkey = parse.search('id="enkey"value="{}"', response)
            guids = parse.findall(
                'divid="{}"class="rowlistwclearfix"', response)
            if enkey and guids:
                print(datetime.utcnow(), filename, 'chinaz start')
                tasks = list()
                for guid in guids:
                    url = 'http://tool.chinaz.com/iframe.ashx?t=ping&callback='
                    headers = {
                        'Proxy-Connection': 'keep-alive',
                        'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
                        'X-Requested-With': 'XMLHttpRequest',
                        'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1',
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'Origin': 'http://tool.chinaz.com',
                        'Referer': 'http://tool.chinaz.com/speedtest/https://cdn.jsdelivr.net/gh/rcsupermanjob/Storage@latest/' + filename,
                        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
                    }
                    data = {
                        'guid': guid[0],
                        'host': 'https://cdn.jsdelivr.net/gh/rcsupermanjob/Storage@latest/' + filename,
                        'ishost': 1,
                        'isipv6': None,
                        'encode': enkey[0],
                        'checktype': 1
                    }
                    tasks.append(client.post(url, headers=headers, data=data))
                await asyncio.gather(*tasks)
                print(datetime.utcnow(), filename, 'chinaz finish')
            else:
                print(datetime.utcnow(), filename, 'chinaz enkey or guids failed')
    except httpcore.CloseError:
        print(datetime.utcnow(), filename, 'chinaz too fast')
    except (httpx.ReadTimeout, httpx.ConnectTimeout):
        print(datetime.utcnow(), filename, 'chinaz timeout')
    except Exception as e:
        traceback.print_exc()
    finally:
        await asyncio.sleep(random.randint(10, 20))
        sem.release()


async def create_task():
    tasks = []
    sem = asyncio.Semaphore(5)
    if len(sys.argv) == 1:
        for path, _, file_list in os.walk("."):
            if path.startswith('./.git') or path.startswith('./.github'):
                continue
            else:
                for file_name in file_list:
                    # tasks.append(task_17ce(os.path.join(path, file_name)[2:], sem))
                    tasks.append(
                        task_ce8(os.path.join(path, file_name)[2:], sem))
                    tasks.append(task_jsdelivr(
                        os.path.join(path, file_name)[2:]))
                    tasks.append(task_chinaz(
                        os.path.join(path, file_name)[2:], sem))
    elif len(sys.argv) > 1:
        for file_name in sys.argv[1:]:
            if file_name.startswith('.git') or file_name.startswith('.github'):
                continue
            else:
                # tasks.append(task_17ce(file_name, sem))
                tasks.append(task_ce8(file_name, sem))
                tasks.append(task_jsdelivr(file_name))
                tasks.append(task_chinaz(file_name, sem))
    random.shuffle(tasks)
    await asyncio.gather(*tasks)


loop = asyncio.get_event_loop()
loop.run_until_complete(create_task())
