# Azure Web Search MCP Server 安装脚本
# 此脚本将自动配置 Claude Desktop 以使用此 MCP Server

param(
    [string]$ProjectPath = $PSScriptRoot
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Azure Web Search MCP Server 安装程序" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. 检查依赖
Write-Host "[1/5] 检查依赖..." -ForegroundColor Yellow

# 检查 uv
try {
    $uvVersion = uv --version
    Write-Host "  ✓ uv 已安装: $uvVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ 错误：未找到 uv" -ForegroundColor Red
    Write-Host "  请先安装 uv: https://github.com/astral-sh/uv" -ForegroundColor Yellow
    exit 1
}

# 检查 Python
try {
    $pythonVersion = python --version
    Write-Host "  ✓ Python 已安装: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ 错误：未找到 Python" -ForegroundColor Red
    Write-Host "  请先安装 Python 3.10 或更高版本" -ForegroundColor Yellow
    exit 1
}

# 2. 安装依赖包
Write-Host ""
Write-Host "[2/5] 安装 Python 依赖..." -ForegroundColor Yellow
Push-Location $ProjectPath
try {
    uv pip install -e .
    Write-Host "  ✓ 依赖安装完成" -ForegroundColor Green
} catch {
    Write-Host "  ✗ 依赖安装失败" -ForegroundColor Red
    Pop-Location
    exit 1
}
Pop-Location

# 3. 检查 .env 文件
Write-Host ""
Write-Host "[3/5] 检查配置文件..." -ForegroundColor Yellow
$envFile = Join-Path $ProjectPath ".env"
if (Test-Path $envFile) {
    Write-Host "  ✓ .env 文件已存在" -ForegroundColor Green
} else {
    Write-Host "  ⚠ .env 文件不存在" -ForegroundColor Yellow
    $envExample = Join-Path $ProjectPath "env.example"
    if (Test-Path $envExample) {
        Copy-Item $envExample $envFile
        Write-Host "  ✓ 已从 env.example 创建 .env 文件" -ForegroundColor Green
        Write-Host "  ⚠ 请编辑 .env 文件，填写你的 Azure OpenAI 配置！" -ForegroundColor Yellow
    } else {
        Write-Host "  ✗ env.example 文件不存在" -ForegroundColor Red
        exit 1
    }
}

# 4. 查找 Claude Desktop 配置文件
Write-Host ""
Write-Host "[4/5] 配置 Claude Desktop..." -ForegroundColor Yellow

$claudeConfigPath = Join-Path $env:APPDATA "Claude\claude_desktop_config.json"
$claudeConfigDir = Split-Path $claudeConfigPath -Parent

# 创建目录（如果不存在）
if (-not (Test-Path $claudeConfigDir)) {
    New-Item -ItemType Directory -Path $claudeConfigDir -Force | Out-Null
    Write-Host "  ✓ 创建了 Claude 配置目录" -ForegroundColor Green
}

# 转换路径为 JSON 格式（Windows 路径需要双反斜杠）
$jsonPath = $ProjectPath -replace '\\', '\\'

# 准备 MCP 服务器配置
$mcpServerConfig = @{
    "azure-web-search" = @{
        command = "uv"
        args = @(
            "--directory",
            $ProjectPath,
            "run",
            "python",
            "bin/mcp_server.py"
        )
        env = @{
            PYTHONPATH = $ProjectPath
            # 让 FastMCP Skills Provider 在 Windows 上按 UTF-8 读取 SKILL.md（避免 gbk 解码失败）
            PYTHONUTF8 = "1"
            PYTHONIOENCODING = "utf-8"
        }
    }
}

# 读取或创建配置文件
$config = @{}
if (Test-Path $claudeConfigPath) {
    Write-Host "  ✓ 找到现有的 Claude 配置文件" -ForegroundColor Green
    $existingConfig = Get-Content $claudeConfigPath -Raw | ConvertFrom-Json -AsHashtable
    if ($existingConfig.mcpServers) {
        $config = $existingConfig
    } else {
        $config = @{ mcpServers = @{} }
    }
} else {
    Write-Host "  ✓ 创建新的 Claude 配置文件" -ForegroundColor Green
    $config = @{ mcpServers = @{} }
}

# 添加或更新我们的 MCP 服务器
$config.mcpServers["azure-web-search"] = $mcpServerConfig["azure-web-search"]

# 保存配置文件
try {
    $config | ConvertTo-Json -Depth 10 | Set-Content $claudeConfigPath -Encoding UTF8
    Write-Host "  ✓ Claude Desktop 配置已更新" -ForegroundColor Green
    Write-Host "    配置文件位置: $claudeConfigPath" -ForegroundColor Gray
} catch {
    Write-Host "  ✗ 无法写入配置文件" -ForegroundColor Red
    Write-Host "    错误: $_" -ForegroundColor Red
    exit 1
}

# 5. 完成
Write-Host ""
Write-Host "[5/5] 安装完成！" -ForegroundColor Green
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  下一步操作" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. 确保 .env 文件已正确配置（包含 Azure OpenAI API 密钥）" -ForegroundColor White
Write-Host "2. 重启 Claude Desktop 应用" -ForegroundColor White
Write-Host "3. 在 Claude 中尝试以下命令：" -ForegroundColor White
Write-Host "   '使用 web search 搜索 2026年人工智能发展趋势'" -ForegroundColor Cyan
Write-Host ""
Write-Host "📚 更多信息请查看：MCP_SETUP.md" -ForegroundColor Yellow
Write-Host ""
Write-Host "如遇问题，请检查：" -ForegroundColor Yellow
Write-Host "  • .env 文件配置是否正确" -ForegroundColor Gray
Write-Host "  • Claude Desktop 是否已完全重启" -ForegroundColor Gray
Write-Host "  • 项目路径是否正确: $ProjectPath" -ForegroundColor Gray
Write-Host ""
