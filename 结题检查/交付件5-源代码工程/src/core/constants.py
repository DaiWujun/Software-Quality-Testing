"""
常量定义文件
存放测试过程中使用的常量、枚举等
"""

# ==================== 用户角色常量 ====================
class UserRole:
    """用户角色枚举"""
    ADMIN = "系统管理员"
    EDITOR = "内容管理员"
    TESTER = "测试人员"
    VISITOR = "访客"
    
    # 英文对应
    ADMIN_EN = "admin"
    EDITOR_EN = "editor"
    TESTER_EN = "tester"
    VISITOR_EN = "visitor"


# ==================== 用户状态常量 ====================
class UserStatus:
    """用户状态枚举"""
    ENABLED = "启用"
    DISABLED = "禁用"


# ==================== 测试模块常量 ====================
class TestModule:
    """测试模块分类"""
    HOME_AD = "HOME-AD"           # 主页广告
    HOME_UPD = "HOME-UPD"         # 主页更新
    HOME_PROJ = "HOME-PROJ"       # 主页项目信息
    NOTE_ART = "NOTE-ART"         # 笔记本文章
    LIB_INFO = "LIB-INFO"         # 图书馆信息
    LIB_BCAT = "LIB-BCAT"         # 图书馆分类
    LIB_SRCH = "LIB-SRCH"         # 图书馆搜索
    ADMIN_STAT = "ADMIN-STAT"     # 管理中心统计
    ADMIN_USER = "ADMIN-USER"     # 管理中心用户管理
    ADMIN_CONT = "ADMIN-CONT"     # 管理中心内容管理
    AUTH_LOGIN = "AUTH-LOGIN"     # 登录认证
    AUTH_RESTR = "AUTH-RESTR"     # 权限限制
    PERF_THPT = "PERF-THPT"       # 性能吞吐量


# ==================== HTTP状态码常量 ====================
class HttpStatus:
    """HTTP状态码"""
    OK = 200
    CREATED = 201
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500


# ==================== 响应消息常量 ====================
class ResponseMessage:
    """常见响应消息"""
    LOGIN_SUCCESS = "登录成功"
    LOGIN_FAILED = "登录失败"
    LOGOUT_SUCCESS = "登出成功"
    PERMISSION_DENIED = "权限不足"
    OPERATION_SUCCESS = "操作成功"
    OPERATION_FAILED = "操作失败"
    INVALID_INPUT = "输入信息无效"
    DATA_NOT_FOUND = "数据不存在"


# ==================== 页面元素定位器常量 ====================
class Locators:
    """页面元素定位器（使用XPath或CSS选择器）"""
    
    # 登录页面
    LOGIN_USERNAME = "//input[@name='username']"
    LOGIN_PASSWORD = "//input[@name='password']"
    LOGIN_SUBMIT = "//button[@type='submit']"
    
    # 导航栏
    NAV_HOME = "//nav//a[contains(text(), '首页')]"
    NAV_LIBRARY = "//nav//a[contains(text(), '图书馆')]"
    NAV_NOTEBOOK = "//nav//a[contains(text(), '笔记本')]"
    NAV_ADMIN = "//nav//a[contains(text(), '管理中心')]"
    NAV_LOGIN = "//nav//a[contains(text(), '登录')]"
    NAV_LOGOUT = "//nav//a[contains(text(), '退出')]"
    
    # 图书馆页面
    LIBRARY_SEARCH_INPUT = "//input[@placeholder='搜索']"
    LIBRARY_SEARCH_BUTTON = "//button[contains(text(), '搜索')]"
    LIBRARY_BOOK_ITEM = "//div[contains(@class, 'book-item')]"
    LIBRARY_CATEGORY_SIDEBAR = "//div[contains(@class, 'category')]"
    LIBRARY_PAGINATION = "//div[contains(@class, 'pagination')]"
    
    # 笔记本页面
    NOTEBOOK_WRITE_ARTICLE = "//button[contains(text(), '写文章')]"
    NOTEBOOK_ARTICLE_LIST = "//div[contains(@class, 'article-list')]"
    
    # 管理中心
    ADMIN_SIDEBAR = "//div[contains(@class, 'admin-sidebar')]"
    ADMIN_USER_MANAGEMENT = "//a[contains(text(), '用户管理')]"
    ADMIN_CONTENT_MANAGEMENT = "//a[contains(text(), '内容管理')]"
    ADMIN_STATISTICS = "//a[contains(text(), '网站运行情况')]"


# ==================== 测试数据常量 ====================
class TestData:
    """测试数据"""
    
    # 测试书籍信息
    TEST_BOOK_KEYWORDS = ["三体", "红楼梦", "活着", "围城"]
    TEST_AUTHOR_KEYWORDS = ["刘慈欣", "曹雪芹", "余华", "钱钟书"]
    TEST_COUNTRY_KEYWORDS = ["中国", "美国", "英国", "法国"]
    
    # 测试文章内容
    TEST_ARTICLE_TITLE = "自动化测试文章标题"
    TEST_ARTICLE_CONTENT = "这是一篇自动化测试生成的文章内容。"
    TEST_ARTICLE_CONTENT_WITH_IMAGE = "这是一篇包含图片的测试文章。"
    
    # 测试搜索关键词
    VALID_SEARCH_KEYWORD = "测试"
    INVALID_SEARCH_KEYWORD = "asdfghjklqwertyuiop12345"
    EMPTY_SEARCH_KEYWORD = ""
    KEYWORD_WITH_SPACE_PREFIX = " 测试"
    KEYWORD_WITH_SPACE_SUFFIX = "测试 "
    KEYWORD_WITH_SPECIAL_CHARS = "测试@#$"
    
    # 性能测试配置
    PERFORMANCE_TEST_CONCURRENCY = [1, 9, 10, 11]
    PERFORMANCE_TEST_ITERATIONS = 10


# ==================== 预期结果常量 ====================
class ExpectedResult:
    """预期结果常量"""
    
    # 图书馆布局
    BOOKS_PER_PAGE = 18  # 每页3行6列
    BOOKS_PER_ROW = 6
    ROWS_PER_PAGE = 3
    
    # 时间限制
    MAX_RESPONSE_TIME_MS = 5000
    
    # 用户管理预期
    CANNOT_DISABLE_ADMIN = "不能禁用系统管理员账户"
    CANNOT_DISABLE_SELF = "不能禁用自己的账户"
    ROLE_UPDATE_SUCCESS = "角色更新成功"


# ==================== 错误消息常量 ====================
class ErrorMessage:
    """错误消息常量"""
    ELEMENT_NOT_FOUND = "页面元素未找到"
    PAGE_LOAD_TIMEOUT = "页面加载超时"
    REQUEST_TIMEOUT = "请求超时"
    AUTHENTICATION_FAILED = "认证失败"
    PERMISSION_DENIED = "权限被拒绝"
    INVALID_INPUT = "无效输入"
    NETWORK_ERROR = "网络错误"


# ==================== 文件路径常量 ====================
class FilePath:
    """文件路径常量"""
    TEST_IMAGE = "../outputs/test_image.png"
    TEST_DOCUMENT = "../outputs/test_document.pdf"
    LOG_FILE = "../outputs/logs/test.log"
