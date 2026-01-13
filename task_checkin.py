import requests
import json
import schedule
import time

def checkin():
    """核心签到函数，执行具体的签到逻辑"""
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
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }

    try:
        # 发送签到POST请求，设置超时时间避免无限等待
        response = requests.post(url, headers=headers, timeout=30)
        # 解析JSON响应数据
        data = response.json()

        # 打印执行结果
        print("="*50)
        print(f"执行时间：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
        print("状态码:", response.status_code)
        print("响应内容:", json.dumps(data, ensure_ascii=False, indent=2))
        print("="*50)
    
    except requests.exceptions.RequestException as e:
        print(f"="*50)
        print(f"执行时间：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
        print(f"网络请求失败：{str(e)}")
        print(f"="*50)
    except json.JSONDecodeError:
        print(f"="*50)
        print(f"执行时间：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
        print("响应内容非JSON格式，原始内容：", response.text)
        print(f"="*50)
    except Exception as e:
        print(f"="*50)
        print(f"执行时间：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
        print(f"未知错误：{str(e)}")
        print(f"="*50)

# 配置定时任务：每天 05:00 执行签到函数
schedule.every().day.at("05:00").do(checkin)

# 启动定时任务循环（持续运行，等待定时触发）
if __name__ == "__main__":
    print("="*50)
    print("签到任务已启动，持续运行中...")
    print(f"定时规则：每天 05:00 执行签到")
    print(f"当前时间：{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
    print("关闭窗口可终止任务")
    print("="*50)
    
    # 无限循环，定期检查是否有任务需要执行
    while True:
        schedule.run_pending()  # 检查并执行到期的任务
        time.sleep(30)  # 每30秒检查一次，降低资源占用
