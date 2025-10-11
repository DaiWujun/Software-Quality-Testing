"""
测试：后端能否阻止对系统管理员权限的修改操作
"""

import os
import sys
import time
import json

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
    print("\n>> " + step_desc)
    if DEMO_AUTO == "1":
        time.sleep(0.3)
        return
    input()


def step_start(desc: str):
    print(f"{desc}")
    print("（回车以继续）")
    if DEMO_AUTO == "1":
        time.sleep(0.3)
        return
    input()


def pretty(obj):
    try:
        return json.dumps(obj, ensure_ascii=False, indent=2)
    except Exception:
        return str(obj)


def attempt_role_update_simple(
    logged_in_client: HttpClient, target_username: str, roles_payload: dict
):
    endpoint = API_ENDPOINTS.get("admin_user", "/api/admin/user")
    try:
        resp = logged_in_client.put(endpoint, json=roles_payload)
    except Exception as e:
        return None, f"请求失败: {e}", True

    if resp is None:
        return None, "无响应", True

    status = getattr(resp, "status_code", None)
    body_summary = ""
    denied = False
    try:
        body = resp.json()
        if isinstance(body, dict):
            body_summary = (
                body.get("message")
                or body.get("error")
                or json.dumps(body, ensure_ascii=False)
            )
            if (
                status in (401, 403)
                or "权限" in str(body_summary)
                or "denied" in str(body_summary).lower()
            ):
                denied = True
        else:
            body_summary = str(body)
    except Exception:
        body_summary = f"(非 JSON 响应, status={status})"
        if status in (401, 403):
            denied = True

    return status, body_summary, denied


def get_current_role_simple(client: HttpClient, username: str):
    admin = ALL_USERS.get("admin")
    try:
        if admin:
            admin_client = HttpClient(API_BASE_URL)
            resp = admin_client.post(
                API_ENDPOINTS.get("login", "/api/login"),
                json={"username": admin["username"], "password": admin["password"]},
            )
            resp = admin_client.get(API_ENDPOINTS.get("admin_user", "/api/admin/user"))
            try:
                body = resp.json()
                results = None
                if isinstance(body, dict):
                    results = (
                        body.get("result") or body.get("data") or body.get("users")
                    )
                if isinstance(results, list):
                    for u in results:
                        if (
                            u.get("username") == username
                            or u.get("userName") == username
                        ):
                            roles = u.get("roles") or []
                            if isinstance(roles, list) and roles:
                                namezhs = [
                                    r.get("nameZh") for r in roles if r.get("nameZh")
                                ]
                                if namezhs:
                                    return (
                                        ",".join(namezhs)
                                        if len(namezhs) > 1
                                        else namezhs[0]
                                    )
                            for key in ("role", "role_en"):
                                if key in u and u.get(key):
                                    return u.get(key)
            except Exception:
                pass
    except Exception:
        pass

    try:
        resp = client.post(
            API_ENDPOINTS.get("login", "/api/login"),
            json={
                "username": username,
                "password": ALL_USERS.get(username, {}).get("password", "123"),
            },
        )
        try:
            data = resp.json()
            if isinstance(data, dict):
                for key in ("role", "role_en", "roles"):
                    if key in data and data.get(key):
                        return data.get(key)
        except Exception:
            pass
    except Exception:
        pass

    try:
        resp = client.get(API_ENDPOINTS.get("admin_users", "/api/admin/users"))
        try:
            users = resp.json()
            u = None
            if isinstance(users, list):
                for it in users:
                    if it.get("username") == username or it.get("userName") == username:
                        u = it
                        break
            elif isinstance(users, dict):
                data = users.get("data") or users.get("users")
                if isinstance(data, list):
                    for it in data:
                        if (
                            it.get("username") == username
                            or it.get("userName") == username
                        ):
                            u = it
                            break
            if u:
                for key in ("role", "role_en", "roles"):
                    if key in u and u.get(key):
                        return u.get(key)
        except Exception:
            pass
    except Exception:
        pass

    return None


