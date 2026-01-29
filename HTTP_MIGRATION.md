# HTTP 流式传输协议迁移指南

## 📋 概述

本项目已成功从 **STDIO 传输协议** 迁移到 **HTTP 流式传输协议**（默认）。这是一个重大升级，提供了更好的性能、可扩展性和部署灵活性。

## 🎯 主要变更

### 1. 新增配置项

在 `src/config.py` 中添加了以下配置：

```python
# HTTP 服务器配置
mcp_host: str = Field(default="127.0.0.1", description="MCP 服务器监听地址")
mcp_port: int = Field(default=8000, description="MCP 服务器端口")
mcp_transport: str = Field(default="http", description="MCP 传输协议 (stdio/http)")
```

### 2. 启动方式变更

**之前（STDIO 模式）**：
```python
def main():
    mcp.run()  # 默认使用 STDIO
```

**现在（HTTP 模式）**：
```python
def main():
    settings = get_settings()

    if settings.mcp_transport == "http":
        mcp.run(transport="http", host=settings.mcp_host, port=settings.mcp_port)
    else:
        mcp.run()  # STDIO 模式
```

### 3. 环境变量配置

在 `.env` 文件中添加：

```env
# MCP 服务器配置（推荐使用 HTTP 模式）
MCP_TRANSPORT=http
MCP_HOST=127.0.0.1
MCP_PORT=8000
```

## 🚀 使用方式

### 启动 HTTP 服务器

```bash
# 方式 1：直接运行
python -m bin.mcp_server

# 方式 2：使用 uv run
uv run python -m bin.mcp_server

# 方式 3：使用 FastMCP CLI
fastmcp run bin/mcp_server.py --transport http --port 8000
```

服务器将在 `http://127.0.0.1:8000/mcp` 启动。

### 客户端配置

#### Claude Desktop / Cursor（HTTP 模式）

```json
{
  "mcpServers": {
    "azure-web-search": {
      "url": "http://127.0.0.1:8000/mcp"
    }
  }
}
```

#### Claude Desktop / Cursor（STDIO 模式 - 向后兼容）

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

## ✅ 测试验证

HTTP 服务器已通过以下测试：

1. ✅ 服务器成功启动在 `http://127.0.0.1:8000/mcp`
2. ✅ 响应 MCP 初始化请求
3. ✅ 支持流式传输（Server-Sent Events）
4. ✅ 正确返回服务器能力信息

### 测试命令

```bash
# 测试初始化
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

## 🎨 HTTP 模式的优势

### 1. 网络访问能力
- 支持远程访问（配置 `MCP_HOST=0.0.0.0`）
- 可部署到服务器或云环境
- 支持反向代理和负载均衡

### 2. 多客户端支持
- 单个服务器实例可服务多个客户端
- 更好的资源利用率
- 支持并发请求处理

### 3. 开发体验
- 独立运行，便于调试
- 可使用标准 HTTP 工具测试
- 支持热重载（使用 `fastmcp run --reload`）

### 4. 生产部署
- 可集成到现有 Web 基础设施
- 支持 Docker 容器化
- 易于监控和日志管理

## 📊 性能对比

| 特性 | STDIO | HTTP (Streamable) |
|-----|-------|-------------------|
| 本地性能 | ⚡⚡⚡ | ⚡⚡ |
| 远程访问 | ❌ | ✅ |
| 多客户端 | ❌ | ✅ |
| 调试便利性 | ⭐⭐ | ⭐⭐⭐ |
| 部署灵活性 | ⭐ | ⭐⭐⭐ |
| 生产环境 | ⭐⭐ | ⭐⭐⭐ |

## 🔧 高级配置

### 允许远程访问

在 `.env` 中设置：
```env
MCP_HOST=0.0.0.0
```

然后使用服务器 IP 地址访问：
```
http://YOUR_SERVER_IP:8000/mcp
```

### 自定义端口

```env
MCP_PORT=9000
```

访问地址变为：`http://127.0.0.1:9000/mcp`

### 使用 Nginx 反向代理

```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;

    location /mcp {
        proxy_pass http://127.0.0.1:8000/mcp;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
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

## 🔄 回退到 STDIO 模式

如果需要使用 STDIO 模式（例如与 Claude Desktop 本地集成）：

1. 修改 `.env` 文件：
   ```env
   MCP_TRANSPORT=stdio
   ```

2. 或者设置环境变量：
   ```bash
   export MCP_TRANSPORT=stdio
   ```

3. 使用传统方式配置客户端（见上文）。

## 📚 相关文档

- [FastMCP HTTP 部署指南](https://gofastmcp.com/deployment/running-server#http-transport-streamable)
- [MCP 配置指南](docs/guides/mcp-setup.md)
- [项目 README](README.md)

## 🐛 故障排查

### 问题 1：端口被占用

**错误**：`Address already in use`

**解决方案**：
```env
MCP_PORT=8001  # 更改为其他端口
```

### 问题 2：无法远程访问

**解决方案**：
1. 确保 `MCP_HOST=0.0.0.0`
2. 检查防火墙设置
3. 确认云服务器安全组规则

### 问题 3：连接被拒绝

**解决方案**：
1. 确认服务器正在运行
2. 检查 URL 是否正确
3. 查看服务器日志

## 📝 更新日志

### v2.1.0 (2026-01-29)

- ✅ 添加 HTTP 流式传输协议支持
- ✅ 新增 `mcp_transport`、`mcp_host`、`mcp_port` 配置
- ✅ 更新 MCP 服务器启动逻辑
- ✅ 更新配置文件和文档
- ✅ 保持向后兼容 STDIO 模式
- ✅ 添加配置验证器

## 🎓 最佳实践

1. **开发环境**：使用 HTTP 模式，便于调试和测试
2. **生产环境**：使用 HTTP 模式，配合 Nginx 或其他反向代理
3. **本地集成**：使用 STDIO 模式，与 Claude Desktop 集成
4. **远程部署**：使用 HTTP 模式，配置适当的认证和加密

## 📞 支持

如有问题，请：
- 查看 [FastMCP 文档](https://gofastmcp.com)
- 检查项目 Issues
- 提交新的 Issue

---

**迁移完成时间**：2026-01-29
**FastMCP 版本**：2.11.3
**MCP 版本**：1.12.4
