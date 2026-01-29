# Azure OpenAI Web Search

一个功能完整、架构清晰的 Azure OpenAI Web Search 集成项目，使用 Python 实现，支持多种搜索模式和 MCP Server 集成。

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![MCP](https://img.shields.io/badge/MCP-Server-purple.svg)](https://modelcontextprotocol.io/)

## 简介

本项目提供了 Azure OpenAI Web Search 的完整 Python 实现，支持两种搜索模式，并可作为 MCP Server 集成到 Claude Desktop 和 Cursor 中。

### 核心特性

- **两种搜索模式**：快速搜索、智能体搜索
- **MCP Server 支持**：可集成到 Claude Desktop 和 Cursor
- **地理位置支持**：基于 ISO 3166-1 标准的国家代码
- **自动引用管理**：智能提取和去重 URL 引用
- **类型安全**：基于 Pydantic 的完整类型验证
- **美观输出**：使用 Rich 库提供彩色终端输出

### 技术栈

- Python 3.10+
- Azure OpenAI SDK
- Pydantic Settings
- Rich (终端美化)
- MCP Server

## 🚀 快速开始

### 30 秒快速体验

```bash
# 1. 克隆项目
git clone <your-repo-url>
cd web-search

# 2. 安装依赖（需要 [uv](https://github.com/astral-sh/uv)）
uv venv && uv pip install -e .

# 3. 配置环境变量
cp .env.example .env
# 编辑 .env 填写你的 Azure OpenAI 配置

# 4. 运行示例
python examples/basic_search.py
```

### 使用 MCP Server（推荐）

在 Claude Desktop 或 Cursor 中直接使用 Web Search 功能：

📖 **详细配置**：[MCP 配置指南](docs/guides/mcp-setup.md) | [Cursor 配置指南](docs/guides/cursor-setup.md)

配置完成后，在 Claude 中直接对话：
```
请使用 web search 搜索"2026年人工智能发展趋势"
```

## 📖 使用方式

### 方式 1：MCP Server（推荐）

直接在 Claude Desktop/Cursor 中使用，无需编写代码。

- [MCP 快速开始](docs/getting-started/quickstart-mcp.md)
- [MCP 详细配置](docs/guides/mcp-setup.md)
- [Cursor 集成](docs/guides/cursor-setup.md)

### 方式 2：Python 库

```python
from src.config import get_settings
from src.web_search import AzureWebSearch

settings = get_settings()
search = AzureWebSearch(settings)

# 快速搜索
result = search.quick_search("2026年人工智能发展趋势")
print(result.text)
```

- [基础功能快速开始](docs/getting-started/quickstart.md)
- [搜索模式对比](docs/guides/search-modes.md)
- [API 参考文档](docs/guides/api-reference.md)

## 🔍 两种搜索模式

| 模式 | 速度 | 深度 | 推理能力 | 适用场景 |
|-----|------|------|---------|---------|
| **Quick Search** | ⚡⚡⚡ | ⭐ | ❌ | 快速查询、时效性信息 |
| **Agentic Search** | ⚡⚡ | ⭐⭐ | ✅ | 复杂查询、需要分析 |

详细说明：[搜索模式对比](docs/guides/search-modes.md)

## 📚 文档导航

### 新用户入门
- [从这里开始](START_HERE.md) - 快速导航指引
- [项目概述](docs/getting-started/overview.md) - 了解项目功能
- [第一次搜索](docs/getting-started/first-search.md) - 跟随教程完成第一次搜索
- [配置详解](docs/getting-started/configuration.md) - 所有配置选项说明

### 使用指南
- [基础功能快速开始](docs/getting-started/quickstart.md)
- [MCP 功能快速开始](docs/getting-started/quickstart-mcp.md)
- [搜索模式对比](docs/guides/search-modes.md)
- [API 参考文档](docs/guides/api-reference.md)

### 配置指南
- [MCP 详细配置](docs/guides/mcp-setup.md) - Claude Desktop 集成
- [Cursor 集成指南](docs/guides/cursor-setup.md) - Cursor 集成
- [架构设计说明](docs/guides/architecture.md) - 项目架构

### 开发者文档
- [开发环境搭建](docs/development/setup.md)
- [测试指南](docs/development/testing.md)
- [贡献指南](docs/development/contributing.md)
- [部署指南](docs/development/deployment.md)

## 🛠️ 开发

### 安装开发依赖

```bash
uv pip install -e ".[dev]"
```

### 代码格式化和检查

```bash
# 格式化代码
black src/ examples/

# 检查代码
ruff check src/ examples/
```

### 运行测试

```bash
pytest
```

## 📋 依赖项

- **openai** (>=1.57.0) - Azure OpenAI SDK
- **python-dotenv** (>=1.0.0) - 环境变量管理
- **pydantic** (>=2.10.0) - 数据验证
- **pydantic-settings** (>=2.6.0) - 配置管理
- **rich** (>=13.9.0) - 终端美化
- **mcp** (>=1.1.2) - MCP Server 支持

## ⚠️ 重要提示

### 费用提醒
- Web Search 功能会产生 Azure OpenAI API 费用
- 每次搜索调用都会计费
- 智能体搜索通常比快速搜索更耗时、也可能更贵

### 数据隐私
- 使用 Grounding with Bing Search 服务
- 数据可能流向合规边界之外
- Microsoft 隐私声明适用

### 模型要求
- Quick/Agentic Search：需要 GPT-4 及更高版本

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🤝 贡献

欢迎贡献！请查看 [贡献指南](docs/development/contributing.md)

## 📞 支持

- 📖 [完整文档](docs/)
- 🐛 [提交 Issue](../../issues)
- 💬 [讨论区](../../discussions)

---

**Made with ❤️ using Python & Azure OpenAI**

📖 **完整文档**：[docs/](docs/) | 🚀 **快速开始**：[START_HERE.md](START_HERE.md)
