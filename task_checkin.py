import requests
import json
import schedule
import time
from datetime import datetime

def checkin():
    """核心签到函数，执行具体签到逻辑，增加详细日志"""
    url = "https://69yun69.com/user/checkin"

    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Content-Length": "0",
        "Cookie": "uid=46718; email=itsansui%40163.com; key=xxx;",  # 替换为有效Cookie
        "Origin": "https://69yun69.com",
        "Referer": "https://69yun69.com/user",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }

    try:
        # 发送签到POST请求，设置超时时间
        response = requests.post(url, headers=headers, timeout=30)
        data = response.json()

        # 打印格式化日志，方便排查
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("-" * 60)
        print(f"【签到日志】执行时间：{current_time}")
        print(f"【签到日志】响应状态码：{response.status_code}")
        print(f"【签到日志】响应内容：{json.dumps(data, ensure_ascii=False, indent=2)}")
        print("-" * 60)
    
    except requests.exceptions.RequestException as e:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("-" * 60)
        print(f"【签到日志】执行时间：{current_time}")
        print(f"【签到日志】错误类型：网络请求失败")
        print(f"【签到日志】错误详情：{str(e)}")
        print("-" * 60)
    except json.JSONDecodeError:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("-" * 60)
        print(f"【签到日志】执行时间：{current_time}")
        print(f"【签到日志】错误类型：响应数据非JSON格式")
        print(f"【签到日志】原始响应：{response.text if 'response' in locals() else '无响应对象'}")
        print("-" * 60)
    except Exception as e:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("-" * 60)
        print(f"【签到日志】执行时间：{current_time}")
        print(f"【签到日志】错误类型：未知异常")
        print(f"【签到日志】错误详情：{str(e)}")
        print("-" * 60)
# 初始化签到消息
    msg = "签到失败"
    if response.status_code == 200:
        msg = "定时task签到成功！"

    # 发送手机通知（修正语法错误，使用英文引号和合法变量名）
    response_phone = requests.get(
        f"https://api.day.app/w7JBm2Rx34tcBvSvznpTUT/{msg}",
        headers=headers,
        timeout=30
    )
# 配置脚本内部定时：每天05:00执行签到（不依赖任何云端定时）
schedule.every().day.at("05:00").do(checkin)

# 启动无限循环，持续监听定时任务（长期运行核心逻辑）
if __name__ == "__main__":
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("=" * 60)
    print(f"【启动日志】签到服务已启动，启动时间：{start_time}")
    print(f"【启动日志】定时规则：每天05:00自动执行签到")
    print(f"【启动日志】服务状态：持续运行中，关闭进程可终止服务")
    print(f"【启动日志】注意：云端运行仅支持6小时内任务，长期运行请部署到本地/云服务器")
    print("=" * 60)
    
    while True:
        schedule.run_pending()  # 检查是否有到期任务需要执行
        time.sleep(30)  # 每30秒检查一次，降低资源占用
