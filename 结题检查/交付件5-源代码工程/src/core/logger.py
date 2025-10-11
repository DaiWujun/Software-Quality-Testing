"""
日志配置模块
提供统一的日志记录功能
"""

import logging
import os
from datetime import datetime
from config import LOG_DIR, VERBOSE_LOGGING


class TestLogger:
    """测试日志记录器"""
    
    _instance = None
    
    def __new__(cls):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super(TestLogger, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """初始化日志配置"""
        if self._initialized:
            return
        
        self._initialized = True
        
        # 确保日志目录存在
        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR)
        
        # 创建日志文件名（包含时间戳）
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(LOG_DIR, f"test_{timestamp}.log")
        
        # 配置日志格式
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        date_format = '%Y-%m-%d %H:%M:%S'
        
        # 设置日志级别
        log_level = logging.DEBUG if VERBOSE_LOGGING else logging.INFO
        
        # 配置根日志记录器
        logging.basicConfig(
            level=log_level,
            format=log_format,
            datefmt=date_format,
            handlers=[
                # 文件处理器
                logging.FileHandler(log_file, encoding='utf-8'),
                # 控制台处理器
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger('TestLogger')
        self.logger.info(f"日志系统初始化完成，日志文件: {log_file}")
    
    def get_logger(self, name=None):
        """
        获取日志记录器
        
        Args:
            name: 日志记录器名称，如果为None则使用默认名称
        
        Returns:
            logging.Logger: 日志记录器实例
        """
        if name:
            return logging.getLogger(name)
        return self.logger
    
    def info(self, message):
        """记录INFO级别日志"""
        self.logger.info(message)
    
    def debug(self, message):
        """记录DEBUG级别日志"""
        self.logger.debug(message)
    
    def warning(self, message):
        """记录WARNING级别日志"""
        self.logger.warning(message)
    
    def error(self, message):
        """记录ERROR级别日志"""
        self.logger.error(message)
    
    def critical(self, message):
        """记录CRITICAL级别日志"""
        self.logger.critical(message)
    
    def log_test_start(self, test_case_id, test_case_title):
        """
        记录测试开始
        
        Args:
            test_case_id: 测试用例ID
            test_case_title: 测试用例标题
        """
        self.logger.info("=" * 80)
        self.logger.info(f"开始执行测试用例: {test_case_id} - {test_case_title}")
        self.logger.info("=" * 80)
    
    def log_test_end(self, test_case_id, result, duration=None):
        """
        记录测试结束
        
        Args:
            test_case_id: 测试用例ID
            result: 测试结果（PASS/FAIL）
            duration: 测试耗时（秒）
        """
        duration_str = f", 耗时: {duration:.2f}秒" if duration else ""
        self.logger.info(f"测试用例 {test_case_id} 执行完成 - 结果: {result}{duration_str}")
        self.logger.info("=" * 80)
        self.logger.info("")
    
    def log_step(self, step_number, step_description):
        """
        记录测试步骤
        
        Args:
            step_number: 步骤编号
            step_description: 步骤描述
        """
        self.logger.info(f"步骤 {step_number}: {step_description}")
    
    def log_request(self, method, url, **kwargs):
        """
        记录HTTP请求
        
        Args:
            method: 请求方法
            url: 请求URL
            **kwargs: 其他请求参数
        """
        self.logger.debug(f"发送 {method} 请求: {url}")
        if kwargs:
            self.logger.debug(f"请求参数: {kwargs}")
    
    def log_response(self, status_code, response_data=None):
        """
        记录HTTP响应
        
        Args:
            status_code: 响应状态码
            response_data: 响应数据
        """
        self.logger.debug(f"收到响应: 状态码 {status_code}")
        if response_data:
            self.logger.debug(f"响应数据: {response_data}")
    
    def log_assertion(self, expected, actual, passed):
        """
        记录断言结果
        
        Args:
            expected: 期望值
            actual: 实际值
            passed: 是否通过
        """
        status = "✓ 通过" if passed else "✗ 失败"
        self.logger.info(f"断言 {status} - 期望: {expected}, 实际: {actual}")


# 创建全局日志实例
logger = TestLogger()


def get_logger(name=None):
    """
    获取日志记录器的便捷函数
    
    Args:
        name: 日志记录器名称
    
    Returns:
        logging.Logger: 日志记录器实例
    """
    return logger.get_logger(name)
