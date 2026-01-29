# 🚀 MCP Server 快速启动

## 最简单的方式

```bash
# 进入项目目录
cd D:\remote\web-search

# 启动 HTTP 服务器
python -m bin.mcp_server
```

服务器将在 `http://127.0.0.1:8000/mcp` 启动

## 其他运行方式

```bash
# 方式 1：直接运行脚本
python bin/mcp_server.py

# 方式 2：使用 uv
uv run python -m bin.mcp_server

# 方式 3：使用安装的命令
azure-mcp-server

# 方式 4：使用 FastMCP CLI（支持热重载）
fastmcp run bin/mcp_server.py --reload
```

## 配置文件 (.env)

```env
# Azure OpenAI（必需）
AZURE_OPENAI_API_KEY=你的密钥
AZURE_OPENAI_ENDPOINT=https://你的资源.openai.azure.com
AZURE_OPENAI_MODEL=gpt-4o

# MCP 服务器
MCP_TRANSPORT=http      # http（推荐）或 stdio
MCP_HOST=127.0.0.1      # 监听地址
MCP_PORT=8000           # 端口

# Web Search（可选）
WEB_SEARCH_COUNTRY=CN   # 国家代码
LOG_LEVEL=INFO          # 日志级别
```

## 客户端配置

### Claude Desktop / Cursor（HTTP 模式）

```json
{
  "mcpServers": {
    "azure-web-search": {
      "url": "http://127.0.0.1:8000/mcp"
    }
  }
}
```

### Claude Desktop / Cursor（STDIO 模式）

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

## 测试连接

```bash
# 测试 HTTP 端点
curl -X POST http://127.0.0.1:8000/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}'
```

## 常见问题

**端口被占用？**
```env
MCP_PORT=8001  # 更改端口
```

**模块未找到？**
```bash
# 确保在项目根目录
cd D:\remote\web-search
python -m bin.mcp_server
```

**依赖缺失？**
```bash
uv pip install -e .
```

## 完整文档

- 📖 [运行指南](RUN_GUIDE.md) - 详细运行说明
- 📖 [HTTP 迁移指南](HTTP_MIGRATION.md) - HTTP 协议说明
- 📖 [MCP 配置指南](docs/guides/mcp-setup.md) - 客户端配置

---

**快速启动**：`python -m bin.mcp_server`
**访问地址**：`http://127.0.0.1:8000/mcp`
