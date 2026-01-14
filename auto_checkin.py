import requests
import json

# 签到接口地址
url = "https://69yun69.com/user/checkin"

# 请求头配置
headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Content-Length": "0",
    "Cookie": (
        "uid=46718;"
        "email=itsansui%40163.com;"
        "key=48322f39d732f0853849d849d3c10ab5aba424c069040;"
        "ip=ea0598694f02eac214bb036055d6846b;"
        "expire_in=1768959185;"
        "PHPSESSID=j4rpcvijr4m38kgnr1ek7n96vo;"
        "mtauth=554aa904a2edc0129b208072c2d4e677;"
        "pop=yes"
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
try:
    # 发送POST请求完成签到（请求体为空）
    response = requests.post(url, headers=headers, timeout=30)
    text = response.text
    data = response.json()

    ret = data.get("ret")
    msg = data.get("msg")
    
    # 发送手机通知（修正语法错误，使用英文引号和合法变量名）
    response_phone = requests.get(
        f"https://api.day.app/w7JBm2Rx34tcBvSvznpTUT/{msg}?icon=https://compus-store-oss.oss-cn-beijing.aliyuncs.com/sansui_ai.jpg",
        headers=headers,
        timeout=30
    )

    # 解析并打印响应内容（优化格式，避免解析失败报错）
    try:
        data = json.loads(text)
        print("状态码:", response.status_code)
        print("响应内容:", json.dumps(data, ensure_ascii=False, indent=2))
    except json.JSONDecodeError:
        print("状态码:", response.status_code)
        print("响应内容（非JSON格式）:", text)

except Exception as e:
    print(f"脚本运行异常: {str(e)}")
    # 异常时发送失败通知
    try:
        requests.get(
            f"https://api.day.app/w7JBm2Rx34tcBvSvznpTUT/脚本运行异常：{str(e)}?icon=https://compus-store-oss.oss-cn-beijing.aliyuncs.com/sansui_ai.jpg",
            headers=headers,
            timeout=30
        )
    except:
        pass





