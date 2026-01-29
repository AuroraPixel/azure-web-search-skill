# Azure Web Search MCP Server 设置指南

本指南将帮助你将 Azure Web Search 项目配置为 MCP (Model Context Protocol) Server，使其可以在 Claude Desktop 和 Cursor 中作为工具使用。

## 📋 前置要求

1. **Python 3.10+** 已安装
2. **uv** 包管理器已安装
3. **Claude Desktop** 或 **Cursor** 应用已安装
4. **Azure OpenAI** 账户和 API 密钥

## 🎯 新特性 (v2.0.0)

本版本已迁移到 **FastMCP** 框架，具有以下优势：

- ✅ 更简洁的代码和 API
- ✅ 更好的开发体验
- ✅ 内置 Skills Provider 支持
- ✅ 更强大的错误处理
- ✅ 更好的类型提示
- ✅ **支持 HTTP 流式传输协议（推荐）**

## 🚀 快速设置

### 步骤 1：安装依赖

首先确保安装了所有必需的依赖，包括 FastMCP：

```powershell
# Windows PowerShell
cd D:\remote\web-search

# 安装依赖（包括 fastmcp）
uv pip install -e .
```

```bash
# macOS/Linux
cd /path/to/web-search

# 安装依赖
uv pip install -e .
```

### 步骤 2.5：选择传输协议

本 MCP Server 支持两种传输协议：

#### HTTP 流式传输（推荐）

**适用场景**：
- 需要远程访问 MCP 服务器
- 多个客户端需要同时连接
- 部署到服务器或云环境
- 需要更好的性能和稳定性

**配置方式**：

在 `.env` 文件中设置：
```env
MCP_TRANSPORT=http
MCP_HOST=127.0.0.1  # 或 0.0.0.0 以允许远程访问
MCP_PORT=8000       # 可以更改为其他端口
```

**启动 HTTP 服务器**：

```bash
# 方式 1：直接运行服务器
python -m bin.mcp_server

# 方式 2：使用 uv run
uv run python -m bin.mcp_server

# 方式 3：使用 FastMCP CLI（推荐用于开发）
fastmcp run bin/mcp_server.py --transport http --port 8000
```

**访问地址**：
- 本地：`http://127.0.0.1:8000/mcp`
- 远程：`http://YOUR_SERVER_IP:8000/mcp`（需要设置 `MCP_HOST=0.0.0.0`）

#### STDIO 传输（传统）

**适用场景**：
- 与 Claude Desktop 集成
- 本地开发测试
- 单用户使用

**配置方式**：

在 `.env` 文件中设置：
```env
MCP_TRANSPORT=stdio
```

然后按照下面的步骤配置 Claude Desktop 或 Cursor。

### 步骤 3：配置 Claude Desktop（STDIO 模式）

#### Windows 用户

1. 找到 Claude Desktop 配置文件位置：
   ```
   %APPDATA%\Claude\claude_desktop_config.json
   ```

2. 编辑配置文件，添加以下内容：

   **STDIO 模式配置**（传统方式）：
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
           "bin/mcp_server.py"
         ],
         "env": {
           "PYTHONPATH": "D:\\remote\\web-search",
           "MCP_TRANSPORT": "stdio"
         }
       }
     }
   }
   ```

   **HTTP 模式配置**（推荐）：
   ```json
   {
     "mcpServers": {
       "azure-web-search": {
         "url": "http://127.0.0.1:8000/mcp"
       }
     }
   }
   ```

   **注意**：使用 HTTP 模式时，需要先单独启动 MCP 服务器（见步骤 2.5）。

3. 保存文件

#### macOS 用户

1. 找到配置文件：
   ```
   ~/Library/Application Support/Claude/claude_desktop_config.json
   ```

2. 编辑配置：

   **STDIO 模式配置**（传统方式）：
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
           "bin/mcp_server.py"
         ],
         "env": {
           "PYTHONPATH": "/path/to/web-search",
           "MCP_TRANSPORT": "stdio"
         }
       }
     }
   }
   ```

   **HTTP 模式配置**（推荐）：
   ```json
   {
     "mcpServers": {
       "azure-web-search": {
         "url": "http://127.0.0.1:8000/mcp"
       }
     }
   }
   ```

#### Linux 用户

