# 🚀 MCP Server 快速开始指南

这是一个超级简化的指南，帮助你在 5 分钟内将 Azure Web Search 配置为 Claude Desktop 的工具。

## ⚡ 快速设置（3 步）

### 第 1 步：安装依赖

打开 PowerShell 或终端，运行：

```powershell
# Windows PowerShell
cd D:\remote\web-search
uv pip install -e .
```

```bash
# macOS/Linux
cd /path/to/web-search
uv pip install -e .
```

### 第 2 步：配置环境变量

确保 `.env` 文件存在并包含你的 Azure OpenAI 配置：

```env
AZURE_OPENAI_API_KEY=你的密钥
AZURE_OPENAI_ENDPOINT=https://你的资源.openai.azure.com
AZURE_OPENAI_MODEL=gpt-4o
```

### 第 3 步：运行安装脚本

```powershell
# Windows
.\scripts\install-mcp\claude.ps1
```

```bash
# macOS/Linux
bash scripts/install-mcp/claude.sh
```

## ✅ 验证安装

运行测试脚本：

```powershell
python test_mcp_server.py
```

如果所有测试通过 (5/5)，你已准备就绪！

## 🎯 使用

1. **重启 Claude Desktop**（完全退出并重新打开）

2. **在 Claude 中测试**：
   ```
   使用 web search 搜索 "2026年人工智能发展趋势"
   ```

3. **可用的搜索模式**：
   - 快速搜索：适合时效性查询
   - 智能搜索：适合需要推理的复杂查询

## 🔧 故障排查

### 问题：Claude 找不到工具

**解决**：
1. 确保完全退出 Claude Desktop（检查任务管理器）
2. 重新打开 Claude Desktop
3. 检查配置文件位置：
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

### 问题：工具调用失败

**解决**：
1. 检查 `.env` 文件配置
2. 验证 Azure OpenAI API 密钥
3. 运行测试脚本：`python test_mcp_server.py`

### 问题：依赖安装失败

**解决**：
```powershell
# 强制重新安装
uv pip install --force-reinstall -e .
```

## 📚 详细文档

需要更多信息？查看：
- [MCP_SETUP.md](MCP_SETUP.md) - 完整配置指南
- [README.md](README.md) - 项目文档

## 💡 示例用法

在 Claude Desktop 中尝试：

```
# 快速查询
搜索今天的科技新闻

# 地区特定
搜索美国地区的 AI 政策

# 深入分析
使用 azure_web_search（mode=agentic）分析量子计算的应用前景
```

---

**就这么简单！现在你可以在 Claude 中使用强大的 Azure Web Search 了。** 🎉
