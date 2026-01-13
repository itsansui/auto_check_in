import requests
import json
url = "https://69yun69.com/user/checkin"

headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Content-Length": "0",
    "Cookie": (
        "uid=46718; "
        "email=itsansui%40163.com; "
        "key=3239c79ba224ed3502515a4cb274902b6d7868e57ce39; "
        "ip=eb909621fea42d2ae7727743fa1d624c; "
        "expire_in=1768896962; "
        "PHPSESSID=vrnfdsfe1qfjn6t1mknms7lm0a; "
        "mtauth=755ea777d7368ff8d9409553e3721772; "
        "top=yes"
    ),
    "Origin": "https://69yun69.com",
    "Pragma": "no-cache",
    "Priority": "u=1, i",
    "Referer": "https://69yun69.com/user",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "X-Requested-With": "XMLHttpRequest"
}

# POST 请求（请求体为空）
response = requests.post(url, headers=headers)
text = response.text  # 你的 requests 返回内容
msg=“签到失败”
if response.status_code==200:
    msg="签到成功！"
# 通知手机
response——phone = requests.get(f“https://api.day.app/w7JBm2Rx34tcBvSvznpTUT/{msg}”, headers=headers)

data = json.loads(text)
print("状态码:", response.status_code)
print("响应内容:", json.dumps(response.json(), ensure_ascii=False, indent=2))

