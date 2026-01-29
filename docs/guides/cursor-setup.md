# 🎯 Cursor IDE - Azure Web Search MCP Server 配置指南

## ✅ 安装完成！

你的 Azure Web Search 已经成功配置为 Cursor 的 MCP Server！

---

## 🚀 快速开始

### 配置已完成 ✓

配置文件位置：
```
C:\Users\wang\AppData\Roaming\Cursor\User\globalStorage\mcp.json
```

### 下一步操作

#### 1. 重启 Cursor IDE

**重要**：必须完全关闭 Cursor 并重新打开，MCP Server 才能生效。

- 关闭所有 Cursor 窗口
- 确保 Cursor 进程已完全退出（可以检查任务管理器）
- 重新启动 Cursor

#### 2. 开始使用

重启 Cursor 后，在与 AI 对话时，可以自然地要求搜索：

**示例 1：快速搜索**
```
Search for Python 3.12 new features
```
或
```
搜索 Python 3.12 的新特性
```

**示例 2：技术研究**
```
Search for the latest AI trends in 2026
```
或
```
研究 2026年 人工智能的最新趋势
```

**示例 3：地区特定搜索**
```
Search for AI regulations in the United States
```
或
```
搜索美国的人工智能监管政策
```

---

## 🔧 可用的工具

Cursor AI 现在可以自动使用以下 2 个工具：

### 1. **web_search_quick** ⚡⚡⚡
- **速度**：最快（几秒钟）
- **适用**：快速查询、新闻、时效性信息
- **示例**："搜索今天的科技新闻"

### 2. **web_search_agentic** ⚡⚡
- **速度**：中等（10-30秒）
- **适用**：复杂查询、需要分析
- **示例**："分析量子计算的应用前景"

---

## 💡 使用技巧

### 自然语言请求

Cursor AI 会自动判断何时需要使用 web search 工具。你可以：

✅ **直接请求**：
```
Search for...
搜索...
查找...
研究...
```

✅ **间接请求**：
```
What are the latest features in React 19?
（AI 会自动搜索最新信息）

帮我了解最新的 AI 监管政策
（AI 会自动进行搜索）
```

### 指定搜索模式

如果你想使用特定的搜索模式：

```
使用快速搜索查找...
使用智能搜索分析...
对...进行深入分析
```

### 地区特定搜索

可以指定地理位置：

```
Search for... in the United States
搜索中国地区的...
查找日本的...
```

---

## 🧪 验证安装

### 方法 1：检查配置文件

查看配置文件内容：

```powershell
# PowerShell
notepad $env:APPDATA\Cursor\User\globalStorage\mcp.json
```

应该看到 `azure-web-search` 配置。

### 方法 2：运行测试脚本

```powershell
cd D:\remote\web-search
python test_mcp_server.py
```

应该看到 4/5 或 5/5 测试通过。

### 方法 3：在 Cursor 中测试

重启 Cursor 后，尝试：

```
Search for "MCP protocol documentation"
```

如果 AI 返回了搜索结果，说明配置成功！

---

## 🐛 故障排查

### 问题 1：Cursor AI 没有使用 web search

**可能原因**：
- Cursor 没有完全重启
- 配置文件格式错误

**解决方案**：
1. 完全退出 Cursor（检查任务管理器）
2. 重新打开 Cursor
3. 检查配置文件：`notepad $env:APPDATA\Cursor\User\globalStorage\mcp.json`
4. 运行测试：`python test_mcp_server.py`

### 问题 2：工具调用失败

**可能原因**：
- .env 配置错误
- Azure OpenAI API 密钥无效

**解决方案**：
1. 检查 `.env` 文件：
   ```env
   AZURE_OPENAI_API_KEY=你的密钥
   AZURE_OPENAI_ENDPOINT=https://你的端点
   AZURE_OPENAI_MODEL=gpt-4o
   ```
2. 验证 API 密钥是否有效
3. 运行测试脚本诊断问题

### 问题 3：找不到 MCP Server

**可能原因**：
- Python 或 uv 不在 PATH 中
- 项目路径错误

**解决方案**：
1. 确保 Python 和 uv 已正确安装
2. 重新运行安装脚本：`.\install_mcp_cursor.ps1`
3. 检查项目路径是否正确

---

## 📚 配置文件说明

配置文件位置：
```
C:\Users\wang\AppData\Roaming\Cursor\User\globalStorage\mcp.json
```

配置内容：
```json
{
  "mcpServers": {
    "azure-web-search": {
      "command": "uv",
      "args": [
        "--directory",
        "D:\\remote\\web-search",
        "run",
        "python",
        "mcp_server.py"
      ],
      "env": {
        "PYTHONPATH": "D:\\remote\\web-search"
      }
    }
  }
}
```

---

## 🔄 重新配置

如果需要重新配置，运行：

```powershell
cd D:\remote\web-search
.\install_mcp_cursor.ps1
```

---

## 📊 工具参数说明

### web_search_quick / web_search_agentic
- `query` (必需): 搜索查询字符串
- `country` (可选): 国家代码，如 `US`, `CN`, `JP`

## 💰 费用提醒

⚠️ **重要提示**：

- Web Search 功能会产生费用
- 每次搜索调用都会计入 Azure OpenAI 账单
- 快速搜索最经济
- 建议在 Azure Portal 设置费用警报

---

## 🎯 使用场景示例

### 开发相关
```
Search for React 19 new features
搜索 TypeScript 5.0 的新特性
查找 Python 异步编程最佳实践
```

### 技术研究
```
Research the latest advancements in quantum computing
研究大语言模型的安全性问题
分析区块链在供应链中的应用
```

### 新闻和资讯
```
Search for today's tech news
搜索今天的 AI 新闻
查找最新的科技动态
```

### 学术研究
```
Deep research on machine learning interpretability
对可解释 AI 进行深入分析
研究神经网络的可解释性
```

---

## 📖 更多资源

- **项目文档**: [README.md](README.md)
- **MCP 协议**: https://modelcontextprotocol.io/
- **Azure OpenAI 文档**: https://learn.microsoft.com/azure/ai-foundry/openai/how-to/web-search

---

## 🎉 享受使用！

现在你可以在 Cursor 中享受强大的 Azure Web Search 功能了！

- ✅ 实时搜索最新信息
- ✅ 自动引用来源
- ✅ 支持多种搜索模式
- ✅ 地理位置定制
- ✅ 自然语言交互

**记得重启 Cursor IDE！** 🚀

---

**有问题？** 运行 `python test_mcp_server.py` 诊断问题
