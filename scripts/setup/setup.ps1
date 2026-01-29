# Azure Web Search 项目设置脚本（PowerShell）

Write-Host "🚀 开始设置 Azure Web Search 项目..." -ForegroundColor Cyan

# 检查 uv 是否已安装
Write-Host "`n📦 检查 uv 是否已安装..." -ForegroundColor Yellow
try {
    $uvVersion = uv --version
    Write-Host "✅ uv 已安装: $uvVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ 未找到 uv，正在安装..." -ForegroundColor Red
    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    Write-Host "✅ uv 安装完成" -ForegroundColor Green
}

# 创建虚拟环境
Write-Host "`n🔧 创建虚拟环境..." -ForegroundColor Yellow
if (Test-Path ".venv") {
    Write-Host "⚠️  虚拟环境已存在，跳过创建" -ForegroundColor Yellow
} else {
    uv venv
    Write-Host "✅ 虚拟环境创建完成" -ForegroundColor Green
}

# 激活虚拟环境
Write-Host "`n✨ 激活虚拟环境..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1

# 安装依赖
Write-Host "`n📥 安装项目依赖..." -ForegroundColor Yellow
uv pip install -e .
Write-Host "✅ 依赖安装完成" -ForegroundColor Green

# 安装开发依赖（可选）
$installDev = Read-Host "`n❓ 是否安装开发依赖（black, ruff, pytest）？(y/n)"
if ($installDev -eq "y" -or $installDev -eq "Y") {
    Write-Host "📥 安装开发依赖..." -ForegroundColor Yellow
    uv pip install -e ".[dev]"
    Write-Host "✅ 开发依赖安装完成" -ForegroundColor Green
}

# 设置环境变量文件
Write-Host "`n⚙️  设置环境变量..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "⚠️  .env 文件已存在，跳过创建" -ForegroundColor Yellow
} else {
    Copy-Item "env.example" ".env"
    Write-Host "✅ 已创建 .env 文件，请编辑并填写您的配置" -ForegroundColor Green
    Write-Host ""
    Write-Host "📝 请在 .env 文件中填写以下配置：" -ForegroundColor Cyan
    Write-Host "   1. AZURE_OPENAI_API_KEY=你的API密钥" -ForegroundColor White
    Write-Host "   2. AZURE_OPENAI_ENDPOINT=https://你的资源名.openai.azure.com" -ForegroundColor White
    Write-Host "   3. AZURE_OPENAI_MODEL=gpt-4o" -ForegroundColor White
    Write-Host ""
    
    $openEnv = Read-Host "是否立即打开 .env 文件编辑？(y/n)"
    if ($openEnv -eq "y" -or $openEnv -eq "Y") {
        notepad .env
    }
}

Write-Host "`n✅ 设置完成！" -ForegroundColor Green
Write-Host ""
Write-Host "🎯 下一步操作：" -ForegroundColor Cyan
Write-Host "   1. 编辑 .env 文件，填写 Azure OpenAI 配置" -ForegroundColor White
Write-Host "   2. 运行示例：python examples/basic_search.py" -ForegroundColor White
Write-Host "   3. 查看文档：README.md" -ForegroundColor White
Write-Host ""
