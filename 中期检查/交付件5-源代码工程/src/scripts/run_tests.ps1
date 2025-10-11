# 快速运行测试脚本

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  软件质量测试 - 快速运行" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 菜单
Write-Host "请选择要运行的测试:" -ForegroundColor Yellow
Write-Host "  1. 运行示例测试 (test_example.py)" -ForegroundColor White
Write-Host "  2. 运行性能测试 (test_performance_example.py)" -ForegroundColor White
Write-Host "  3. 运行所有测试" -ForegroundColor White
Write-Host "  4. 运行测试并生成HTML报告" -ForegroundColor White
Write-Host "  5. 退出" -ForegroundColor White
Write-Host ""

$choice = Read-Host "请输入选项 (1-5)"

switch ($choice) {
    "1" {
        Write-Host "`n运行示例测试..." -ForegroundColor Green
        pytest test_example.py -v -s
    }
    "2" {
        Write-Host "`n运行性能测试..." -ForegroundColor Green
        pytest test_performance_example.py -v -s -m performance
    }
    "3" {
        Write-Host "`n运行所有测试..." -ForegroundColor Green
        pytest -v -s
    }
    "4" {
        Write-Host "`n运行测试并生成报告..." -ForegroundColor Green
        $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
        $reportPath = "..\outputs\reports\report_$timestamp.html"
        pytest -v --html=$reportPath --self-contained-html
        
        if (Test-Path $reportPath) {
            Write-Host "`n✓ 报告已生成: $reportPath" -ForegroundColor Green
            Write-Host "是否打开报告? (Y/N)" -ForegroundColor Yellow
            $open = Read-Host
            if ($open -eq "Y" -or $open -eq "y") {
                Start-Process $reportPath
            }
        }
    }
    "5" {
        Write-Host "`n退出" -ForegroundColor Gray
        exit 0
    }
    default {
        Write-Host "`n无效选项" -ForegroundColor Red
    }
}

Write-Host "`n按任意键退出..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
