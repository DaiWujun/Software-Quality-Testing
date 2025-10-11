"""
管理员权限撤销演示（测试用例：ADMIN-USER-14）

"""

import sys
import os
import time
import json
from datetime import datetime

THIS_DIR = os.path.dirname(__file__)
SRC_ROOT = os.path.abspath(os.path.join(THIS_DIR, ".."))
CORE_DIR = os.path.join(SRC_ROOT, "core")

for p in (SRC_ROOT, CORE_DIR):
    if p and os.path.isdir(p) and p not in sys.path:
        sys.path.insert(0, p)

from config import API_ENDPOINTS, ALL_USERS, API_BASE_URL
from utils import HttpClient
from logger import get_logger

logger = get_logger(__name__)


DEMO_AUTO = os.environ.get("DEMO_AUTO", "0")


def wait_enter(step_desc: str):
    """等待用户按回车继续，若环境变量 DEMO_AUTO 被设为 '1' 则自动前进。"""
    auto = DEMO_AUTO == "1"
    print("\n>> 按回车执行步骤：" + step_desc)
    if auto:
        print("(检测到 DEMO_AUTO=1，自动前进)")
        time.sleep(0.5)
        return
    input()


def pretty(obj):
    try:
        return json.dumps(obj, ensure_ascii=False, indent=2)
    except Exception:
        return str(obj)


def find_user_in_list(users_list, username):
    for u in users_list:
        if u.get("username") == username or u.get("userName") == username:
            return u
    return None