def run_test_scenario(
    login_user_key: str, target_role_payload: dict, scenario_desc: str
):
    print("\n" + scenario_desc)

    user = ALL_USERS.get(login_user_key)
    if not user:
        print(f"用户配置未找到: {login_user_key}")
        return

    client = HttpClient(API_BASE_URL)

    step_start(
        "步骤1：登录（账号：%s，密码：%s），输出当前用户的权限"
        % (user["username"], user["password"])
    )
    try:
        client.post(
            API_ENDPOINTS.get("login", "/api/login"),
            json={"username": user["username"], "password": user["password"]},
        )
    except Exception:
        pass

    current_role = get_current_role_simple(client, user["username"])
    print(
        "\n\n\n步骤1结果：当前用户权限为 %s"
        % (current_role if current_role is not None else "获取失败")
    )

    step_start("步骤2：调用 API 请求提升当前用户为目标角色，并展示响应结果")
    status, body_summary, denied = attempt_role_update_simple(
        client, user["username"], target_role_payload
    )
    status_str = str(status) if status is not None else "无响应"
    short_body = (
        (body_summary[:200] + "...")
        if isinstance(body_summary, str) and len(body_summary) > 200
        else body_summary
    )
    print("\n\n\n步骤2结果：status=" + status_str)

    step_start("步骤3：再次输出当前用户的权限并给出测试结论")
    latest_role = get_current_role_simple(client, user["username"])
    latest_role_str = latest_role if latest_role is not None else "获取失败"
    print("\n\n\n步骤3结果：当前用户权限为 %s" % latest_role_str)

    passed = denied or (latest_role == current_role)
    print(
        "\n结论：%s"
        % ("通过 - 系统拒绝非法权限修改" if passed else "失败 - 非法提升被允许")
    )


def main():
    print("非法提升权限演示")

    payload_editor_to_useradmin = {
        "username": "editor",
        "name": "",
        "phone": "",
        "email": "editor@example.com",
        "roles": [
            {
                "id": 2,
                "name": "userAdmin",
                "nameZh": "用户管理员",
                "enabled": True,
                "perms": [
                    {
                        "id": 10,
                        "name": "users_management",
                        "desc_": "用户管理",
                        "url": "/api/admin/user",
                    }
                ],
                "menus": [],
            }
        ],
    }

    payload_editor_to_test = {
        "username": "editor",
        "name": "",
        "phone": "",
        "email": "editor@example.com",
        "roles": [
            {
                "id": 4,
                "name": "test",
                "nameZh": "测试人员",
                "enabled": True,
                "perms": [],
                "menus": [],
            }
        ],
    }

    payload_test_to_editor = {
        "username": "test",
        "name": "",
        "phone": "",
        "email": "test@example.com",
        "roles": [
            {
                "id": 5,
                "name": "editor",
                "nameZh": "内容管理员",
                "enabled": True,
                "perms": [],
                "menus": [],
            }
        ],
    }

    payload_test_to_useradmin = {
        "username": "test",
        "name": "",
        "phone": "",
        "email": "test@example.com",
        "roles": [
            {
                "id": 2,
                "name": "userAdmin",
                "nameZh": "用户管理员",
                "enabled": True,
                "perms": [],
                "menus": [],
            }
        ],
    }

    run_test_scenario(
        "editor", payload_editor_to_useradmin, "测试1：editor 尝试提升为 用户管理员"
    )

    run_test_scenario(
        "editor", payload_editor_to_test, "测试2：editor 尝试提升为 测试人员"
    )

    run_test_scenario(
        "tester", payload_test_to_editor, "测试3：tester 尝试提升为 内容管理员"
    )

    run_test_scenario(
        "tester", payload_test_to_useradmin, "测试4：tester 尝试提升为 用户管理员"
    )


if __name__ == "__main__":
    main()
