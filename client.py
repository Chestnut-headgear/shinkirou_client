import requests
import subprocess
import asyncio
import os
import time
import re
import pyperclip
import sys


def getIPaddress(input):
    #sample stdout: Connected. Ask your peer to connect to 219.123.149.209 on port 10800 with proxypunch

    ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'

    matches = re.findall(ip_pattern, input)
    match = matches[0]

    return match 

async def main():
    await check_host()
    await run_exe()
    
async def check_host():
    await get_host_number()
    
async def run_exe():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    exe_path = os.path.join(base_dir, "proxypunch.win64.exe")

    process = await asyncio.create_subprocess_exec(
        exe_path,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    while True:
        line = await process.stdout.readline()
        if not line:
            break
        decoded_line = line.decode().rstrip()
        print("stdout:", decoded_line)

        # 特定の文字列が出たら関数呼び出し
        if "Ask your peer to connect to " in decoded_line:
            await serverIP_send(decoded_line)
        elif "Host? " in decoded_line:
            await serverIP_get()

    return_code = await process.wait()
    print("終了コード:", return_code)


async def get_host_number():
    respond = sendtext("ホストの数よこせ")
    print(respond)


async def serverIP_get():
    respond = sendtext("IPよこせ")
    print(respond)
    opponent = respond.replace("opponent:", "")
    pyperclip.copy(opponent) 


async def serverIP_send(line_with_IP):
    ipaddress = getIPaddress(line_with_IP)
    ipaddress = ipaddress + ":10800"
    print(ipaddress)
    # 例：HTTPリクエストを送る
    sendtext(ipaddress)
    print("プロキシパンチで生成したIPアドレスをサーバーに通知しました、対戦相手を待っています")

def sendtext(text):
    #url = "https://shinkirou-server.onrender.com/echo"
    url = "http://127.0.0.1:5000/echo"

    payload = {'text':text}

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        data = response.json()
        print("response:",data['response'])
        return data['response']
    else:
        print("fuck")
        sys.exit()

if __name__ == "__main__":
    asyncio.run(main())
    input("終了しました。Enterキーで閉じます...")


