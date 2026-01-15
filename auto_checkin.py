import os
import re
import sys
import requests
from urllib.parse import urlencode
# import dotenv
# dotenv.load_dotenv()

# ============================================================
# 配置区（一般只需要改这里）
# ============================================================

# 登录接口地址
LOGIN_URL = "https://69yun69.com/auth/login"

# 签到接口地址
CHECKIN_URL = "https://69yun69.com/user/checkin"

# Bark 推送接口（可通过环境变量覆盖）
PUSH_URL = os.getenv(
    "PUSH_URL",
    "https://api.day.app/w7JBm2Rx34tcBvSvznpTUT"
)

# Bark 推送图标
BARK_ICON = os.getenv(
    "BARK_ICON",
    "https://compus-store-oss.oss-cn-beijing.aliyuncs.com/sansui_ai.jpg"
)

# 登录邮箱（从环境变量读取）
LOGIN_EMAIL = os.getenv("LOGIN_EMAIL", "").strip()

# 登录密码（从环境变量读取）
LOGIN_PASS = os.getenv("LOGIN_PASS", "").strip()

# 登录请求表单数据
LOGIN_PAYLOAD = {
    "email": LOGIN_EMAIL,
    "passwd": LOGIN_PASS,
    "remember_me": "on",
    "code": "",
}

# 登录请求头
LOGIN_HEADERS = {
    "Origin": "https://69yun69.com",
    "Referer": "https://69yun69.com/auth/login",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120 Safari/537.36"
    ),
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept": "application/json, text/javascript, */*; q=0.01",
}

# 签到请求头
CHECKIN_HEADERS = {
    "Origin": "https://69yun69.com",
    "Referer": "https://69yun69.com/user",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120 Safari/537.36"
    ),
    "X-Requested-With": "XMLHttpRequest",
    "Accept": "application/json, text/javascript, */*; q=0.01",
}

# ============================================================
# 启动前检查
# ============================================================

if not LOGIN_EMAIL or not LOGIN_PASS:
    raise SystemExit("【启动失败】缺少 LOGIN_EMAIL 或 LOGIN_PASS 环境变量")

if not PUSH_URL:
    raise SystemExit("【启动失败】缺少 PUSH_URL 环境变量")


# ============================================================
# Bark 推送工具
# ============================================================

class PushClient:
    """Bark URL 构建器"""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self._path_parts = []
        self._query = {}

    def add_path(self, *parts: str):
        for p in parts:
            if p:
                self._path_parts.append(p.strip("/"))
        return self

    def add_query(self, **params):
        for k, v in params.items():
            if v is not None:
                self._query[k] = v
        return self

    def build(self) -> str:
        path = "/".join(self._path_parts)
        url = f"{self.base_url}/{path}" if path else self.base_url
        if self._query:
            url = f"{url}?{urlencode(self._query)}"
        return url


def send_push(
    session: requests.Session,
    title: str,
    body: str = "",
    icon: str = BARK_ICON
):
    """发送 Bark 推送"""
    url = (
        PushClient(PUSH_URL)
        .add_path(title, body)
        .add_query(icon=icon)
        .build()
    )
    session.get(url)


# ============================================================
# HTTP 工具函数
# ============================================================

def post_json(session: requests.Session, url: str, **kwargs):
    """POST 请求并解析 JSON"""
    resp = session.post(url, **kwargs)
    try:
        data = resp.json()
    except ValueError:
        snippet = resp.text[:80]
        raise RuntimeError(f"服务器返回非 JSON 内容：{snippet}")
    return resp, data


# ============================================================
# 主流程：登录 → 签到
# ============================================================

with requests.Session() as s:

    # -------------------------
    # 登录流程
    # -------------------------
    try:
        login_resp, login_data = post_json(
            s,
            LOGIN_URL,
            data=LOGIN_PAYLOAD,
            headers=LOGIN_HEADERS
        )

        login_msg = login_data.get("msg", "")

        if not (login_resp.ok and login_data.get("ret") == 1):
            send_push(
                s,
                "69云 ",
                login_msg or f"登录失败,HTTP 状态码：{login_resp.status_code}"
            )
            raise SystemExit(f"【错误】登录失败：{login_msg}")

        print("【信息】登录成功")
        send_push(s, "69云", "登录成功")

    except Exception as exc:
        send_push(s, "69云", '登录失败'+str(exc))
        raise SystemExit(f"【异常】登录过程发生异常：{exc}")

    # -------------------------
    # 签到流程
    # -------------------------
    try:
        checkin_resp, data = post_json(
            s,
            CHECKIN_URL,
            headers=CHECKIN_HEADERS
        )

        checkin = data.get("ret")

        # 提取获得流量
        m = re.search(r"获得了\s*([\d.]+\s*[A-Za-z]+)", data.get("msg", ""))
        gained = m.group(1).replace(" ", "") if m else "未知"

        # 剩余流量
        traffic_info = data.get("trafficInfo") or {}
        left = traffic_info.get("unUsedTraffic", "未知")

        if checkin == 1:
            print(f"【信息】签到成功：获得 {gained}，剩余 {left}")
            send_push(
                s,
                "69云",
                f"签到成功,获得流量：{gained}\n剩余流量：{left}"
            )
            sys.exit(0)

        elif checkin == 0:
            print("【提示】今日已签到，无需重复操作")
            send_push(
                s,
                "69云",
                "今日已签到，无需重复操作"
            )
            sys.exit(0)

        else:
            reason = data.get("msg", "未知原因")
            send_push(s, "69云", reason)
            raise SystemExit(f"【错误】签到失败：{reason}")

    except Exception as exc:
        send_push(s, "69云", str(exc))
        raise SystemExit(f"【异常】签到过程发生异常：{exc}")
