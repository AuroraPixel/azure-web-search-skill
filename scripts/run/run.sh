#!/bin/bash
# 快速启动脚本 - Azure Web Search

echo "🚀 启动 Azure Web Search..."

# 检查虚拟环境
if [ ! -d ".venv" ]; then
    echo "❌ 未找到虚拟环境"
    echo "💡 请先运行 setup.sh 安装项目"
    echo ""
    read -p "是否现在运行安装脚本？(y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        ./setup.sh
    fi
    exit 1
fi

# 检查 .env 文件
if [ ! -f ".env" ]; then
    echo "❌ 未找到 .env 配置文件"
    echo "💡 请先复制 env.example 为 .env 并填写配置"
    echo ""
    echo "命令："
    echo "  cp env.example .env"
    echo "  然后编辑 .env 文件填写您的 Azure OpenAI 配置"
    exit 1
fi

# 激活虚拟环境并运行主程序
source .venv/bin/activate
echo "✅ 虚拟环境已激活"
echo ""

# 运行主程序
python main.py
