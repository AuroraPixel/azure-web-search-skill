# Azure Web Search MCP Server - Cursor Configuration Script
# This script configures Cursor IDE to use this MCP Server

param(
    [string]$ProjectPath = $PSScriptRoot
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Azure Web Search MCP - Cursor Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check .env file
Write-Host "[1/3] Checking configuration..." -ForegroundColor Yellow
$envFile = Join-Path $ProjectPath ".env"
if (Test-Path $envFile) {
    Write-Host "  OK: .env file exists" -ForegroundColor Green
} else {
    Write-Host "  ERROR: .env file not found" -ForegroundColor Red
    Write-Host "  Please create .env file first!" -ForegroundColor Yellow
    exit 1
}

# Configure Cursor
Write-Host ""
Write-Host "[2/3] Configuring Cursor IDE..." -ForegroundColor Yellow

# Cursor MCP config path
$cursorConfigDir = Join-Path $env:APPDATA "Cursor\User\globalStorage"
$cursorMcpConfig = Join-Path $cursorConfigDir "mcp.json"

# Create directory if not exists
if (-not (Test-Path $cursorConfigDir)) {
    New-Item -ItemType Directory -Path $cursorConfigDir -Force | Out-Null
    Write-Host "  OK: Created Cursor config directory" -ForegroundColor Green
}

# Prepare MCP server configuration
$mcpConfig = @{
    mcpServers = @{
        "azure-web-search" = @{
            command = "uv"
            args = @(
                "--directory"
                $ProjectPath
                "run"
                "python"
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
}

# Read or create config file
$config = @{}
if (Test-Path $cursorMcpConfig) {
    Write-Host "  OK: Found existing Cursor MCP config" -ForegroundColor Green
    try {
        $existingConfig = Get-Content $cursorMcpConfig -Raw | ConvertFrom-Json -AsHashtable
        if ($existingConfig.mcpServers) {
            $config = $existingConfig
        } else {
            $config = $mcpConfig
        }
    }
    catch {
        Write-Host "  WARN: Existing config invalid, creating new one" -ForegroundColor Yellow
        $config = $mcpConfig
    }
} else {
    Write-Host "  OK: Creating new Cursor MCP config" -ForegroundColor Green
    $config = $mcpConfig
}

# Add or update our MCP server
if (-not $config.mcpServers) {
    $config.mcpServers = @{}
}
$config.mcpServers["azure-web-search"] = $mcpConfig.mcpServers["azure-web-search"]

# Save config file
try {
    $config | ConvertTo-Json -Depth 10 | Set-Content $cursorMcpConfig -Encoding UTF8
    Write-Host "  OK: Cursor MCP config updated" -ForegroundColor Green
    Write-Host "    Config file: $cursorMcpConfig" -ForegroundColor Gray
}
catch {
    Write-Host "  ERROR: Cannot write config file" -ForegroundColor Red
    Write-Host "    Error: $_" -ForegroundColor Red
    exit 1
}

# Done
Write-Host ""
Write-Host "[3/3] Installation complete!" -ForegroundColor Green
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Next Steps" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Restart Cursor IDE (completely close and reopen)" -ForegroundColor White
Write-Host ""
Write-Host "2. In Cursor, try asking the AI:" -ForegroundColor White
Write-Host "   'Search for Python 3.12 new features'" -ForegroundColor Cyan
Write-Host "   OR" -ForegroundColor Gray
Write-Host "   'Search for AI trends in 2026'" -ForegroundColor Cyan
Write-Host ""
Write-Host "3. Cursor AI will automatically use web search tools" -ForegroundColor White
Write-Host ""
Write-Host "Config location: $cursorMcpConfig" -ForegroundColor Gray
Write-Host ""
Write-Host "If you have issues, run: python test_mcp_server.py" -ForegroundColor Yellow
Write-Host ""
