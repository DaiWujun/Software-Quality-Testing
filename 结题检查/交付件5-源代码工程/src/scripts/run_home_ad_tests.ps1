# 运行主页广告测试
# 此脚本用于快速运行 HOME-AD 系列测试

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  主页广告测试 (HOME-AD)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查Python环境
Write-Host "检查Python环境..." -ForegroundColor Yellow
python --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "错误: 未找到Python" -ForegroundColor Red
    exit 1
}

# 检查pytest
Write-Host "检查pytest..." -ForegroundColor Yellow
python -c "import pytest" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "错误: 未找到pytest，请先运行 setup.ps1 安装依赖" -ForegroundColor Red
    exit 1
}

Write-Host "✓ 环境检查通过" -ForegroundColor Green
Write-Host ""

# 显示菜单
Write-Host "请选择测试选项:" -ForegroundColor Yellow
Write-Host "  1. 运行所有 HOME-AD 测试" -ForegroundColor White
Write-Host "  2. HOME-AD-01: 展示广告" -ForegroundColor White
Write-Host "  3. HOME-AD-02: 广告跳转" -ForegroundColor White
Write-Host "  4. HOME-AD-03: 切换广告" -ForegroundColor White
Write-Host "  5. HOME-AD-04: 广告编辑" -ForegroundColor White
Write-Host "  6. HOME-AD-05: CRUD操作（扩展）" -ForegroundColor White
Write-Host "  7. 生成HTML测试报告" -ForegroundColor White
Write-Host "  8. 退出" -ForegroundColor White
Write-Host ""

$choice = Read-Host "请输入选项 (1-8)"

switch ($choice) {
    "1" {
        Write-Host "`n运行所有 HOME-AD 测试..." -ForegroundColor Green
        pytest test_home_ad.py -v -s --tb=short
    }
    "2" {
        Write-Host "`n运行 HOME-AD-01: 展示广告..." -ForegroundColor Green
        pytest test_home_ad.py::TestHomeAdvertisement::test_home_ad_01_display_advertisement -v -s
    }
    "3" {
        Write-Host "`n运行 HOME-AD-02: 广告跳转..." -ForegroundColor Green
        pytest test_home_ad.py::TestHomeAdvertisement::test_home_ad_02_advertisement_navigation -v -s
    }
    "4" {
        Write-Host "`n运行 HOME-AD-03: 切换广告..." -ForegroundColor Green
        pytest test_home_ad.py::TestHomeAdvertisement::test_home_ad_03_switch_advertisement -v -s
    }
    "5" {
        Write-Host "`n运行 HOME-AD-04: 广告编辑..." -ForegroundColor Green
        pytest test_home_ad.py::TestHomeAdvertisement::test_home_ad_04_edit_advertisement -v -s
    }
    "6" {
        Write-Host "`n运行 HOME-AD-05: CRUD操作..." -ForegroundColor Green
        pytest test_home_ad.py::TestHomeAdvertisement::test_home_ad_05_advertisement_crud_operations -v -s
    }
    "7" {
        Write-Host "`n生成HTML测试报告..." -ForegroundColor Green
        $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
        $reportPath = "..\outputs\reports\home_ad_report_$timestamp.html"
        
        # 确保目录存在
        $reportDir = Split-Path -Parent $reportPath
        if (!(Test-Path $reportDir)) {
            New-Item -ItemType Directory -Path $reportDir -Force | Out-Null
        }
        
        pytest test_home_ad.py -v --html=$reportPath --self-contained-html
        
        if (Test-Path $reportPath) {
            Write-Host "`n✓ 报告已生成: $reportPath" -ForegroundColor Green
            Write-Host "是否打开报告? (Y/N)" -ForegroundColor Yellow
            $open = Read-Host
            if ($open -eq "Y" -or $open -eq "y") {
                Start-Process $reportPath
            }
        }
    }
    "8" {
        Write-Host "`n退出" -ForegroundColor Gray
        exit 0
    }
    default {
        Write-Host "`n无效选项" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "测试执行完成" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "日志文件位置: ..\outputs\logs\" -ForegroundColor Gray
Write-Host "查看详细文档: TEST_HOME_AD_README.md" -ForegroundColor Gray
Write-Host ""

# 询问是否查看日志
Write-Host "是否查看最新日志文件? (Y/N)" -ForegroundColor Yellow
$viewLog = Read-Host
if ($viewLog -eq "Y" -or $viewLog -eq "y") {
    $logDir = "..\outputs\logs"
    if (Test-Path $logDir) {
        $latestLog = Get-ChildItem $logDir -Filter "test_*.log" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
        if ($latestLog) {
            Write-Host "`n最新日志: $($latestLog.FullName)" -ForegroundColor Cyan
            Get-Content $latestLog.FullName -Tail 50
        }
    }
}

Write-Host "`n按任意键退出..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
