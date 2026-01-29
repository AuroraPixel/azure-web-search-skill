# 配置模板目录

本目录包含各种配置文件的模板，方便快速配置和部署。

## 📁 目录结构

```
config-templates/
├── claude/      # Claude Desktop 相关配置
└── cursor/      # Cursor 编辑器相关配置
```

## 📋 配置文件说明

### claude/ - Claude Desktop 配置

用于配置 Claude Desktop 的 MCP Server。

- **mcp-server.json** - Claude Desktop MCP Server 配置模板

使用方法：
1. 复制模板到 Claude Desktop 配置目录：
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
2. 根据你的实际情况修改路径

详细配置指南：[MCP 配置指南](../docs/guides/mcp-setup.md)

### cursor/ - Cursor 编辑器配置

用于配置 Cursor 编辑器的 MCP Server。

- **mcp-rules.txt** - Cursor MCP 规则配置模板

使用方法：
1. 复制模板到 Cursor 项目配置目录
2. 根据项目路径调整配置

详细配置指南：[Cursor 配置指南](../docs/guides/cursor-setup.md)

## 🔧 快速配置

### 方式 1：使用安装脚本（推荐）

```powershell
# Claude Desktop (Windows)
.\scripts\install-mcp\claude.ps1

# Claude Desktop (Unix)
bash scripts/install-mcp/claude.sh

# Cursor (Windows)
.\scripts\install-mcp\cursor.ps1

# Cursor (Unix)
bash scripts/install-mcp/cursor.sh
```

### 方式 2：手动配置

1. 复制对应的配置模板
2. 修改路径和参数
3. 粘贴到目标配置文件

## 📚 相关文档

- [MCP 详细配置](../docs/guides/mcp-setup.md)
- [Cursor 集成指南](../docs/guides/cursor-setup.md)
- [配置详解](../docs/getting-started/configuration.md)

## ⚠️ 注意事项

1. **路径格式**：
   - Windows: 使用反斜杠 `\` 或正斜杠 `/`
   - Unix/macOS: 使用正斜杠 `/`

2. **Python 解释器**：
   - 确保指向正确的 Python 环境
   - 使用虚拟环境时需要指定完整路径

3. **环境变量**：
   - 配置文件不会自动加载 `.env`
   - 需要在系统环境变量中设置

4. **JSON 格式**：
   - 确保配置文件是有效的 JSON 格式
   - 注意逗号和引号

## 🔍 配置验证

配置完成后，可以运行测试验证：

```bash
python test_mcp_server.py
```

---

**需要帮助？** 查看 [完整文档](../docs/) 或 [提交 Issue](../..//issues)
