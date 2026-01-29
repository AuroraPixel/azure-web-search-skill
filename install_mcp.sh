#!/bin/bash
# Azure Web Search MCP Server 安装脚本（macOS/Linux）
# 此脚本将自动配置 Claude Desktop 以使用此 MCP Server

set -e

PROJECT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "========================================"
echo "  Azure Web Search MCP Server 安装程序"
echo "========================================"
echo ""

# 1. 检查依赖
echo "[1/5] 检查依赖..."

# 检查 uv
if command -v uv &> /dev/null; then
    UV_VERSION=$(uv --version)
    echo "  ✓ uv 已安装: $UV_VERSION"
else
    echo "  ✗ 错误：未找到 uv"
    echo "  请先安装 uv: https://github.com/astral-sh/uv"
    exit 1
fi

# 检查 Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "  ✓ Python 已安装: $PYTHON_VERSION"
else
    echo "  ✗ 错误：未找到 Python"
    echo "  请先安装 Python 3.10 或更高版本"
    exit 1
fi

# 2. 安装依赖包
echo ""
echo "[2/5] 安装 Python 依赖..."
cd "$PROJECT_PATH"
uv pip install -e .
echo "  ✓ 依赖安装完成"

# 3. 检查 .env 文件
echo ""
echo "[3/5] 检查配置文件..."
if [ -f "$PROJECT_PATH/.env" ]; then
    echo "  ✓ .env 文件已存在"
else
    echo "  ⚠ .env 文件不存在"
    if [ -f "$PROJECT_PATH/env.example" ]; then
        cp "$PROJECT_PATH/env.example" "$PROJECT_PATH/.env"
        echo "  ✓ 已从 env.example 创建 .env 文件"
        echo "  ⚠ 请编辑 .env 文件，填写你的 Azure OpenAI 配置！"
    else
        echo "  ✗ env.example 文件不存在"
        exit 1
    fi
fi

# 4. 配置 Claude Desktop
echo ""
echo "[4/5] 配置 Claude Desktop..."

# 确定配置文件路径
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    CLAUDE_CONFIG_PATH="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
else
    # Linux
    CLAUDE_CONFIG_PATH="$HOME/.config/Claude/claude_desktop_config.json"
fi

CLAUDE_CONFIG_DIR=$(dirname "$CLAUDE_CONFIG_PATH")

# 创建目录（如果不存在）
mkdir -p "$CLAUDE_CONFIG_DIR"
echo "  ✓ Claude 配置目录已准备"

# 创建或更新配置
if [ -f "$CLAUDE_CONFIG_PATH" ]; then
    echo "  ✓ 找到现有的 Claude 配置文件"
    # 备份现有配置
    cp "$CLAUDE_CONFIG_PATH" "$CLAUDE_CONFIG_PATH.backup"
    echo "  ✓ 已备份现有配置"
fi

# 生成新配置（使用 Python 来处理 JSON）
python3 << EOF
import json
import os

config_path = "$CLAUDE_CONFIG_PATH"
project_path = "$PROJECT_PATH"

# 读取现有配置
config = {}
if os.path.exists(config_path):
    with open(config_path, 'r') as f:
        config = json.load(f)

# 确保 mcpServers 存在
if 'mcpServers' not in config:
    config['mcpServers'] = {}

# 添加或更新我们的服务器
config['mcpServers']['azure-web-search'] = {
    'command': 'uv',
    'args': [
        '--directory',
        project_path,
        'run',
        'python',
        'mcp_server.py'
    ],
    'env': {
        'PYTHONPATH': project_path
    }
}

# 保存配置
with open(config_path, 'w') as f:
    json.dump(config, f, indent=2)

print("  ✓ Claude Desktop 配置已更新")
print(f"    配置文件位置: {config_path}")
EOF

# 5. 完成
echo ""
echo "[5/5] 安装完成！"
echo ""
echo "========================================"
echo "  下一步操作"
echo "========================================"
echo ""
echo "1. 确保 .env 文件已正确配置（包含 Azure OpenAI API 密钥）"
echo "2. 重启 Claude Desktop 应用"
echo "3. 在 Claude 中尝试以下命令："
echo "   '使用 web search 搜索 2026年人工智能发展趋势'"
echo ""
echo "📚 更多信息请查看：MCP_SETUP.md"
echo ""
echo "如遇问题，请检查："
echo "  • .env 文件配置是否正确"
echo "  • Claude Desktop 是否已完全重启"
echo "  • 项目路径是否正确: $PROJECT_PATH"
echo ""
