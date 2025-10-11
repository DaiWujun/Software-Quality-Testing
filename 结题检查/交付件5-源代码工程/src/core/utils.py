"""
通用工具函数模块
提供测试过程中常用的工具函数
"""

import os
import time
import json
from datetime import datetime
from typing import Dict, Any, Optional
import requests
from config import (
    BASE_URL, API_BASE_URL, REQUEST_TIMEOUT, 
    SCREENSHOT_DIR, AUTO_SCREENSHOT
)
from logger import get_logger

logger = get_logger(__name__)


class HttpClient:
    """HTTP客户端封装"""
    
    def __init__(self, base_url=API_BASE_URL, timeout=REQUEST_TIMEOUT):
        """
        初始化HTTP客户端
        
        Args:
            base_url: 基础URL
            timeout: 请求超时时间
        """
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        self.cookies = {}
    
    def set_cookies(self, cookies: Dict[str, str]):
        """
        设置cookies
        
        Args:
            cookies: cookies字典
        """
        self.cookies = cookies
        self.session.cookies.update(cookies)
    
    def get_cookies(self) -> Dict[str, str]:
        """
        获取当前cookies
        
        Returns:
            cookies字典
        """
        return dict(self.session.cookies)
    
    def clear_cookies(self):
        """清除cookies"""
        self.session.cookies.clear()
        self.cookies = {}
    
    def request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """
        发送HTTP请求
        
        Args:
            method: 请求方法（GET, POST, PUT, DELETE等）
            endpoint: API端点
            **kwargs: 其他请求参数
        
        Returns:
            requests.Response: 响应对象
        """
        url = f"{self.base_url}{endpoint}" if not endpoint.startswith('http') else endpoint
        
        # 设置默认超时
        if 'timeout' not in kwargs:
            kwargs['timeout'] = self.timeout
        
        logger.debug(f"发送 {method} 请求: {url}")
        if 'json' in kwargs:
            logger.debug(f"请求数据: {kwargs['json']}")
        
        try:
            response = self.session.request(method, url, **kwargs)
            logger.debug(f"响应状态码: {response.status_code}")
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"请求失败: {str(e)}")
            raise
    
    def get(self, endpoint: str, **kwargs) -> requests.Response:
        """GET请求"""
        return self.request('GET', endpoint, **kwargs)
    
    def post(self, endpoint: str, **kwargs) -> requests.Response:
        """POST请求"""
        return self.request('POST', endpoint, **kwargs)
    
    def put(self, endpoint: str, **kwargs) -> requests.Response:
        """PUT请求"""
        return self.request('PUT', endpoint, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """DELETE请求"""
        return self.request('DELETE', endpoint, **kwargs)


class TimeUtils:
    """时间相关工具"""
    
    @staticmethod
    def get_timestamp() -> str:
        """
        获取当前时间戳字符串
        
        Returns:
            格式化的时间戳字符串
        """
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    @staticmethod
    def get_datetime_str() -> str:
        """
        获取当前日期时间字符串
        
        Returns:
            格式化的日期时间字符串
        """
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    @staticmethod
    def measure_time(func):
        """
        装饰器：测量函数执行时间
        
        Args:
            func: 要测量的函数
        
        Returns:
            包装后的函数
        """
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            duration = end_time - start_time
            logger.info(f"函数 {func.__name__} 执行耗时: {duration:.4f}秒")
            return result, duration
        return wrapper
    
    @staticmethod
    def sleep(seconds: float, reason: str = ""):
        """
        等待指定时间
        
        Args:
            seconds: 等待秒数
            reason: 等待原因
        """
        if reason:
            logger.debug(f"等待 {seconds} 秒 - {reason}")
        else:
            logger.debug(f"等待 {seconds} 秒")
        time.sleep(seconds)


class FileUtils:
    """文件操作工具"""
    
    @staticmethod
    def ensure_dir(directory: str):
        """
        确保目录存在，如果不存在则创建
        
        Args:
            directory: 目录路径
        """
        if not os.path.exists(directory):
            os.makedirs(directory)
            logger.debug(f"创建目录: {directory}")
    
    @staticmethod
    def save_json(data: Dict[Any, Any], filepath: str):
        """
        保存数据为JSON文件
        
        Args:
            data: 要保存的数据
            filepath: 文件路径
        """
        FileUtils.ensure_dir(os.path.dirname(filepath))
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.debug(f"保存JSON文件: {filepath}")
    
    @staticmethod
    def load_json(filepath: str) -> Dict[Any, Any]:
        """
        从JSON文件加载数据
        
        Args:
            filepath: 文件路径
        
        Returns:
            加载的数据
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.debug(f"加载JSON文件: {filepath}")
        return data
    
    @staticmethod
    def get_screenshot_path(test_case_id: str) -> str:
        """
        获取截图保存路径
        
        Args:
            test_case_id: 测试用例ID
        
        Returns:
            截图文件路径
        """
        FileUtils.ensure_dir(SCREENSHOT_DIR)
        timestamp = TimeUtils.get_timestamp()
        filename = f"{test_case_id}_{timestamp}.png"
        return os.path.join(SCREENSHOT_DIR, filename)


class AssertUtils:
    """断言工具"""
    
    @staticmethod
    def assert_equals(actual, expected, message: str = ""):
        """
        断言相等
        
        Args:
            actual: 实际值
            expected: 期望值
            message: 断言消息
        
        Raises:
            AssertionError: 如果断言失败
        """
        passed = actual == expected
        logger.info(f"断言相等 {'✓' if passed else '✗'} - 期望: {expected}, 实际: {actual}")
        if message:
            logger.info(f"断言消息: {message}")
        
        if not passed:
            raise AssertionError(f"{message} - 期望: {expected}, 实际: {actual}")
    
    @staticmethod
    def assert_true(condition, message: str = ""):
        """
        断言为真
        
        Args:
            condition: 条件
            message: 断言消息
        
        Raises:
            AssertionError: 如果断言失败
        """
        logger.info(f"断言为真 {'✓' if condition else '✗'}")
        if message:
            logger.info(f"断言消息: {message}")
        
        if not condition:
            raise AssertionError(f"{message} - 条件为假")
    
    @staticmethod
    def assert_false(condition, message: str = ""):
        """
        断言为假
        
        Args:
            condition: 条件
            message: 断言消息
        
        Raises:
            AssertionError: 如果断言失败
        """
        logger.info(f"断言为假 {'✓' if not condition else '✗'}")
        if message:
            logger.info(f"断言消息: {message}")
        
        if condition:
            raise AssertionError(f"{message} - 条件为真")
    
    @staticmethod
    def assert_in(item, collection, message: str = ""):
        """
        断言包含
        
        Args:
            item: 元素
            collection: 集合
            message: 断言消息
        
        Raises:
            AssertionError: 如果断言失败
        """
        passed = item in collection
        logger.info(f"断言包含 {'✓' if passed else '✗'} - 元素: {item}")
        if message:
            logger.info(f"断言消息: {message}")
        
        if not passed:
            raise AssertionError(f"{message} - {item} 不在集合中")
    
    @staticmethod
    def assert_status_code(response: requests.Response, expected_code: int, message: str = ""):
        """
        断言HTTP状态码
        
        Args:
            response: 响应对象
            expected_code: 期望状态码
            message: 断言消息
        
        Raises:
            AssertionError: 如果断言失败
        """
        actual_code = response.status_code
        passed = actual_code == expected_code
        logger.info(f"断言状态码 {'✓' if passed else '✗'} - 期望: {expected_code}, 实际: {actual_code}")
        if message:
            logger.info(f"断言消息: {message}")
        
        if not passed:
            raise AssertionError(f"{message} - 期望状态码: {expected_code}, 实际: {actual_code}")


class DataGenerator:
    """测试数据生成器"""
    
    @staticmethod
    def generate_unique_username() -> str:
        """
        生成唯一的用户名
        
        Returns:
            唯一用户名
        """
        timestamp = TimeUtils.get_timestamp()
        return f"test_user_{timestamp}"
    
    @staticmethod
    def generate_test_article(include_image: bool = False) -> Dict[str, Any]:
        """
        生成测试文章数据
        
        Args:
            include_image: 是否包含图片
        
        Returns:
            文章数据字典
        """
        timestamp = TimeUtils.get_timestamp()
        article = {
            "title": f"测试文章_{timestamp}",
            "content": f"这是一篇自动化测试生成的文章，生成时间: {TimeUtils.get_datetime_str()}",
            "author": "测试用户"
        }
        
        if include_image:
            article["content"] += "\n[图片占位符]"
            article["has_image"] = True
        
        return article


# 创建全局HTTP客户端实例
http_client = HttpClient()
