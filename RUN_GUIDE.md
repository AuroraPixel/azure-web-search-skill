# MCP Server 运行指南

## 🚀 快速启动

### 推荐方式：Python 模块运行

```bash
# 进入项目目录
cd D:\remote\web-search

# 以 Python 模块方式运行（推荐）
python -m bin.mcp_server
```

### 其他运行方式

#### 方式 1：直接运行脚本

```bash
# Windows PowerShell
python bin/mcp_server.py

# 或使用完整路径
python D:\remote\web-search\bin\mcp_server.py
```

#### 方式 2：使用 uv run

```bash
# 使用 uv 包管理器
uv run python -m bin.mcp_server

# 或
uv run python bin/mcp_server.py
```

#### 方式 3：使用安装的命令行工具

```bash
# 首先安装项目（如果还没安装）
uv pip install -e .

# 然后使用命令行工具
azure-mcp-server
```

#### 方式 4：使用 FastMCP CLI（开发模式）

```bash
# 使用 FastMCP CLI 运行（支持热重载）
fastmcp run bin/mcp_server.py --transport http --port 8000

# 开发模式（自动重载）
fastmcp run bin/mcp_server.py --reload
```

## ⚙️ 配置说明

### 环境变量配置 (.env)

在项目根目录创建 `.env` 文件：

```env
# Azure OpenAI 配置
AZURE_OPENAI_API_KEY=你的API密钥
AZURE_OPENAI_ENDPOINT=https://你的资源名.openai.azure.com
AZURE_OPENAI_MODEL=gpt-4o

# MCP 服务器配置
MCP_TRANSPORT=http      # 传输协议：http 或 stdio
MCP_HOST=127.0.0.1      # HTTP 服务器监听地址
MCP_PORT=8000           # HTTP 服务器端口

# Web Search 配置
WEB_SEARCH_COUNTRY=CN   # 国家代码（可选）

# 日志级别
LOG_LEVEL=INFO          # DEBUG, INFO, WARNING, ERROR
```

### 选择传输协议

#### HTTP 模式（推荐）

**适用场景**：
- 需要远程访问 MCP 服务器
- 多个客户端需要同时连接
- 部署到服务器或云环境
- 开发和测试

**配置**：
```env
MCP_TRANSPORT=http
MCP_HOST=127.0.0.1
MCP_PORT=8000
```

**启动后访问**：
```
http://127.0.0.1:8000/mcp
```

#### STDIO 模式（传统）

**适用场景**：
- 与 Claude Desktop 集成
- 本地开发测试
- 单用户使用

**配置**：
```env
MCP_TRANSPORT=stdio
```

**启动方式**：
```bash
# 客户端会自动启动服务器
# 或手动运行（用于测试）
python -m bin.mcp_server
```

## 🧪 测试运行

### 测试 HTTP 模式

1. **启动服务器**：
   ```bash
   python -m bin.mcp_server
   ```

2. **查看输出**：
   ```
   🚀 启动 Azure Web Search MCP Server (HTTP 流式传输模式)
   📡 服务器地址: http://127.0.0.1:8000/mcp
   🎯 MCP HTTP 服务器正在启动...
   ```

3. **测试连接**（在新终端）：
   ```bash
   curl -X POST http://127.0.0.1:8000/mcp \
     -H "Content-Type: application/json" \
     -H "Accept: application/json, text/event-stream" \
     -d '{
       "jsonrpc": "2.0",
       "id": 1,
       "method": "initialize",
       "params": {
         "protocolVersion": "2024-11-05",
         "capabilities": {},
         "clientInfo": {"name": "test", "version": "1.0"}
       }
     }'
   ```

### 测试 STDIO 模式

1. **启动服务器**：
   ```bash
   python -m bin.mcp_server
   ```

2. **查看输出**：
   ```
   🚀 启动 Azure Web Search MCP Server (STDIO 传输模式)
   🎯 MCP STDIO 服务器已启动，等待连接...
   ```

3. **发送 JSON-RPC 消息**（通过 stdin）：
   ```json
   {"jsonrpc":"2.0","id":1,"method":"initialize","params":{...}}
   ```

