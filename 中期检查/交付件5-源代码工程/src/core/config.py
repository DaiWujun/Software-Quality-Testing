"""
测试配置文件
存放项目的基本配置信息，包括URL、账户信息等
"""

# ==================== 系统配置 ====================
# 基础URL配置
BASE_URL = "http://localhost:8443"
API_BASE_URL = "http://localhost:8443"

# 页面路由
ROUTES = {
    "home": "/",
    "library": "/library",
    "notebook": "/notebook",
    "admin": "/admin",
    "login": "/login"
}

# ==================== 账户信息 ====================
# 系统管理员账户
ADMIN_USER = {
    "username": "admin",
    "password": "123",
    "role": "系统管理员",
    "role_en": "admin"
}

# 内容管理员账户
EDITOR_USER = {
    "username": "editor",
    "password": "123",
    "role": "内容管理员",
    "role_en": "editor"
}

# 访客账户
VISITOR_USER = {
    "username": "test",
    "password": "123",
    "role": "访客",
    "role_en": "visitor"
}

# 测试人员账户（如果有的话）
TESTER_USER = {
    "username": "tester",
    "password": "123",
    "role": "测试人员",
    "role_en": "tester"
}

# 所有用户集合
ALL_USERS = {
    "admin": ADMIN_USER,
    "editor": EDITOR_USER,
    "visitor": VISITOR_USER,
    "tester": TESTER_USER
}

# ==================== API端点配置 ====================
API_ENDPOINTS = {
    # 认证相关
    "login": "/api/login",
    "logout": "/api/logout",
    "register": "/api/register",
    
    # 图书相关
    "books": "/api/books",
    "book_detail": "/api/books/{id}",
    "book_search": "/api/books/search",
    "book_categories": "/api/categories",
    
    # 文章/笔记相关
    "articles": "/api/articles",
    "article_detail": "/api/articles/{id}",
    "article_create": "/api/articles",
    "article_update": "/api/articles/{id}",
    "article_delete": "/api/articles/{id}",
    
    # 管理员相关
    "admin_dashboard": "/api/admin/dashboard",
    "admin_users": "/api/admin/users",
    "admin_user_disable": "/api/admin/users/{id}/disable",
    "admin_user_enable": "/api/admin/users/{id}/enable",
    "admin_user_role": "/api/admin/users/{id}/role",
    "admin_statistics": "/api/admin/statistics",
    
    # 广告相关
    "advertisements": "/api/advertisements",
    "advertisement_detail": "/api/advertisements/{id}",
    
    # 更新内容相关
    "updates": "/api/updates",
    "update_detail": "/api/updates/{id}"
}

# ==================== 测试配置 ====================
# 超时设置（秒）
REQUEST_TIMEOUT = 10
PAGE_LOAD_TIMEOUT = 30
IMPLICIT_WAIT = 10

# 最大等待时长（毫秒）- 用于性能测试
MAX_WAIT_TIME_MS = 5000

# 测试数据配置
TEST_DATA_DIR = "../outputs"
LOG_DIR = "../outputs/logs"
SCREENSHOT_DIR = "../outputs/screenshots"
REPORT_DIR = "../outputs/reports"

# ==================== 浏览器配置 ====================
# Selenium浏览器配置
BROWSER = "chrome"  # 可选: chrome, firefox, edge
HEADLESS = False  # 是否无头模式

# 浏览器选项
BROWSER_OPTIONS = {
    "window_size": "1920,1080",
    "disable_gpu": True,
    "no_sandbox": True,
    "disable_dev_shm_usage": True
}

# ==================== 数据库配置（如需要） ====================
# 如果需要直接访问数据库进行验证
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "username": "root",
    "password": "root",
    "database": "whitejotter"
}

# ==================== 其他配置 ====================
# 是否启用详细日志
VERBOSE_LOGGING = True

# 是否在测试失败时自动截图
AUTO_SCREENSHOT = True

# 测试报告格式
REPORT_FORMAT = "html"  # html, json, xml
