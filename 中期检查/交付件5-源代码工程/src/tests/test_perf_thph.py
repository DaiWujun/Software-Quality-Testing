import pytest
from base_test import BaseTest
from performance_test import perf_test
from constants import TestData
from logger import get_logger
import config

logger = get_logger(__name__)


class TestPerfThpt(BaseTest):

    @pytest.mark.performance
    def test_perf_thpt_01_single_request(self):
        self.log_test_case("PERF-THPT-01", "单请求吞吐/延迟")

        result = perf_test.concurrent_test(
            func=self.get_books,
            concurrency=1,
            iterations=TestData.PERFORMANCE_TEST_ITERATIONS,
        )

        passed = perf_test.validate_performance_requirement(
            result,
            max_avg_time_ms=config.MAX_WAIT_TIME_MS,
            max_p95_time_ms=config.MAX_WAIT_TIME_MS,
            max_p99_time_ms=config.MAX_WAIT_TIME_MS,
        )

        assert passed, "PERF-THPT-01 未满足性能要求"

    @pytest.mark.performance
    def test_perf_thpt_02_concurrency_9(self):
        """测试用例: PERF-THPT-02 - 并发 9"""
        self.log_test_case("PERF-THPT-02", "并发 9 吞吐/延迟")

        concurrency = (
            TestData.PERFORMANCE_TEST_CONCURRENCY[1]
            if len(TestData.PERFORMANCE_TEST_CONCURRENCY) > 1
            else 9
        )

        result = perf_test.concurrent_test(
            func=self.get_books,
            concurrency=concurrency,
            iterations=TestData.PERFORMANCE_TEST_ITERATIONS,
        )

        passed = perf_test.validate_performance_requirement(
            result, max_avg_time_ms=config.MAX_WAIT_TIME_MS
        )
        assert passed, f"PERF-THPT-02 并发 {concurrency} 未满足性能要求"

    @pytest.mark.performance
    def test_perf_thpt_03_concurrency_10(self):
        """测试用例: PERF-THPT-03 - 并发 10"""
        self.log_test_case("PERF-THPT-03", "并发 10 吞吐/延迟")

        # 默认取 constants 中的第三个并发级别（若存在）或 10
        concurrency = (
            TestData.PERFORMANCE_TEST_CONCURRENCY[2]
            if len(TestData.PERFORMANCE_TEST_CONCURRENCY) > 2
            else 10
        )

        result = perf_test.concurrent_test(
            func=self.get_books,
            concurrency=concurrency,
            iterations=TestData.PERFORMANCE_TEST_ITERATIONS,
        )

        passed = perf_test.validate_performance_requirement(
            result, max_avg_time_ms=config.MAX_WAIT_TIME_MS
        )
        assert passed, f"PERF-THPT-03 并发 {concurrency} 未满足性能要求"

    @pytest.mark.performance
    def test_perf_thpt_04_concurrency_11(self):
        """测试用例: PERF-THPT-04 - 并发 11"""
        self.log_test_case("PERF-THPT-04", "并发 11 吞吐/延迟")

        concurrency = (
            TestData.PERFORMANCE_TEST_CONCURRENCY[3]
            if len(TestData.PERFORMANCE_TEST_CONCURRENCY) > 3
            else 11
        )

        result = perf_test.concurrent_test(
            func=self.get_books,
            concurrency=concurrency,
            iterations=TestData.PERFORMANCE_TEST_ITERATIONS,
        )

        passed = perf_test.validate_performance_requirement(
            result, max_avg_time_ms=config.MAX_WAIT_TIME_MS
        )
        assert passed, f"PERF-THPT-04 并发 {concurrency} 未满足性能要求"


if __name__ == "__main__":
    pytest.main([__file__, "-q", "-m", "performance"])
