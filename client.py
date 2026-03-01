import requests
import subprocess
import asyncio
import os
import time

async def main():
    await run_exe()
    
    
async def run_exe():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    exe_path = os.path.join(base_dir, "proxypunch.win64.exe")

    process = await asyncio.create_subprocess_exec(
        exe_path,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    # 標準出力を1行ずつ監視
    while True:
        line = await process.stdout.readline()
        if not line:
            break
        decoded_line = line.decode().rstrip()
        print("stdout:", decoded_line)

        # 特定の文字列が出たら関数呼び出し
        if "Ask your peer to connect to " in decoded_line:
            await on_ready()

    # 標準エラーも読み取り（必要なら）
    err = await process.stderr.read()
    if err:
        print("stderr:", err.decode().rstrip())

    return_code = await process.wait()
    print("終了コード:", return_code)

# 条件が満たされたとき呼ばれる関数
async def on_ready():
    print("READY が出力されました！別処理を実行します。")
    # 例：HTTPリクエストを送る
    # await sendtext("READYが出ました")

def sendtext(text):
    url = "https://shinkirou-server.onrender.com/echo"

    payload = {'text':text}

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        data = response.json()
        print("response:",data['response'])
    else:
        print("fuck")

if __name__ == "__main__":
    asyncio.run(main())
    input("終了しました。Enterキーで閉じます...")


