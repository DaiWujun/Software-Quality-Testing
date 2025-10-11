# White-Jotter Test Environment Setup Script

Write-Host ""
Write-Host "" -ForegroundColor Cyan
Write-Host "     White-Jotter 测试环境设置                         " -ForegroundColor Cyan  
Write-Host "" -ForegroundColor Cyan
Write-Host ""

Write-Host "检查环境..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    $npmVersion = npm --version
    Write-Host " Node.js: $nodeVersion" -ForegroundColor Green
    Write-Host " npm: $npmVersion" -ForegroundColor Green
}
catch {
    Write-Host " 错误: 未找到 Node.js 或 npm" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "安装测试依赖..." -ForegroundColor Yellow
npm install --save-dev @vue/test-utils 2>&1 | Out-Null
Write-Host " 测试依赖检查完成" -ForegroundColor Green
Write-Host ""

function Show-TestMenu {
    Write-Host "请选择要执行的操作:" -ForegroundColor Cyan
    Write-Host "  1. 运行所有测试" -ForegroundColor White
    Write-Host "  2. 仅运行单元测试" -ForegroundColor White
    Write-Host "  3. 仅运行 E2E 测试" -ForegroundColor White
    Write-Host "  4. 运行单元测试（监听模式）" -ForegroundColor White
    Write-Host "  5. 查看测试覆盖率报告" -ForegroundColor White
    Write-Host "  6. 运行代码检查" -ForegroundColor White
    Write-Host "  0. 退出" -ForegroundColor White
    Write-Host ""
    $choice = Read-Host "请输入选项 (0-6)"
    return $choice
}

$continue = $true
while ($continue) {
    Write-Host ""
    Write-Host ("" * 60) -ForegroundColor Cyan
    $choice = Show-TestMenu
    
    switch ($choice) {
        "1" { node scripts/run-all-tests.js }
        "2" { npm run unit }
        "3" { npm run e2e }
        "4" { npm run unit:watch }
        "5" {
            $reportPath = "test\unit\coverage\lcov-report\index.html"
            if (Test-Path $reportPath) {
                Start-Process $reportPath
            }
            else {
                Write-Host " 未找到覆盖率报告" -ForegroundColor Red
            }
        }
        "6" { npm run lint }
        "0" { $continue = $false }
        default { Write-Host " 无效选项" -ForegroundColor Red }
    }
    
    if ($continue) {
        Write-Host ""
        Write-Host "按任意键继续..." -ForegroundColor Gray
        $null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')
    }
}
