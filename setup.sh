#!/bin/bash
# Azure Web Search 项目设置脚本（Bash）

echo "🚀 开始设置 Azure Web Search 项目..."

# 检查 uv 是否已安装
echo ""
echo "📦 检查 uv 是否已安装..."
if command -v uv &> /dev/null; then
    echo "✅ uv 已安装: $(uv --version)"
else
    echo "❌ 未找到 uv，正在安装..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    echo "✅ uv 安装完成"
fi

# 创建虚拟环境
echo ""
echo "🔧 创建虚拟环境..."
if [ -d ".venv" ]; then
    echo "⚠️  虚拟环境已存在，跳过创建"
else
    uv venv
    echo "✅ 虚拟环境创建完成"
fi

# 激活虚拟环境
echo ""
echo "✨ 激活虚拟环境..."
source .venv/bin/activate

# 安装依赖
echo ""
echo "📥 安装项目依赖..."
uv pip install -e .
echo "✅ 依赖安装完成"

# 安装开发依赖（可选）
echo ""
read -p "❓ 是否安装开发依赖（black, ruff, pytest）？(y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📥 安装开发依赖..."
    uv pip install -e ".[dev]"
    echo "✅ 开发依赖安装完成"
fi

# 设置环境变量文件
echo ""
echo "⚙️  设置环境变量..."
if [ -f ".env" ]; then
    echo "⚠️  .env 文件已存在，跳过创建"
else
    cp env.example .env
    echo "✅ 已创建 .env 文件，请编辑并填写您的配置"
    echo ""
    echo "📝 请在 .env 文件中填写以下配置："
    echo "   1. AZURE_OPENAI_API_KEY=你的API密钥"
    echo "   2. AZURE_OPENAI_ENDPOINT=https://你的资源名.openai.azure.com"
    echo "   3. AZURE_OPENAI_MODEL=gpt-4o"
    echo ""
    
    read -p "是否立即打开 .env 文件编辑？(y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        ${EDITOR:-nano} .env
    fi
fi

echo ""
echo "✅ 设置完成！"
echo ""
echo "🎯 下一步操作："
echo "   1. 编辑 .env 文件，填写 Azure OpenAI 配置"
echo "   2. 激活虚拟环境：source .venv/bin/activate"
echo "   3. 运行示例：python examples/basic_search.py"
echo "   4. 查看文档：README.md"
echo ""
