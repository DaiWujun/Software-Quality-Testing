# 软件质量测试项目 - 环境安装脚本
# 运行此脚本以安装所有依赖

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  软件质量测试项目 - 环境配置" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查Python版本
Write-Host "1. 检查Python版本..." -ForegroundColor Yellow
python --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "错误: 未找到Python，请先安装Python 3.7+" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Python检查通过" -ForegroundColor Green
Write-Host ""

# 检查pip
Write-Host "2. 检查pip..." -ForegroundColor Yellow
pip --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "错误: 未找到pip" -ForegroundColor Red
    exit 1
}
Write-Host "✓ pip检查通过" -ForegroundColor Green
Write-Host ""

# 升级pip
Write-Host "3. 升级pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip
Write-Host "✓ pip升级完成" -ForegroundColor Green
Write-Host ""

# 安装依赖
Write-Host "4. 安装项目依赖..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "警告: 部分依赖安装失败，请手动检查" -ForegroundColor Yellow
} else {
    Write-Host "✓ 依赖安装完成" -ForegroundColor Green
}
Write-Host ""

# 创建输出目录
Write-Host "5. 创建输出目录..." -ForegroundColor Yellow
$outputDirs = @(
    "..\outputs\logs",
    "..\outputs\screenshots",
    "..\outputs\reports"
)

foreach ($dir in $outputDirs) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "  创建目录: $dir" -ForegroundColor Gray
    }
}
Write-Host "✓ 输出目录创建完成" -ForegroundColor Green
Write-Host ""

# 验证安装
Write-Host "6. 验证安装..." -ForegroundColor Yellow
Write-Host "  检查关键包..." -ForegroundColor Gray

$packages = @("pytest", "requests", "selenium")
$allInstalled = $true

foreach ($package in $packages) {
    python -c "import $package" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ $package" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $package 未安装" -ForegroundColor Red
        $allInstalled = $false
    }
}

Write-Host ""

# 最终结果
Write-Host "========================================" -ForegroundColor Cyan
if ($allInstalled) {
    Write-Host "  环境配置完成！" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "现在可以运行测试了:" -ForegroundColor Yellow
    Write-Host "  pytest test_example.py -v" -ForegroundColor White
    Write-Host "  pytest test_performance_example.py -v -m performance" -ForegroundColor White
    Write-Host ""
    Write-Host "生成HTML报告:" -ForegroundColor Yellow
    Write-Host "  pytest --html=..\outputs\reports\report.html" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host "  环境配置未完全成功" -ForegroundColor Yellow
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "请手动安装缺失的包:" -ForegroundColor Yellow
    Write-Host "  pip install pytest requests selenium" -ForegroundColor White
    Write-Host ""
}

Write-Host "查看完整文档: README.md" -ForegroundColor Cyan
Write-Host "查看配置总结: SETUP_SUMMARY.md" -ForegroundColor Cyan
Write-Host ""