## 🔧 常见问题

### 问题 1：模块未找到错误

**错误**：
```
ModuleNotFoundError: No module named 'bin'
```

**解决方案**：
```bash
# 确保在项目根目录
cd D:\remote\web-search

# 确保当前目录在 Python 路径中
python -m bin.mcp_server
```

### 问题 2：环境变量未加载

**错误**：
```
ValidationError: AZURE_OPENAI_API_KEY is required
```

**解决方案**：
1. 确保 `.env` 文件存在于项目根目录
2. 检查环境变量格式是否正确
3. 尝试手动设置环境变量：
   ```bash
   # Windows PowerShell
   $env:AZURE_OPENAI_API_KEY="你的密钥"
   $env:AZURE_OPENAI_ENDPOINT="https://..."
   python -m bin.mcp_server
   ```

### 问题 3：端口被占用

**错误**：
```
OSError: [Errno 48] Address already in use
```

**解决方案**：
```env
# 在 .env 文件中更改端口
MCP_PORT=8001
```

或临时指定端口：
```bash
# 使用环境变量
$env:MCP_PORT="8001"
python -m bin.mcp_server
```

### 问题 4：依赖包缺失

**错误**：
```
ModuleNotFoundError: No module named 'fastmcp'
```

**解决方案**：
```bash
# 安装项目依赖
uv pip install -e .

# 或单独安装 fastmcp
uv pip install fastmcp
```

## 📊 运行模式对比

| 运行方式 | 优点 | 缺点 | 适用场景 |
|---------|------|------|---------|
| `python -m bin.mcp_server` | 标准、可靠 | 需要在项目根目录 | 日常使用 |
| `python bin/mcp_server.py` | 简单直接 | 路径问题 | 快速测试 |
| `uv run python ...` | 隔离环境 | 稍慢 | 开发环境 |
| `azure-mcp-server` | 最简单 | 需要先安装 | 生产环境 |
| `fastmcp run ...` | 功能丰富 | 需要额外工具 | 高级开发 |

## 🎯 最佳实践

### 开发环境

```bash
# 1. 创建虚拟环境（可选）
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# 2. 安装依赖
uv pip install -e .

# 3. 使用 HTTP 模式运行（便于调试）
python -m bin.mcp_server

# 4. 或使用 FastMCP CLI（支持热重载）
fastmcp run bin/mcp_server.py --reload --transport http
```

### 生产环境

```bash
# 1. 安装项目
uv pip install -e .

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 文件

# 3. 使用 systemd/supervisor/nomad 等管理进程
azure-mcp-server

# 4. 或使用 Python 模块方式
python -m bin.mcp_server
```

### Docker 部署

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN pip install uv
RUN uv pip install -e .

ENV MCP_TRANSPORT=http
ENV MCP_HOST=0.0.0.0
ENV MCP_PORT=8000

EXPOSE 8000

CMD ["python", "-m", "bin.mcp_server"]
```

## 🔍 调试技巧

### 查看详细日志

```env
# 在 .env 中设置
LOG_LEVEL=DEBUG
```

### 检查服务器状态

```bash
# HTTP 模式：检查端口
netstat -an | findstr 8000  # Windows
lsof -i :8000               # macOS/Linux

# 测试连接
curl http://127.0.0.1:8000/mcp
```

### 查看可用工具

使用 MCP Inspector（需要安装 fastmcp）：
```bash
fastmcp inspect bin/mcp_server.py
```

## 📚 相关文档

- [HTTP 迁移指南](HTTP_MIGRATION.md)
- [MCP 配置指南](docs/guides/mcp-setup.md)
- [FastMCP 文档](https://gofastmcp.com)

## 🚀 下一步

1. ✅ 选择运行方式（推荐 `python -m bin.mcp_server`）
2. ✅ 配置 `.env` 文件
3. ✅ 启动服务器
4. ✅ 配置客户端（Claude Desktop / Cursor）
5. ✅ 测试工具调用

---

**最后更新**：2026-01-29
**Python 版本**：3.10+
**FastMCP 版本**：2.11.3
