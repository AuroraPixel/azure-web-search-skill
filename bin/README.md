# 程序入口目录

本目录包含项目的主要程序入口点。

## 📁 文件说明

### main.py
交互式命令行工具的主程序入口。

**运行方式：**
```bash
# 方式 1：使用 Python 直接运行
python bin/main.py

# 方式 2：使用 uv 运行
uv run python bin/main.py

# 方式 3：安装后使用命令（推荐）
uv pip install -e .
azure-web-search
```

**功能：**
- 提供交互式菜单界面
- 支持三种搜索模式
- 实时显示搜索结果
- 彩色终端输出

### mcp_server.py
MCP Server 程序入口，用于 Claude Desktop 和 Cursor 集成。

**运行方式：**
```bash
# 方式 1：使用 Python 直接运行
python bin/mcp_server.py

# 方式 2：使用 uv 运行
uv run python bin/mcp_server.py

# 方式 3：安装后使用命令（推荐）
uv pip install -e .
azure-mcp-server
```

**功能：**
- 实现 MCP 协议
- 提供 3 个搜索工具
- 支持异步操作
- 标准输入输出通信

## 🔧 配置

这些程序需要以下环境变量（在 `.env` 文件中配置）：

```env
AZURE_OPENAI_API_KEY=你的密钥
AZURE_OPENAI_ENDPOINT=https://你的资源.openai.azure.com
AZURE_OPENAI_MODEL=gpt-4o
```

## 📚 相关文档

- [主程序使用指南](../docs/getting-started/quickstart.md)
- [MCP 配置指南](../docs/guides/mcp-setup.md)
- [API 参考文档](../docs/guides/api-reference.md)

## ⚠️ 注意事项

1. **路径问题**：
   - 程序会自动添加项目根目录到 Python 路径
   - 无需手动配置 PYTHONPATH

2. **依赖安装**：
   - 运行前确保已安装所有依赖：`uv pip install -e .`
   - 或使用 `uv run` 自动管理虚拟环境

3. **MCP Server**：
   - 通常通过 Claude Desktop/Cursor 自动启动
   - 手动运行仅用于调试

---

**需要帮助？** 查看 [完整文档](../docs/)
