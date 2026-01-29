# Azure Web Search MCP Server 设置指南

本指南将帮助你将 Azure Web Search 项目配置为 MCP (Model Context Protocol) Server，使其可以在 Claude Desktop 中作为工具使用。

## 📋 前置要求

1. **Python 3.10+** 已安装
2. **uv** 包管理器已安装
3. **Claude Desktop** 应用已安装
4. **Azure OpenAI** 账户和 API 密钥

## 🚀 快速设置

### 步骤 1：安装依赖

首先确保安装了所有必需的依赖，包括新添加的 MCP 包：

```powershell
# Windows PowerShell
cd D:\remote\web-search

# 安装依赖（包括 mcp）
uv pip install -e .
```

### 步骤 2：配置环境变量

确保 `.env` 文件已正确配置：

```env
# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=你的API密钥
AZURE_OPENAI_ENDPOINT=https://你的资源名.openai.azure.com
AZURE_OPENAI_MODEL=gpt-4o
AZURE_OPENAI_API_VERSION=2024-12-01-preview

# Web Search 配置
WEB_SEARCH_COUNTRY=CN

# 日志级别
LOG_LEVEL=INFO
```

### 步骤 3：配置 Claude Desktop

#### Windows 用户

1. 找到 Claude Desktop 配置文件位置：
   ```
   %APPDATA%\Claude\claude_desktop_config.json
   ```
   完整路径通常是：
   ```
   C:\Users\你的用户名\AppData\Roaming\Claude\claude_desktop_config.json
   ```

2. 打开配置文件（如果不存在则创建），添加或合并以下内容：

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

**重要提示：**
- 请将 `D:\\remote\\web-search` 替换为你的实际项目路径
- Windows 路径需要使用双反斜杠 `\\`
- 如果配置文件中已有其他 MCP 服务器，只需添加 `azure-web-search` 这一项

#### macOS/Linux 用户

1. 找到配置文件位置：
   ```bash
   # macOS
   ~/Library/Application Support/Claude/claude_desktop_config.json
   
   # Linux
   ~/.config/Claude/claude_desktop_config.json
   ```

2. 编辑配置文件：

```json
{
  "mcpServers": {
    "azure-web-search": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/web-search",
        "run",
        "python",
        "mcp_server.py"
      ],
      "env": {
        "PYTHONPATH": "/path/to/web-search"
      }
    }
  }
}
```

### 步骤 4：重启 Claude Desktop

完全退出并重新启动 Claude Desktop 应用，使配置生效。

### 步骤 5：验证安装

1. 打开 Claude Desktop
2. 在对话界面，你应该能看到一个工具图标或提示，表明 MCP 服务器已连接
3. 尝试使用以下提示词测试：
   ```
   使用 web search 帮我搜索"2026年人工智能发展趋势"
   ```

## 🔧 可用的工具

配置成功后，Claude 将可以使用以下三个工具：

### 1. web_search_quick
**快速网络搜索（无推理）**

- **适用场景**：快速查询、时效性信息、简单事实查询
- **参数**：
  - `query`（必需）：搜索查询字符串
  - `country`（可选）：国家代码，如 US、CN、JP
- **速度**：⚡⚡⚡ 最快

### 2. web_search_agentic
**智能体搜索（带推理）**

- **适用场景**：复杂查询、多步推理、综合分析
- **参数**：
  - `query`（必需）：搜索查询字符串
  - `country`（可选）：国家代码
- **速度**：⚡⚡ 较快

### 3. web_search_deep
**深度研究搜索**

- **适用场景**：学术研究、深度调查、全面分析
- **参数**：
  - `query`（必需）：研究主题
  - `country`（可选）：国家代码
  - `include_code_interpreter`（可选）：是否包含代码解释器
- **速度**：⚡ 最慢但最深入
- **注意**：需要 `o3-deep-research` 模型

## 📝 使用示例

在 Claude Desktop 中，你可以这样使用：

### 示例 1：快速搜索新闻
```
请使用快速搜索查找今天的科技新闻
```

### 示例 2：地区特定搜索
```
搜索美国地区关于"AI regulations"的最新信息
```

### 示例 3：深度研究
```
对"量子计算的最新进展"进行深度研究，给我一份详细报告
```

## 🐛 故障排查

### 问题 1：Claude 无法找到工具

**解决方法：**
1. 检查配置文件路径是否正确
2. 确保项目路径使用了正确的分隔符（Windows 用 `\\`）
3. 完全退出 Claude Desktop（检查任务管理器确保进程已结束）
4. 重新启动 Claude Desktop

### 问题 2：工具调用失败

**解决方法：**
1. 检查 `.env` 文件是否配置正确
2. 验证 Azure OpenAI API 密钥是否有效
3. 查看日志文件（如果配置了日志）
4. 尝试在命令行直接运行测试：
   ```powershell
   cd D:\remote\web-search
   uv run python mcp_server.py
   ```

### 问题 3：依赖安装失败

**解决方法：**
```powershell
# 重新安装依赖
uv pip install --force-reinstall -e .

# 或者单独安装 mcp
uv pip install mcp
```

### 问题 4：权限错误

**Windows 解决方法：**
- 以管理员身份运行 PowerShell
- 检查文件夹权限
- 确保 Python 和 uv 已添加到 PATH

## 🧪 手动测试 MCP Server

在配置 Claude Desktop 之前，你可以手动测试 MCP Server 是否正常工作：

```powershell
# Windows PowerShell
cd D:\remote\web-search

# 激活虚拟环境（如果使用）
.\.venv\Scripts\Activate.ps1

# 运行 MCP Server
uv run python mcp_server.py
```

服务器应该启动并等待输入。你可以按 `Ctrl+C` 退出。

## 📊 监控和日志

MCP Server 会输出日志信息，包括：
- ✅ 初始化成功
- 🔍 搜索请求
- ❌ 错误信息

日志级别由 `.env` 文件中的 `LOG_LEVEL` 控制。

## 🔒 安全注意事项

1. **API 密钥保护**：
   - 不要提交 `.env` 文件到版本控制
   - 定期轮换 API 密钥
   - 使用最小权限原则

2. **费用控制**：
   - 每次搜索都会产生费用
   - 深度研究模式可能产生多次调用
   - 建议设置 Azure 费用警报

3. **数据隐私**：
   - 搜索查询会发送到 Azure OpenAI
   - 使用 Bing Search 服务
   - 遵守 Microsoft 隐私政策

## 📚 相关文档

- [MCP 协议文档](https://modelcontextprotocol.io/)
- [Azure OpenAI Web Search](https://learn.microsoft.com/azure/ai-foundry/openai/how-to/web-search)
- [Claude Desktop 配置指南](https://docs.anthropic.com/claude/docs)

## 🆘 获取帮助

如果遇到问题：
1. 查看本文档的故障排查部分
2. 检查项目的 README.md
3. 查看 Azure OpenAI 服务状态
4. 提交 GitHub Issue

---

**配置完成后，你就可以在 Claude Desktop 中使用强大的 Azure Web Search 功能了！** 🎉