1. 找到配置文件：
   ```
   ~/.config/Claude/claude_desktop_config.json
   ```

2. 使用与 macOS 相同的配置格式（STDIO 或 HTTP 模式）

### 步骤 4：配置 Cursor（可选）

#### Windows 用户

1. 找到 Cursor 配置文件：
   ```
   %APPDATA%\Cursor\User\globalStorage\mcp.json
   ```

2. 添加配置：

   **STDIO 模式配置**（传统方式）：
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
           "bin/mcp_server.py"
         ],
         "env": {
           "PYTHONPATH": "D:\\remote\\web-search",
           "MCP_TRANSPORT": "stdio"
         }
       }
     }
   }
   ```

   **HTTP 模式配置**（推荐）：
   ```json
   {
     "mcpServers": {
       "azure-web-search": {
         "url": "http://127.0.0.1:8000/mcp"
       }
     }
   }
   ```

#### macOS/Linux 用户

1. 找到配置文件：
   ```
   ~/Library/Application Support/Cursor/User/globalStorage/mcp.json  (macOS)
   ~/.config/Cursor/User/globalStorage/mcp.json                    (Linux)
   ```

2. 使用与 Claude Desktop 相同的配置格式（STDIO 或 HTTP 模式）

### 步骤 5：启动服务器和重启应用

#### HTTP 模式

1. **先启动 MCP HTTP 服务器**：
   ```bash
   # 在新的终端窗口中
   cd D:\remote\web-search
   python -m bin.mcp_server
   ```

   服务器会显示：
   ```
   🚀 启动 Azure Web Search MCP Server (HTTP 流式传输模式)
   📡 服务器地址: http://127.0.0.1:8000/mcp
   🎯 MCP HTTP 服务器正在启动...
   ```

2. **重启 Claude Desktop 或 Cursor**

#### STDIO 模式

1. **完全关闭** Claude Desktop 或 Cursor
2. **重新启动**应用
3. MCP 服务器会自动启动

## 🛠️ 测试 MCP Server

### 方法 1：使用测试脚本

```bash
# Windows PowerShell
cd D:\remote\web-search
python test_mcp_server.py
```

```bash
# macOS/Linux
cd /path/to/web-search
python test_mcp_server.py
```

### 方法 2：在 Claude Desktop 中测试

1. 打开 Claude Desktop
2. 输入测试查询：
   ```
   使用 web_search_quick 搜索 "Python 3.12 新特性"
   ```
3. 查看结果

### 方法 3：查看日志

MCP Server 的日志会输出到终端，可以看到：
- 服务器启动信息
- 技能加载信息
- 工具调用日志
- 错误信息

## 📦 可用工具

MCP Server 提供以下工具：

### 1. web_search_quick

快速搜索，无推理

```json
{
  "name": "web_search_quick",
  "description": "执行快速网络搜索（无推理）",
  "parameters": {
    "query": "搜索查询（必需）",
    "country": "国家代码（可选）"
  }
}
```

**使用示例**：
```
使用 web_search_quick 搜索 "2026年人工智能趋势"
```

### 2. web_search_agentic

智能体搜索，带推理

```json
{
  "name": "web_search_agentic",
  "description": "执行智能体搜索（带推理）",
  "parameters": {
    "query": "搜索查询（必需）",
    "country": "国家代码（可选）"
  }
}
```

**使用示例**：
```
使用 web_search_agentic 分析 "量子计算在密码学中的应用"
```

## 🎨 Skills Provider 功能

本 MCP Server 还支持 Skills Provider，可以将 AI 技能作为资源暴露。

### 可用技能

1. **Research Assistant** (`skill://research-assistant`)
   - 多阶段研究
   - 信息综合和分析
   - 来源追踪和验证

2. **News Analyzer** (`skill://news-analyzer`)
   - 实时新闻搜索
   - 多源分析和验证
   - 趋势追踪

3. **Code Reviewer** (`skill://code-reviewer`)
   - 代码搜索和示例
   - 技术最佳实践
   - 工具和框架评估

### 使用技能

在 Claude Desktop 中：

```
使用 research-assistant 技能研究 "人工智能在医疗领域的应用"
使用 news-analyzer 技能分析 "今日科技新闻"
使用 code-reviewer 技能查找 "Python 异步编程最佳实践"
```

### 技能目录结构

