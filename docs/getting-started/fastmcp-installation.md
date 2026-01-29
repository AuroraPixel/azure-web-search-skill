# FastMCP 升级安装指南

本指南帮助你将项目升级到使用 FastMCP 框架的 v2.0.0 版本。

## 📋 升级前准备

### 检查当前版本

查看当前使用的 MCP 版本：

```bash
# 查看已安装的包
uv pip list | grep -i mcp
```

如果你看到 `mcp` 包，说明你使用的是旧版本。

### 备份配置（可选）

虽然升级不会影响配置文件，但建议备份：

```bash
# Windows
copy %APPDATA%\Claude\claude_desktop_config.json %APPDATA%\Claude\claude_desktop_config.json.backup

# macOS/Linux
cp ~/Library/Application\ Support/Claude/claude_desktop_config.json ~/Library/Application\ Support/Claude/claude_desktop_config.json.backup
```

## 🚀 升级步骤

### 步骤 1: 卸载旧版本（如果存在）

```bash
# Windows PowerShell
uv pip uninstall mcp

# macOS/Linux
uv pip uninstall mcp
```

### 步骤 2: 安装 FastMCP

```bash
# Windows PowerShell
cd D:\remote\web-search
uv pip install fastmcp

# macOS/Linux
cd /path/to/web-search
uv pip install fastmcp
```

### 步骤 3: 重新安装项目依赖

```bash
# 确保所有依赖都是最新的
uv pip install -e .
```

### 步骤 4: 验证安装

运行测试脚本：

```bash
python test_fastmcp_server.py
```

你应该看到：

```
============================================================
  FastMCP Server 测试
============================================================

🔍 测试 1: 检查依赖包...
  ✅ FastMCP 已安装 (版本: x.x.x)
  ✅ 配置模块可导入
  ✅ Web Search 模块可导入

...

============================================================
  测试总结
============================================================
✅ 所有测试通过! (6/6)

🎉 MCP Server 已准备就绪!
```

### 步骤 5: 重启 Claude Desktop 或 Cursor

1. **完全关闭** Claude Desktop 或 Cursor
2. **重新启动**应用

MCP Server 会自动启动并加载 FastMCP 框架。

## ✅ 验证升级

### 在 Claude Desktop 中测试

1. 打开 Claude Desktop
2. 输入测试查询：

```
使用 azure_web_search（mode=quick）搜索 "FastMCP 框架"
```

3. 查看结果是否正常返回

### 检查服务器版本

在 Claude Desktop 中：

```
获取 config://server 资源
```

应该看到：

```json
{
  "server_name": "Azure Web Search MCP Server",
  "version": "2.0.0",
  "framework": "FastMCP",
  ...
}
```

### 测试 Skills Provider

```
使用 research-assistant 技能研究 "人工智能"
```

或

```
获取 skill://research-assistant 资源
```

## 🆕 新功能

### 1. Skills Provider

升级后，你可以使用三个内置技能：

- **Research Assistant** - 研究助手
- **News Analyzer** - 新闻分析
- **Code Reviewer** - 代码审查

### 2. 改进的资源

除了工具，现在还有：

- **配置资源**: `config://server`
- **模式资源**: `search://modes`
- **技能资源**: `skill://research-assistant` 等

### 3. 提示模板

可以使用预定义的提示：

- `research_assistant` - 研究助手提示
- `news_analyzer` - 新闻分析提示

## 🔧 配置变更

### 无需更改

好消息！配置文件**无需更改**：

- Claude Desktop 配置保持不变
- Cursor 配置保持不变
- 环境变量保持不变

### 配置示例

如果需要重新配置，参考以下格式：

**Claude Desktop** (`%APPDATA%\Claude\claude_desktop_config.json`):

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
        "PYTHONPATH": "D:\\remote\\web-search"
      }
    }
  }
}
```

**Cursor** (`%APPDATA%\Cursor\User\globalStorage\mcp.json`):

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
        "PYTHONPATH": "D:\\remote\\web-search"
      }
    }
  }
}
```

## ⚠️ 常见问题

### 问题 1: FastMCP 安装失败

**错误**: `No module named 'fastmcp'`

**解决方案**:

```bash
# 确保使用正确的 pip
which uv  # 检查 uv 路径
uv pip install fastmcp

# 或使用完整路径
uv pip install --upgrade fastmcp
```

### 问题 2: 测试脚本失败

**错误**: 部分测试失败

**解决方案**:

1. 检查 Python 版本（需要 3.10+）
   ```bash
   python --version
   ```

2. 重新安装依赖
   ```bash
   uv pip install --upgrade -e .
   ```

3. 检查 .env 文件配置

### 问题 3: MCP Server 无法启动

**症状**: Claude Desktop 启动时没有日志输出

**解决方案**:

1. 手动运行测试：
   ```bash
   python bin/mcp_server.py
   ```

2. 查看错误信息

3. 检查路径配置

### 问题 4: Skills Provider 不可用

**症状**: 无法访问技能资源

**解决方案**:

1. 确认 skills/ 目录存在
   ```bash
   ls skills/
   ```

2. 检查每个技能目录是否包含 SKILL.md
   ```bash
   ls skills/research-assistant/
   ```

3. 重启 Claude Desktop

## 📚 相关文档

- [FastMCP 完整指南](../guides/fastmcp-guide.md)
- [MCP 设置指南](../guides/mcp-setup.md)
- [技能系统说明](../skills/README.md)
- [更新日志](../../CHANGELOG.md)

## 🎓 最佳实践

### 1. 版本管理

定期检查更新：

```bash
uv pip list --outdated
uv pip install --upgrade fastmcp
```

### 2. 开发环境

使用虚拟环境：

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 安装依赖
uv pip install -e .
```

### 3. 日志调试

启用详细日志：

在 `.env` 文件中设置：

```env
LOG_LEVEL=DEBUG
```

### 4. 备份和恢复

定期备份配置：

```bash
# 创建备份脚本
# backup_config.sh
cp ~/.claude/claude_desktop_config.json ~/.claude/claude_desktop_config.json.backup.$(date +%Y%m%d)
```

## 📞 获取帮助

如果遇到问题：

1. 查看 [FastMCP 官方文档](https://gofastmcp.com)
2. 检查项目 Issues
3. 运行测试脚本诊断问题
4. 提交新的 Issue 并附上日志

---

**升级完成后，你将享受更简洁的 API、更好的性能和强大的 Skills Provider 功能！**

**最后更新**: 2026-01-29
**版本**: 2.0.0 (FastMCP)