def main():
    demo_username = "admin_demo"
    demo_password = "123"

    anon_client = HttpClient(API_BASE_URL)

    # 第 1 步：创建 admin_demo 账号
    step = "1. 创建 admin_demo 账号（访客）"
    print("\n步骤 1：" + step)
    wait_enter(step)

    try:
        # 使用 name/phone/email 字段以匹配后端预期的请求体
        resp = anon_client.post(
            API_ENDPOINTS.get("register", "/api/register"),
            json={
                "username": demo_username,
                "password": demo_password,
                "name": "",
                "phone": "",
                "email": f"{demo_username}@example.com",
            },
        )
        print(f"注册响应状态码: {resp.status_code}")
        try:
            print("响应体:", pretty(resp.json()))
        except Exception:
            print("响应体: (非 JSON)")
    except Exception as e:
        print("注册请求失败:", str(e))

    # 尝试确定 admin_demo 的当前角色
    print("\n正在确定 admin_demo 的当前角色...")
    current_role = None
    try:
        # Some implementations return created user info; try login to see own info
        resp_login = anon_client.post(
            API_ENDPOINTS.get("login", "/api/login"),
            json={"username": demo_username, "password": demo_password},
        )
        print(f"以 admin_demo 登录的响应状态码: {resp_login.status_code}")
        try:
            data = resp_login.json()
            print("登录响应体:", pretty(data))
            # Look for role fields
            if isinstance(data, dict):
                for key in ("role", "role_en", "roles"):
                    if key in data:
                        current_role = data.get(key)
                        break
        except Exception:
            pass
    except Exception as e:
        print("Login as admin_demo failed (may need to verify user exists):", str(e))

    if not current_role:
        current_role = "visitor"

    print(f"admin_demo 当前角色: {current_role}")

    # 第 2 步：使用 admin 登录
    step = "2. 使用 admin 登录"
    print("\n步骤 2：" + step)
    wait_enter(step)

    admin = ALL_USERS.get("admin")
    if not admin:
        print("在 config.ALL_USERS 中未找到 admin 凭据")
        return

    admin_client = HttpClient(API_BASE_URL)
    try:
        resp = admin_client.post(
            API_ENDPOINTS.get("login", "/api/login"),
            json={"username": admin["username"], "password": admin["password"]},
        )
        print(f"admin 登录响应状态码: {resp.status_code}")
        try:
            print("响应体:", pretty(resp.json()))
        except Exception:
            pass
    except Exception as e:
        print("Admin login request failed:", str(e))
        return

    # 第 3 步：admin 为 admin_demo 授予系统管理员权限
    step = "3. admin 授予 admin_demo 系统管理员权限"
    print("\n步骤 3：" + step)
    wait_enter(step)

    # Use direct PUT /api/admin/user to update roles (grant and revoke) — matches provided backend API
    endpoint = API_ENDPOINTS.get("admin_user", "/api/admin/user")

    # Construct grant payload (grant sysAdmin role) — example structure provided by user
    grant_payload = {
        "username": demo_username,
        "name": "",
        "phone": "",
        "email": f"{demo_username}@example.com",
        "roles": [
            {
                "id": 1,
                "name": "sysAdmin",
                "nameZh": "系统管理员",
                "enabled": True,
                "perms": [
                    {
                        "id": 1,
                        "name": "users_management",
                        "desc_": "用户管理",
                        "url": "/api/admin/user",
                    },
                    {
                        "id": 2,
                        "name": "roles_management",
                        "desc_": "角色管理",
                        "url": "/api/admin/role",
                    },
                    {
                        "id": 3,
                        "name": "content_management",
                        "desc_": "内容管理",
                        "url": "/api/admin/content",
                    },
                ],
                "menus": [],
            }
        ],
    }

    try:
        print("\n尝试为 admin_demo 授予系统管理员权限...")
        resp = admin_client.put(endpoint, json=grant_payload)
        print(f"授予请求响应状态码: {resp.status_code}")
        try:
            print("响应体:", pretty(resp.json()))
        except Exception:
            pass
    except Exception as e:
        print("授予权限请求失败:", str(e))

    # 第 4 步：admin 尝试撤销 admin_demo 的系统管理员权限
    step = "4. admin 撤销 admin_demo 系统管理员权限"
    print("\n步骤 4：" + step)
    wait_enter(step)

    # Construct revoke payload (set roles to visitor)
    revoke_payload = {
        "username": demo_username,
        "name": "",
        "phone": "",
        "email": f"{demo_username}@example.com",
        "roles": [
            {
                "id": 3,
                "name": "visitor",
                "nameZh": "访客",
                "enabled": True,
                "perms": [],
                "menus": [
                    {
                        "id": 1,
                        "path": "/admin",
                        "name": "AdminIndex",
                        "nameZh": "首页",
                        "iconCls": "el-icon-s-home",
                        "component": "AdminIndex",
                        "parentId": 0,
                        "children": [
                            {
                                "id": 2,
                                "path": "/admin/dashboard",
                                "name": "DashboardAdmin",
                                "nameZh": "运行情况",
                                "iconCls": None,
                                "component": "dashboard/admin/index",
                                "parentId": 1,
                                "children": [],
                            }
                        ],
                    }
                ],
            }
        ],
    }

    try:
        print("\n尝试撤销 admin_demo 的系统管理员权限（设置为访客）...")
        resp = admin_client.put(endpoint, json=revoke_payload)
        print(f"撤销请求响应状态码: {resp.status_code}")
        try:
            print("响应体:", pretty(resp.json()))
        except Exception:
            pass

        denied = False
        if resp.status_code in (401, 403):
            denied = True
        else:
            try:
                body = resp.json()
                if isinstance(body, dict):
                    msg = body.get("message") or body.get("error") or ""
                    if "权限" in str(msg) or "denied" in str(msg).lower():
                        denied = True
            except Exception:
                pass

        # 第 5 步：输出结论
        print("\n步骤 5：结论")
        wait_enter("5. 显示结论")

        if denied:
            print("测试结论：操作被拒绝（符合预期）")
        else:
            print("测试结论：测试用例不通过\n理由：撤销管理员权限操作被允许")

    except Exception as e:
        print("撤销权限请求失败:", str(e))
        print("\n结论：由于错误，结果不确定")


if __name__ == "__main__":
    print("管理员权限撤销演示（ADMIN-USER-14）")
    main()
