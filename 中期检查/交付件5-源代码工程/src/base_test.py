"""
测试基类
所有测试类的基类，提供通用的测试方法和设置
"""

import time
import pytest
from typing import Optional
from logger import get_logger
from utils import HttpClient, TimeUtils, FileUtils, AssertUtils
from config import API_BASE_URL, AUTO_SCREENSHOT, ALL_USERS

logger = get_logger(__name__)


class BaseTest:
    """测试基类"""
    
    def setup_method(self, method):
        """
        每个测试方法执行前的设置
        
        Args:
            method: 测试方法
        """
        self.test_method_name = method.__name__
        logger.info(f"开始执行测试方法: {self.test_method_name}")
        
        # 创建HTTP客户端
        self.client = HttpClient(API_BASE_URL)
        
        # 初始化测试开始时间
        self.test_start_time = time.time()
        
        # 初始化断言工具
        self.assert_utils = AssertUtils()
    
    def teardown_method(self, method):
        """
        每个测试方法执行后的清理
        
        Args:
            method: 测试方法
        """
        # 计算测试耗时
        test_duration = time.time() - self.test_start_time
        
        logger.info(f"测试方法 {self.test_method_name} 执行完成，耗时: {test_duration:.2f}秒")
        
        # 清理session
        if hasattr(self, 'client'):
            self.client.clear_cookies()
    
    def login(self, username: str, password: str) -> dict:
        """
        执行登录操作
        
        Args:
            username: 用户名
            password: 密码
        
        Returns:
            登录响应数据
        """
        logger.info(f"尝试登录用户: {username}")
        
        login_data = {
            "username": username,
            "password": password
        }
        
        response = self.client.post("/api/login", json=login_data)
        
        logger.info(f"登录响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            logger.info(f"用户 {username} 登录成功")
            # 保存cookies
            self.client.set_cookies(self.client.get_cookies())
            
            # 尝试解析响应
            try:
                result = response.json() if response.content else {}
                logger.info(f"登录响应数据: {result}")
                return result
            except Exception as e:
                logger.warning(f"解析登录响应失败: {e}")
                return {"status": "success", "message": "登录成功"}
        else:
            logger.warning(f"用户 {username} 登录失败，状态码: {response.status_code}")
            try:
                error_data = response.json() if response.content else {}
                logger.warning(f"错误响应: {error_data}")
                return error_data
            except:
                return {"status": "error", "message": f"登录失败，状态码: {response.status_code}"}
    
    def login_as(self, role: str) -> dict:
        """
        以指定角色登录
        
        Args:
            role: 角色类型 (admin, editor, visitor, tester)
        
        Returns:
            登录响应数据
        """
        if role not in ALL_USERS:
            raise ValueError(f"未知的角色类型: {role}")
        
        user = ALL_USERS[role]
        return self.login(user['username'], user['password'])
    
    def logout(self):
        """执行登出操作"""
        logger.info("执行登出操作")
        
        try:
            response = self.client.post("/api/logout")
            self.client.clear_cookies()
            
            if response.status_code == 200:
                logger.info("登出成功")
            else:
                logger.warning(f"登出失败，状态码: {response.status_code}")
        except Exception as e:
            logger.error(f"登出时发生错误: {str(e)}")
    
    def get_books(self, page: int = 1, size: int = 18, keyword: str = "") -> dict:
        """
        获取图书列表
        
        Args:
            page: 页码
            size: 每页数量
            keyword: 搜索关键词
        
        Returns:
            图书列表数据
        """
        params = {
            "page": page,
            "size": size
        }
        
        if keyword:
            params["keyword"] = keyword
        
        response = self.client.get("/api/books", params=params)
        return response.json() if response.content else {}
    
    def search_books(self, keyword: str) -> dict:
        """
        搜索图书
        
        Args:
            keyword: 搜索关键词
        
        Returns:
            搜索结果
        """
        logger.info(f"搜索图书，关键词: {keyword}")
        
        response = self.client.get("/api/books/search", params={"keyword": keyword})
        return response.json() if response.content else {}
    
    def get_book_categories(self) -> dict:
        """
        获取图书分类
        
        Returns:
            分类列表
        """
        response = self.client.get("/api/categories")
        return response.json() if response.content else {}
    
    def create_article(self, title: str, content: str) -> dict:
        """
        创建文章
        
        Args:
            title: 文章标题
            content: 文章内容
        
        Returns:
            创建结果
        """
        logger.info(f"创建文章: {title}")
        
        article_data = {
            "title": title,
            "content": content
        }
        
        response = self.client.post("/api/articles", json=article_data)
        return response.json() if response.content else {}
    
    def delete_article(self, article_id: int) -> dict:
        """
        删除文章
        
        Args:
            article_id: 文章ID
        
        Returns:
            删除结果
        """
        logger.info(f"删除文章: {article_id}")
        
        response = self.client.delete(f"/api/articles/{article_id}")
        return response.json() if response.content else {}
    
    def get_admin_statistics(self) -> dict:
        """
        获取管理员统计信息
        
        Returns:
            统计信息
        """
        response = self.client.get("/api/admin/statistics")
        return response.json() if response.content else {}
    
    def get_users(self) -> dict:
        """
        获取用户列表（需要管理员权限）
        
        Returns:
            用户列表
        """
        response = self.client.get("/api/admin/users")
        return response.json() if response.content else {}
    
    def update_user_status(self, user_id: int, enabled: bool) -> dict:
        """
        更新用户状态
        
        Args:
            user_id: 用户ID
            enabled: 是否启用
        
        Returns:
            更新结果
        """
        endpoint = f"/api/admin/users/{user_id}/{'enable' if enabled else 'disable'}"
        response = self.client.post(endpoint)
        return response.json() if response.content else {}
    
    def update_user_role(self, user_id: int, role: str) -> dict:
        """
        更新用户角色
        
        Args:
            user_id: 用户ID
            role: 新角色
        
        Returns:
            更新结果
        """
        role_data = {"role": role}
        response = self.client.put(f"/api/admin/users/{user_id}/role", json=role_data)
        return response.json() if response.content else {}
    
    def measure_response_time(self, func, *args, **kwargs) -> tuple:
        """
        测量函数响应时间
        
        Args:
            func: 要测量的函数
            *args: 位置参数
            **kwargs: 关键字参数
        
        Returns:
            (结果, 耗时毫秒)
        """
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        duration_ms = (end_time - start_time) * 1000
        logger.info(f"响应时间: {duration_ms:.2f}ms")
        
        return result, duration_ms
    
    def assert_response_time(self, duration_ms: float, max_time_ms: float = 5000):
        """
        断言响应时间
        
        Args:
            duration_ms: 实际响应时间（毫秒）
            max_time_ms: 最大允许时间（毫秒）
        """
        passed = duration_ms <= max_time_ms
        logger.info(f"响应时间断言 {'✓' if passed else '✗'} - "
                   f"实际: {duration_ms:.2f}ms, 最大允许: {max_time_ms}ms")
        
        assert passed, f"响应时间超时: {duration_ms:.2f}ms > {max_time_ms}ms"
    
    def log_test_case(self, test_case_id: str, test_case_title: str):
        """
        记录测试用例信息
        
        Args:
            test_case_id: 测试用例ID
            test_case_title: 测试用例标题
        """
        logger.info("=" * 80)
        logger.info(f"测试用例: {test_case_id} - {test_case_title}")
        logger.info("=" * 80)
    
    def log_step(self, step: str):
        """
        记录测试步骤
        
        Args:
            step: 步骤描述
        """
        logger.info(f"步骤: {step}")
    
    def take_screenshot(self, name: str = ""):
        """
        截图（当使用Selenium时）
        
        Args:
            name: 截图名称
        """
        if not AUTO_SCREENSHOT:
            return
        
        # 这里预留接口，当使用Selenium时实现
        logger.debug(f"截图: {name}")
