# 🎯 从这里开始 - Azure Web Search MCP Server

## 🎊 恭喜！你的项目现在支持 MCP Server！

你的 web-search 项目已成功添加为 Claude Desktop 的 MCP Server。现在可以在 Claude 对话中直接使用 Azure Web Search 功能了！

---

## ⚡ 3 步快速开始

### 1️⃣ 安装依赖（2 分钟）

打开 PowerShell，运行：

```powershell
cd D:\remote\web-search
uv pip install -e .
```

这将安装所有必需的包，包括新添加的 `mcp` 包。

### 2️⃣ 运行安装脚本（1 分钟）

```powershell
.\install_mcp.ps1
```

脚本会自动：
- ✅ 检查环境配置
- ✅ 配置 Claude Desktop
- ✅ 创建配置文件

### 3️⃣ 启动使用（1 分钟）

1. **重启 Claude Desktop**（完全退出并重新打开）

2. **在 Claude 中测试**：
   ```
   使用 web search 搜索 "2026年人工智能发展趋势"
   ```

3. **享受强大的 Web Search！** 🎉

---

## ✅ 验证安装（可选）

运行测试脚本确保一切正常：

```powershell
python test_mcp_server.py
```

应该看到所有 5 个测试通过：
```
✓ 通过 - 基础依赖
✓ 通过 - 环境配置
✓ 通过 - Web Search 客户端
✓ 通过 - MCP Server 文件
✓ 通过 - Claude Desktop 配置

通过: 5/5
```

---

## 📚 使用示例

### 快速查询
```
搜索今天的科技新闻
```

### 复杂分析
```
分析人工智能在医疗领域的应用和挑战
```

### 地区特定
```
搜索美国地区关于 AI regulations 的最新政策
```

### 深度研究
```
对量子计算的最新进展进行深度研究
```

---

## 📖 更多信息

### 文档快速导航

| 文档 | 用途 | 时间 |
|------|------|------|
| **[QUICKSTART_MCP.md](QUICKSTART_MCP.md)** | 最快速的开始指南 | 5 分钟 |
| **[MCP_README.md](MCP_README.md)** | 功能总览和示例 | 10 分钟 |
| **[MCP_SETUP.md](MCP_SETUP.md)** | 详细配置和故障排查 | 需要时查阅 |

### 新增的文件

✅ **核心文件**
- `mcp_server.py` - MCP Server 主程序
- `install_mcp.ps1` / `.sh` - 自动安装脚本
- `test_mcp_server.py` - 测试验证脚本

✅ **文档文件**
- `MCP_SETUP.md` - 详细配置指南
- `QUICKSTART_MCP.md` - 快速开始
- `MCP_README.md` - 功能总览
- `START_HERE.md` - 本文件

---

## 🔧 可用工具

你现在可以在 Claude 中使用 3 个强大的工具：

### 1. web_search_quick ⚡⚡⚡
**最快速的搜索**
- 适合：快速查询、新闻、时效性信息
- 速度：几秒钟

### 2. web_search_agentic ⚡⚡
**智能搜索**
- 适合：复杂查询、需要分析的问题
- 速度：10-30 秒

### 3. web_search_deep ⚡
**深度研究**
- 适合：学术研究、全面分析
- 速度：数分钟

---

## 🆘 遇到问题？

### 问题 1：Claude 找不到工具

**解决方案**：
1. 确保完全退出 Claude Desktop
2. 检查任务管理器，确保进程已结束
3. 重新打开 Claude Desktop

### 问题 2：工具调用失败

**解决方案**：
1. 检查 `.env` 文件配置
2. 确认 Azure OpenAI API 密钥有效
3. 运行：`python test_mcp_server.py`

### 问题 3：配置文件问题

**解决方案**：
配置文件位置：
```
C:\Users\你的用户名\AppData\Roaming\Claude\claude_desktop_config.json
```

查看详细故障排查：[MCP_SETUP.md](MCP_SETUP.md)

---

## 💡 提示和技巧

### 最佳实践

1. **指定搜索模式**：
   ```
   使用快速搜索查找...
   使用智能搜索分析...
   进行深度研究...
   ```

2. **指定地区**（可选）：
   ```
   搜索中国地区的...
   查找美国的...
   ```

3. **自然语言**：
   ```
   帮我搜索...
   查找关于...的信息
   研究...的最新进展
   ```

### 费用提示

⚠️ **注意**：
- Web Search 功能会产生费用
- 快速搜索最经济
- 深度研究可能产生多次调用
- 建议在 Azure 设置费用警报

---

## 🎓 下一步

1. ✅ 运行 `.\install_mcp.ps1`
2. ✅ 重启 Claude Desktop
3. ✅ 在 Claude 中测试搜索
4. 📖 查看其他文档了解更多功能
5. 🚀 在你的工作流中使用

---

## 🌟 功能亮点

- ✅ **无缝集成**：在 Claude 中自然使用
- ✅ **多种模式**：适应不同需求
- ✅ **自动引用**：所有结果带来源
- ✅ **地理定位**：按国家/地区搜索
- ✅ **一键安装**：自动化配置

---

## 📞 需要帮助？

### 查看文档
- 快速问题：[QUICKSTART_MCP.md](QUICKSTART_MCP.md)
- 故障排查：[MCP_SETUP.md](MCP_SETUP.md)
- 功能详情：[MCP_README.md](MCP_README.md)

### 运行测试
```powershell
python test_mcp_server.py
```

### 检查配置
```powershell
# 查看 Claude 配置文件
notepad %APPDATA%\Claude\claude_desktop_config.json
```

---

## 🎉 就这么简单！

现在你可以：
1. 在 Claude Desktop 中使用 Azure Web Search
2. 享受三种搜索模式
3. 获得带引用的搜索结果
4. 通过自然语言与搜索交互

**准备好了吗？运行 `.\install_mcp.ps1` 开始吧！** 🚀

---

**Made with ❤️ for Claude Desktop**
