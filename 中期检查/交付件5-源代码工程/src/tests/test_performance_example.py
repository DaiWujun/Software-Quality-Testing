"""
性能测试示例
演示如何进行性能测试
"""

import pytest
from base_test import BaseTest
from performance_test import perf_test
from constants import TestData
from logger import get_logger

logger = get_logger(__name__)


class TestPerformance(BaseTest):
    """性能测试类"""
    
    @pytest.mark.performance
    def test_single_request_performance(self):
        """
        测试用例: PERF-THPT-01
        测试单个请求的性能
        """
        self.log_test_case("PERF-THPT-01", "单请求性能测试")
        
        # 执行性能测试
        result = perf_test.concurrent_test(
            func=self.get_books,
            concurrency=1,
            iterations=10
        )
        
        # 验证性能要求
        passed = perf_test.validate_performance_requirement(
            result,
            max_avg_time_ms=5000,
            max_p95_time_ms=5000,
            max_p99_time_ms=5000
        )
        
        assert passed, "性能测试未通过要求"
    
    @pytest.mark.performance
    def test_concurrent_performance(self):
        """
        测试用例: PERF-THPT-02/03/04
        测试不同并发级别的性能
        """
        self.log_test_case("PERF-THPT-02/03/04", "并发性能测试")
        
        # 测试不同的并发级别
        concurrency_levels = TestData.PERFORMANCE_TEST_CONCURRENCY  # [1, 9, 10, 11]
        
        results = perf_test.batch_concurrent_test(
            func=self.get_books,
            concurrency_levels=concurrency_levels,
            iterations=TestData.PERFORMANCE_TEST_ITERATIONS
        )
        
        # 验证所有并发级别都满足性能要求
        all_passed = True
        for concurrency, result in results.items():
            logger.info(f"\n验证并发级别 {concurrency} 的性能要求")
            passed = perf_test.validate_performance_requirement(
                result,
                max_avg_time_ms=5000,
                max_p95_time_ms=5000,
                max_p99_time_ms=5000
            )
            
            if not passed:
                all_passed = False
                logger.error(f"并发级别 {concurrency} 未通过性能要求")
        
        assert all_passed, "部分并发级别未通过性能要求"
    
    @pytest.mark.performance
    def test_search_performance(self):
        """
        测试搜索功能的性能
        """
        self.log_test_case("PERF-SEARCH-01", "搜索性能测试")
        
        # 测试搜索性能
        result = perf_test.concurrent_test(
            func=self.search_books,
            concurrency=10,
            iterations=10,
            keyword="测试"
        )
        
        # 验证性能
        passed = perf_test.validate_performance_requirement(
            result,
            max_avg_time_ms=5000
        )
        
        assert passed, "搜索性能测试未通过"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s", "-m", "performance"])
