# 从这里开始 🚀

欢迎来到 Azure OpenAI Web Search 项目！本文档将帮助你快速找到所需的文档。

---

## 🎯 我是新用户

### 我想快速体验功能
- **30 秒快速开始** → [README.md 快速开始部分](README.md#-快速开始)
- **第一次搜索教程** → [第一次搜索](docs/getting-started/first-search.md)

### 我想了解项目功能
- **项目概述** → [overview.md](docs/getting-started/overview.md)
- **三种搜索模式对比** → [search-modes.md](docs/guides/search-modes.md)

### 我想使用 MCP Server（推荐）
- **MCP 快速开始** → [quickstart-mcp.md](docs/getting-started/quickstart-mcp.md)
- **Claude Desktop 配置** → [mcp-setup.md](docs/guides/mcp-setup.md)
- **Cursor 配置** → [cursor-setup.md](docs/guides/cursor-setup.md)

### 我想作为 Python 库使用
- **基础功能快速开始** → [quickstart.md](docs/getting-started/quickstart.md)
- **API 参考文档** → [api-reference.md](docs/guides/api-reference.md)

### 我需要配置说明
- **配置详解** → [configuration.md](docs/getting-started/configuration.md)

---

## 👨‍💻 我是开发者

### 我想搭建开发环境
- **开发环境搭建** → [setup.md](docs/development/setup.md)

### 我想运行测试
- **测试指南** → [testing.md](docs/development/testing.md)

### 我想贡献代码
- **贡献指南** → [contributing.md](docs/development/contributing.md)

### 我想了解架构
- **架构设计说明** → [architecture.md](docs/guides/architecture.md)

---

## 📚 完整文档目录

查看完整文档索引：[docs/README.md](docs/README.md)

---

## ❓ 快速问题

### ⚡ 最快的开始方式？

**使用 MCP Server**（3 步）：
1. 运行安装脚本：`scripts/install-mcp/claude.ps1`（Windows）或 `claude.sh`（Unix）
2. 重启 Claude Desktop
3. 在对话中说："请使用 web search 搜索你的问题"

### 🔑 我需要什么？

- **Azure OpenAI 资源**（需要 Azure 账户）
- **Python 3.10+**
- **uv**（推荐）或 pip

### 💰 费用如何？

- 每次 API 调用都会产生费用
- Quick Search 最便宜
- Deep Research 最贵（可能多次调用）

### 🆘 遇到问题？

1. 查看 [配置详解](docs/getting-started/configuration.md)
2. 检查 [常见问题](docs/getting-started/overview.md#常见问题)
3. [提交 Issue](../../issues)

---

## 🎓 学习路径建议

### 初学者路径
1. 📖 阅读 [项目概述](docs/getting-started/overview.md)
2. 🚀 完成 [第一次搜索教程](docs/getting-started/first-search.md)
3. ⚙️ 了解 [配置选项](docs/getting-started/configuration.md)
4. 🔍 尝试 [不同搜索模式](docs/guides/search-modes.md)

### MCP 用户路径
1. 🚀 阅读 [MCP 快速开始](docs/getting-started/quickstart-mcp.md)
2. ⚙️ 完成 [MCP 详细配置](docs/guides/mcp-setup.md)
3. 💬 在 Claude Desktop 中开始使用

### 开发者路径
1. 🛠️ 搭建 [开发环境](docs/development/setup.md)
2. 🏗️ 了解 [项目架构](docs/guides/architecture.md)
3. 🧪 运行 [测试](docs/development/testing.md)
4. 🤝 查看 [贡献指南](docs/development/contributing.md)

---

**需要帮助？** 查看 [完整文档](docs/) 或 [提交 Issue](../../issues)
