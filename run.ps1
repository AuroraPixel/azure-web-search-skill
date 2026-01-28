# 快速启动脚本 - Azure Web Search

Write-Host "🚀 启动 Azure Web Search..." -ForegroundColor Cyan

# 检查虚拟环境
if (-Not (Test-Path ".venv")) {
    Write-Host "❌ 未找到虚拟环境" -ForegroundColor Red
    Write-Host "💡 请先运行 setup.ps1 安装项目" -ForegroundColor Yellow
    Write-Host ""
    $runSetup = Read-Host "是否现在运行安装脚本？(y/n)"
    if ($runSetup -eq "y" -or $runSetup -eq "Y") {
        .\setup.ps1
    }
    exit
}

# 检查 .env 文件
if (-Not (Test-Path ".env")) {
    Write-Host "❌ 未找到 .env 配置文件" -ForegroundColor Red
    Write-Host "💡 请先复制 env.example 为 .env 并填写配置" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "命令：" -ForegroundColor Cyan
    Write-Host "  copy env.example .env" -ForegroundColor White
    Write-Host "  然后编辑 .env 文件填写您的 Azure OpenAI 配置" -ForegroundColor White
    exit
}

# 激活虚拟环境并运行主程序
& .\.venv\Scripts\Activate.ps1
Write-Host "✅ 虚拟环境已激活" -ForegroundColor Green
Write-Host ""

# 运行主程序
python main.py
