import requests
import json
import schedule
import time

def checkin():
    url = "https://69yun69.com/user/checkin"

    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Content-Length": "0",
        "Cookie": "uid=46718; email=itsansui%40163.com; key=xxx;",
        "Origin": "https://69yun69.com",
        "Referer": "https://69yun69.com/user",
        "User-Agent": "Mozilla/5.0",
        "X-Requested-With": "XMLHttpRequest"
    }

    response = requests.post(url, headers=headers)
    data = response.json()

    print("状态码:", response.status_code)
    print(json.dumps(data, ensure_ascii=False, indent=2))


# 每天 05:00 执行
schedule.every().day.at("05:00").do(checkin)

print("签到任务已启动，等待 05:00 执行...")

while True:
    schedule.run_pending()
    time.sleep(30)
