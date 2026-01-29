# 🤖 Azure Web Search MCP Server

将 Azure OpenAI Web Search 作为 Claude Desktop 的强大工具！

## 🎯 什么是 MCP Server？

Model Context Protocol (MCP) 是一个开放协议，允许 AI 助手（如 Claude）连接到外部工具和数据源。通过将此项目配置为 MCP Server，Claude Desktop 可以直接调用 Azure Web Search 功能。

## ✨ 主要优势

- **无缝集成**: 在 Claude 对话中自然使用 Web Search
- **三种模式**: 快速搜索、智能搜索、深度研究
- **地理定位**: 支持按国家/地区搜索
- **自动引用**: 所有搜索结果都包含来源引用
- **一键安装**: 自动化安装脚本

## 🚀 5 分钟快速开始

### 第 1 步：安装依赖

```powershell
# Windows PowerShell
cd D:\remote\web-search
uv pip install -e .
```

### 第 2 步：配置环境

确保 `.env` 文件包含你的 Azure OpenAI 配置：

```env
AZURE_OPENAI_API_KEY=你的密钥
AZURE_OPENAI_ENDPOINT=https://你的资源.openai.azure.com
AZURE_OPENAI_MODEL=gpt-4o
```

### 第 3 步：运行安装脚本

```powershell
# Windows
.\install_mcp.ps1
```

```bash
# macOS/Linux
chmod +x install_mcp.sh
./install_mcp.sh
```

### 第 4 步：验证安装

```bash
python test_mcp_server.py
```

所有测试通过 (5/5) ✅

### 第 5 步：使用！

1. 重启 Claude Desktop
2. 在对话中尝试：
   ```
   使用 web search 搜索 "2026年人工智能发展趋势"
   ```

## 🔧 可用工具

### 1️⃣ web_search_quick - 快速搜索
```
搜索今天的科技新闻
```
- ⚡ 最快（几秒钟）
- 📝 适合时效性信息

### 2️⃣ web_search_agentic - 智能搜索
```
分析人工智能在医疗领域的应用
```
- 🧠 带推理能力
- 📝 适合复杂查询

### 3️⃣ web_search_deep - 深度研究
```
对量子计算的最新进展进行深度研究
```
- 📚 最深入（数分钟）
- 📝 适合学术研究

## 📖 使用示例

### 基础搜索
```
使用 web search 查找 Python 3.12 的新特性
```

### 地区特定搜索
```
搜索美国地区关于 AI regulations 的信息
```

### 深度研究
```
对 "区块链在供应链管理中的应用" 进行深度研究
```

## 🛠️ 技术架构

```
Claude Desktop
     ↓ (MCP Protocol)
mcp_server.py
     ↓ (Python API)
AzureWebSearch
     ↓ (HTTP/REST)
Azure OpenAI API
     ↓ (Bing Grounding)
Web Search Results
```

## 📁 文件说明

| 文件 | 说明 |
|------|------|
| `mcp_server.py` | MCP Server 主程序 |
| `install_mcp.ps1` / `.sh` | 自动安装脚本 |
| `test_mcp_server.py` | 配置验证脚本 |
| `MCP_SETUP.md` | 详细配置指南 |
| `QUICKSTART_MCP.md` | 快速开始指南 |
| `claude_desktop_config.json` | 配置模板 |

## 🐛 故障排查

### 问题：Claude 找不到工具

**解决方案：**
1. 完全退出 Claude Desktop（检查任务管理器）
2. 重新启动 Claude Desktop
3. 运行测试：`python test_mcp_server.py`

### 问题：工具调用失败

**解决方案：**
1. 验证 `.env` 配置
2. 检查 API 密钥有效性
3. 查看日志输出

### 问题：依赖安装失败

**解决方案：**
```bash
uv pip install --force-reinstall -e .
```

## 📚 更多资源

- **详细指南**: [MCP_SETUP.md](MCP_SETUP.md)
- **快速开始**: [QUICKSTART_MCP.md](QUICKSTART_MCP.md)
- **项目文档**: [README.md](README.md)
- **MCP 协议**: https://modelcontextprotocol.io/

## 🔐 安全提示

- ⚠️ 不要提交 `.env` 文件到版本控制
- 💰 Web Search 功能会产生费用
- 🔄 定期轮换 API 密钥
- 📊 建议设置 Azure 费用警报

## 🎉 开始使用

现在你可以在 Claude Desktop 中享受强大的 Azure Web Search 功能了！

有问题？查看 [MCP_SETUP.md](MCP_SETUP.md) 的故障排查部分。

---

**Made with ❤️ for Claude Desktop**
