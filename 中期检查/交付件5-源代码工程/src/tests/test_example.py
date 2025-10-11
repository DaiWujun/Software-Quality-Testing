"""
示例测试文件
演示如何使用测试框架编写测试用例
"""

import pytest
from base_test import BaseTest
from constants import HttpStatus, UserRole
from config import ALL_USERS


class TestExample(BaseTest):
    """示例测试类"""
    
    def test_admin_login_success(self):
        """
        测试用例: AUTH-LOGIN-01
        测试管理员成功登录
        """
        self.log_test_case("AUTH-LOGIN-01", "管理员登录成功测试")
        
        # 步骤1: 使用管理员账户登录
        self.log_step("使用管理员账户登录")
        response = self.login_as("admin")
        
        # 断言: 登录应该成功
        self.assert_utils.assert_true(
            "token" in response or "success" in str(response),
            "登录应该返回token或成功标识"
        )
        
        logger.info("测试用例 AUTH-LOGIN-01 执行通过")
    
    def test_visitor_cannot_access_admin(self):
        """
        测试用例: AUTH-LOGIN-02
        测试访客无法进入管理中心
        """
        self.log_test_case("AUTH-LOGIN-02", "访客无法进入管理中心")
        
        # 步骤1: 使用访客账户登录
        self.log_step("使用访客账户登录")
        self.login_as("visitor")
        
        # 步骤2: 尝试访问管理中心
        self.log_step("尝试访问管理中心")
        response = self.client.get("/api/admin/dashboard")
        
        # 断言: 应该返回403或跳转
        self.assert_utils.assert_true(
            response.status_code in [HttpStatus.FORBIDDEN, HttpStatus.UNAUTHORIZED],
            "访客不应该能访问管理中心"
        )
        
        logger.info("测试用例 AUTH-LOGIN-02 执行通过")
    
    def test_book_search_by_keyword(self):
        """
        测试用例: LIB-SRCH-01
        测试图书搜索功能
        """
        self.log_test_case("LIB-SRCH-01", "图书关键词搜索测试")
        
        # 步骤1: 执行搜索
        keyword = "三体"
        self.log_step(f"搜索关键词: {keyword}")
        result = self.search_books(keyword)
        
        # 断言: 应该返回搜索结果
        self.assert_utils.assert_true(
            "books" in result or "data" in result,
            "搜索应该返回结果"
        )
        
        logger.info("测试用例 LIB-SRCH-01 执行通过")
    
    def test_response_time_measurement(self):
        """
        测试用例: PERF-THPT-01
        测试响应时间
        """
        self.log_test_case("PERF-THPT-01", "响应时间测试")
        
        # 步骤1: 测量获取图书列表的响应时间
        self.log_step("测量获取图书列表的响应时间")
        result, duration_ms = self.measure_response_time(self.get_books)
        
        # 断言: 响应时间应该在5000ms以内
        self.assert_response_time(duration_ms, max_time_ms=5000)
        
        logger.info("测试用例 PERF-THPT-01 执行通过")
    
    def test_article_creation_by_editor(self):
        """
        测试用例: ADMIN-CONT-01
        测试内容管理员创建文章
        """
        self.log_test_case("ADMIN-CONT-01", "内容管理员创建文章测试")
        
        # 步骤1: 使用编辑账户登录
        self.log_step("使用内容管理员账户登录")
        self.login_as("editor")
        
        # 步骤2: 创建文章
        self.log_step("创建测试文章")
        title = "自动化测试文章"
        content = "这是一篇自动化测试创建的文章"
        result = self.create_article(title, content)
        
        # 断言: 文章创建成功
        self.assert_utils.assert_true(
            "id" in result or "success" in str(result),
            "文章应该创建成功"
        )
        
        # 清理: 删除测试文章
        if "id" in result:
            self.log_step("清理测试数据")
            self.delete_article(result["id"])
        
        logger.info("测试用例 ADMIN-CONT-01 执行通过")


# 导入logger用于日志记录
from logger import get_logger
logger = get_logger(__name__)


if __name__ == "__main__":
    # 可以直接运行此文件进行测试
    pytest.main([__file__, "-v", "-s"])
