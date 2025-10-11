"""
性能测试工具
提供并发测试、响应时间测试等功能
"""

import time
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, List, Dict, Any
from logger import get_logger

logger = get_logger(__name__)


class PerformanceTest:
    """性能测试工具类"""
    
    def __init__(self):
        self.results = []
    
    def concurrent_test(
        self, 
        func: Callable, 
        concurrency: int = 1, 
        iterations: int = 1,
        *args, 
        **kwargs
    ) -> Dict[str, Any]:
        """
        并发测试
        
        Args:
            func: 要测试的函数
            concurrency: 并发数
            iterations: 每次测试的迭代次数（取平均值）
            *args: 函数位置参数
            **kwargs: 函数关键字参数
        
        Returns:
            性能测试结果字典
        """
        logger.info(f"开始并发测试 - 并发数: {concurrency}, 迭代次数: {iterations}")
        
        all_durations = []
        
        for iteration in range(iterations):
            logger.info(f"执行第 {iteration + 1}/{iterations} 次迭代")
            
            durations = []
            
            with ThreadPoolExecutor(max_workers=concurrency) as executor:
                # 提交并发任务
                futures = []
                start_time = time.time()
                
                for i in range(concurrency):
                    future = executor.submit(self._timed_execution, func, *args, **kwargs)
                    futures.append(future)
                
                # 等待所有任务完成并收集结果
                for future in as_completed(futures):
                    try:
                        duration = future.result()
                        durations.append(duration)
                    except Exception as e:
                        logger.error(f"任务执行失败: {str(e)}")
                
                total_time = time.time() - start_time
            
            # 记录本次迭代结果
            all_durations.extend(durations)
            
            logger.info(f"第 {iteration + 1} 次迭代完成 - 总耗时: {total_time:.4f}秒")
        
        # 计算统计数据
        result = self._calculate_statistics(all_durations, concurrency, iterations)
        
        # 打印结果
        self._print_results(result)
        
        return result
    
    def _timed_execution(self, func: Callable, *args, **kwargs) -> float:
        """
        执行函数并测量时间
        
        Args:
            func: 要执行的函数
            *args: 位置参数
            **kwargs: 关键字参数
        
        Returns:
            执行时间（毫秒）
        """
        start_time = time.time()
        try:
            func(*args, **kwargs)
        except Exception as e:
            logger.error(f"函数执行出错: {str(e)}")
            raise
        end_time = time.time()
        
        duration_ms = (end_time - start_time) * 1000
        return duration_ms
    
    def _calculate_statistics(
        self, 
        durations: List[float], 
        concurrency: int, 
        iterations: int
    ) -> Dict[str, Any]:
        """
        计算统计数据
        
        Args:
            durations: 响应时间列表（毫秒）
            concurrency: 并发数
            iterations: 迭代次数
        
        Returns:
            统计结果字典
        """
        if not durations:
            return {
                "error": "没有可用的测试数据"
            }
        
        result = {
            "concurrency": concurrency,
            "iterations": iterations,
            "total_requests": len(durations),
            "min_time_ms": min(durations),
            "max_time_ms": max(durations),
            "avg_time_ms": statistics.mean(durations),
            "median_time_ms": statistics.median(durations),
            "std_dev_ms": statistics.stdev(durations) if len(durations) > 1 else 0,
            "all_durations": durations
        }
        
        # 计算百分位数
        sorted_durations = sorted(durations)
        result["p50_ms"] = self._percentile(sorted_durations, 50)
        result["p90_ms"] = self._percentile(sorted_durations, 90)
        result["p95_ms"] = self._percentile(sorted_durations, 95)
        result["p99_ms"] = self._percentile(sorted_durations, 99)
        
        return result
    
    def _percentile(self, data: List[float], percentile: int) -> float:
        """
        计算百分位数
        
        Args:
            data: 已排序的数据列表
            percentile: 百分位（0-100）
        
        Returns:
            百分位数值
        """
        if not data:
            return 0
        
        k = (len(data) - 1) * percentile / 100
        f = int(k)
        c = f + 1 if f < len(data) - 1 else f
        
        if f == c:
            return data[f]
        
        d0 = data[f] * (c - k)
        d1 = data[c] * (k - f)
        return d0 + d1
    
    def _print_results(self, result: Dict[str, Any]):
        """
        打印测试结果
        
        Args:
            result: 测试结果字典
        """
        logger.info("=" * 80)
        logger.info("性能测试结果:")
        logger.info("-" * 80)
        logger.info(f"并发数: {result.get('concurrency', 'N/A')}")
        logger.info(f"迭代次数: {result.get('iterations', 'N/A')}")
        logger.info(f"总请求数: {result.get('total_requests', 'N/A')}")
        logger.info(f"最小响应时间: {result.get('min_time_ms', 0):.2f} ms")
        logger.info(f"最大响应时间: {result.get('max_time_ms', 0):.2f} ms")
        logger.info(f"平均响应时间: {result.get('avg_time_ms', 0):.2f} ms")
        logger.info(f"中位数响应时间: {result.get('median_time_ms', 0):.2f} ms")
        logger.info(f"标准差: {result.get('std_dev_ms', 0):.2f} ms")
        logger.info(f"P50: {result.get('p50_ms', 0):.2f} ms")
        logger.info(f"P90: {result.get('p90_ms', 0):.2f} ms")
        logger.info(f"P95: {result.get('p95_ms', 0):.2f} ms")
        logger.info(f"P99: {result.get('p99_ms', 0):.2f} ms")
        logger.info("=" * 80)
    
    def batch_concurrent_test(
        self,
        func: Callable,
        concurrency_levels: List[int],
        iterations: int = 10,
        *args,
        **kwargs
    ) -> Dict[int, Dict[str, Any]]:
        """
        批量并发测试（测试不同的并发级别）
        
        Args:
            func: 要测试的函数
            concurrency_levels: 并发级别列表
            iterations: 每个级别的迭代次数
            *args: 函数位置参数
            **kwargs: 函数关键字参数
        
        Returns:
            各并发级别的测试结果
        """
        results = {}
        
        for concurrency in concurrency_levels:
            logger.info(f"\n开始测试并发级别: {concurrency}")
            result = self.concurrent_test(
                func, 
                concurrency=concurrency, 
                iterations=iterations,
                *args, 
                **kwargs
            )
            results[concurrency] = result
            
            # 等待一下，避免对服务器造成过大压力
            time.sleep(1)
        
        # 打印对比结果
        self._print_comparison(results)
        
        return results
    
    def _print_comparison(self, results: Dict[int, Dict[str, Any]]):
        """
        打印不同并发级别的对比结果
        
        Args:
            results: 测试结果字典
        """
        logger.info("\n" + "=" * 80)
        logger.info("并发测试对比结果:")
        logger.info("=" * 80)
        logger.info(f"{'并发数':<10} {'平均(ms)':<12} {'最大(ms)':<12} {'P95(ms)':<12} {'P99(ms)':<12}")
        logger.info("-" * 80)
        
        for concurrency, result in sorted(results.items()):
            logger.info(
                f"{concurrency:<10} "
                f"{result.get('avg_time_ms', 0):<12.2f} "
                f"{result.get('max_time_ms', 0):<12.2f} "
                f"{result.get('p95_ms', 0):<12.2f} "
                f"{result.get('p99_ms', 0):<12.2f}"
            )
        
        logger.info("=" * 80)
    
    def validate_performance_requirement(
        self,
        result: Dict[str, Any],
        max_avg_time_ms: float = 5000,
        max_p95_time_ms: float = 5000,
        max_p99_time_ms: float = 5000
    ) -> bool:
        """
        验证性能是否满足要求
        
        Args:
            result: 性能测试结果
            max_avg_time_ms: 平均响应时间要求（毫秒）
            max_p95_time_ms: P95响应时间要求（毫秒）
            max_p99_time_ms: P99响应时间要求（毫秒）
        
        Returns:
            是否满足要求
        """
        avg_time = result.get('avg_time_ms', float('inf'))
        p95_time = result.get('p95_ms', float('inf'))
        p99_time = result.get('p99_ms', float('inf'))
        
        passed = (
            avg_time <= max_avg_time_ms and
            p95_time <= max_p95_time_ms and
            p99_time <= max_p99_time_ms
        )
        
        logger.info(f"\n性能要求验证: {'✓ 通过' if passed else '✗ 失败'}")
        logger.info(f"平均响应时间: {avg_time:.2f}ms <= {max_avg_time_ms}ms ? "
                   f"{'✓' if avg_time <= max_avg_time_ms else '✗'}")
        logger.info(f"P95响应时间: {p95_time:.2f}ms <= {max_p95_time_ms}ms ? "
                   f"{'✓' if p95_time <= max_p95_time_ms else '✗'}")
        logger.info(f"P99响应时间: {p99_time:.2f}ms <= {max_p99_time_ms}ms ? "
                   f"{'✓' if p99_time <= max_p99_time_ms else '✗'}")
        
        return passed


# 创建全局性能测试实例
perf_test = PerformanceTest()