```
skills/
├── research-assistant/
│   └── SKILL.md
├── news-analyzer/
│   └── SKILL.md
├── code-reviewer/
│   └── SKILL.md
└── README.md
```

## 🔧 高级配置

### 自定义技能目录

如果要将技能放在其他位置，可以修改 `bin/mcp_server.py`：

```python
def setup_skills_provider():
    """设置 Skills Provider"""
    # 自定义技能目录
    skills_dir = Path("/path/to/custom/skills")

    if skills_dir.exists():
        from fastmcp.server.providers.skills import SkillsDirectoryProvider
        mcp.add_provider(SkillsDirectoryProvider(roots=skills_dir))
```

### 调整日志级别

在 `.env` 文件中设置：

```env
LOG_LEVEL=DEBUG  # 详细日志
LOG_LEVEL=INFO   # 标准日志（默认）
LOG_LEVEL=WARNING # 警告和错误
LOG_LEVEL=ERROR  # 仅错误
```

### 性能优化

1. **减少日志输出**：设置 `LOG_LEVEL=WARNING`
2. **调整搜索结果数量**：在工具调用中指定 `num_results`
3. **使用缓存**：FastMCP 会自动缓存常用查询

## ⚠️ 故障排查

### 问题 1：MCP Server 无法启动

**症状**：Claude Desktop 启动时没有看到 MCP 服务器日志

**解决方案**：
1. 检查配置文件路径是否正确
2. 验证 `.env` 文件存在并包含有效的 API 密钥
3. 确认 `uv` 已安装：`uv --version`
4. 手动运行测试：`python bin/mcp_server.py`

### 问题 2：工具调用失败

**症状**：Claude 报告无法调用工具

**解决方案**：
1. 检查 Azure OpenAI API 密钥是否有效
2. 验证 endpoint URL 是否正确
3. 查看日志中的错误信息
4. 确认模型名称正确（如 `gpt-4o`）

### 问题 3：Skills Provider 不可用

**症状**：无法访问技能资源

**解决方案**：
1. 确认 `skills/` 目录存在
2. 检查每个技能目录是否包含 `SKILL.md`
3. 重启 Claude Desktop
4. 查看服务器日志确认技能已加载

### 问题 4：路径错误（Windows）

**症状**：Python 无法找到项目模块

**解决方案**：
确保配置中的路径使用双反斜杠或正斜杠：

```json
{
  "args": [
    "--directory",
    "D:\\remote\\web-search",  // 或 "D:/remote/web-search"
    "run",
    "python",
    "bin/mcp_server.py"
  ]
}
```

## 📚 相关文档

- [FastMCP 完整指南](fastmcp-guide.md)
- [API 参考文档](api-reference.md)
- [主 README](../../README.md)
- [快速开始指南](../getting-started/quickstart.md)

## 🆕 从旧版本升级

如果你使用的是旧版本（基于 `mcp` 包），升级步骤：

1. **更新依赖**
   ```bash
   uv pip install --upgrade fastmcp
   ```

2. **更新配置**
   - 配置文件无需更改
   - 确保路径指向 `bin/mcp_server.py`

3. **重启应用**
   - 完全关闭 Claude Desktop/Cursor
   - 重新启动

4. **验证升级**
   - 查看 `config://server` 资源确认版本为 2.0.0
   - 测试工具调用
   - 检查 Skills Provider 是否正常工作

## 🎓 最佳实践

1. **使用合适的搜索模式**
   - 简单查询 → `web_search_quick`
   - 复杂查询 → `web_search_agentic`

2. **利用技能系统**
   - 复用预定义的技能模板
   - 根据需求创建自定义技能
   - 保持技能文档更新

3. **监控性能**
   - 查看日志了解搜索耗时
   - 调整搜索参数优化性能
   - 使用缓存减少重复查询

4. **安全性**
   - 不要在配置中硬编码 API 密钥
   - 使用 `.env` 文件管理敏感信息
   - 定期轮换 API 密钥

## 📞 获取帮助

如果遇到问题：

1. 查看 [FastMCP 文档](https://gofastmcp.com)
2. 检查项目 Issues
3. 提交新的 Issue 并附上日志
4. 查看 [故障排查部分](#⚠️-故障排查)

---

**最后更新**: 2026-01-29
**版本**: 2.0.0 (FastMCP)
