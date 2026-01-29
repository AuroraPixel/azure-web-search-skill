# 脚本目录

本目录包含项目的所有脚本文件，按用途分类组织。

## 📁 目录结构

```
scripts/
├── setup/           # 环境设置脚本
├── install-mcp/     # MCP Server 安装脚本
└── run/             # 运行脚本
```

## 🛠️ 脚本说明

### setup/ - 环境设置

设置开发环境和依赖。

- **setup.ps1** (Windows) - PowerShell 安装脚本
- **setup.sh** (Unix) - Bash 安装脚本

使用方法：
```powershell
# Windows
.\scripts\setup\setup.ps1

# Unix
bash scripts/setup/setup.sh
```

### install-mcp/ - MCP Server 安装

自动配置 MCP Server 到 Claude Desktop 或 Cursor。

- **claude.ps1** (Windows) - Claude Desktop 安装脚本
- **claude.sh** (Unix) - Claude Desktop 安装脚本
- **cursor.ps1** (Windows) - Cursor 安装脚本
- **cursor.sh** (Unix) - Cursor 安装脚本

使用方法：
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

### run/ - 运行脚本

运行应用程序和测试。

- **run.ps1** (Windows) - PowerShell 运行脚本
- **run.sh** (Unix) - Bash 运行脚本

使用方法：
```powershell
# Windows
.\scripts\run\run.ps1

# Unix
bash scripts/run/run.sh
```

## ⚠️ 注意事项

1. **执行权限**（Unix）：
   ```bash
   chmod +x scripts/setup/setup.sh
   chmod +x scripts/install-mcp/*.sh
   chmod +x scripts/run/run.sh
   ```

2. **PowerShell 执行策略**（Windows）：
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

3. **路径问题**：
   - 所有脚本使用相对路径
   - 请从项目根目录运行脚本

## 📚 相关文档

- [MCP 配置指南](../docs/guides/mcp-setup.md)
- [Cursor 配置指南](../docs/guides/cursor-setup.md)
- [开发环境搭建](../docs/development/setup.md)

---

**需要帮助？** 查看 [完整文档](../docs/)
