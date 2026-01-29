# 更新日志

## [2026-01-29] - v2.0.0 - FastMCP 迁移和 Skills Provider

### 🎁 重大更新

#### 迁移到 FastMCP 框架
- **完全重写 MCP Server**：从旧的 `mcp` 包迁移到 `FastMCP` 框架
- **更简洁的 API**：使用装饰器模式，代码更清晰易读
- **更好的开发体验**：改进的类型提示和错误处理
- **性能提升**：优化的异步处理和缓存机制

#### 新增 Skills Provider 支持
- **技能系统**：支持将 AI 技能作为 MCP 资源暴露
- **三个内置技能**：
  - Research Assistant - 研究助手
  - News Analyzer - 新闻分析
  - Code Reviewer - 代码审查
- **技能目录**：`skills/` 目录用于存放技能定义
- **可扩展**：轻松添加自定义技能

### 🔄 代码变更

#### MCP Server 重构 (`bin/mcp_server.py`)
- 使用 `@mcp.tool()` 装饰器定义工具
- 使用 `@mcp.resource()` 装饰器定义资源
- 使用 `@mcp.prompt()` 装饰器定义提示
- 新增 `setup_skills_provider()` 函数
- 改进的错误处理和日志记录

#### 依赖更新 (`pyproject.toml`)
- 移除：`mcp>=1.1.2`
- 新增：`fastmcp>=0.1.0`

### 📁 新增文件

#### 技能定义
- `skills/research-assistant/SKILL.md` - 研究助手技能
- `skills/news-analyzer/SKILL.md` - 新闻分析技能
- `skills/code-reviewer/SKILL.md` - 代码审查技能
- `skills/README.md` - 技能系统说明

#### 文档
- `docs/guides/fastmcp-guide.md` - FastMCP 完整指南（80KB）

### 📝 更新文档

- `docs/guides/mcp-setup.md` - 更新为 FastMCP 版本
  - 新增 v2.0.0 特性说明
  - 更新安装步骤
  - 添加 Skills Provider 使用指南
  - 新增从旧版本升级说明

### ✨ 新功能

#### MCP 工具
所有工具保持兼容，但使用 FastMCP 重新实现：
- `web_search_quick` - 快速搜索
- `web_search_agentic` - 智能体搜索

#### MCP 资源
- `config://server` - 服务器配置信息
- `search://modes` - 搜索模式说明
- `skill://research-assistant` - 研究助手技能
- `skill://news-analyzer` - 新闻分析技能
- `skill://code-reviewer` - 代码审查技能

#### MCP 提示
- `research_assistant` - 研究助手提示模板
- `news_analyzer` - 新闻分析提示模板

### 🔧 改进

- **类型安全**：完整的类型注解
- **文档字符串**：详细的函数文档
- **错误处理**：更友好的错误信息
- **日志记录**：改进的日志输出
- **代码组织**：更清晰的模块划分

### 📊 兼容性

#### 保持兼容
- 配置文件格式无需更改
- 工具名称和参数保持不变
- 现有集成无需修改

#### 需要更新
- 依赖包需要重新安装：`uv pip install -e .`
- 首次运行需要安装 FastMCP

### 🚀 使用示例

#### 在 Claude Desktop 中

```bash
# 使用工具
使用 web_search_quick 搜索 "Python 3.12 新特性"

# 使用技能
使用 research-assistant 技能研究 "量子计算应用"
使用 news-analyzer 技能分析 "今日科技新闻"
使用 code-reviewer 技能查找 "最佳实践"
```

#### 创建自定义技能

```bash
# 1. 创建技能目录
mkdir skills/my-skill

# 2. 创建 SKILL.md
cat > skills/my-skill/SKILL.md << EOF
# My Custom Skill

## 概述
技能描述

## 能力
- 能力 1
- 能力 2
...
EOF

# 3. 重启 MCP Server
# 技能会自动被发现并可用
```

### 🐛 修复问题

- 修复了路径计算问题（使用 `Path` 对象）
- 修复了技能目录扫描逻辑
- 改进了错误消息的清晰度

### 📚 相关资源

- [FastMCP 官方文档](https://gofastmcp.com)
- [FastMCP 完整指南](docs/guides/fastmcp-guide.md)
- [MCP 设置指南](docs/guides/mcp-setup.md)

---

## [2026-01-29] - 项目结构重组

### 🎁 重大改进
- **重组项目结构**：更清晰的目录组织和文档分类
- **文档整合**：减少重复，统一信息源
- **脚本分类**：按用途组织到 `scripts/` 目录
- **配置模板**：统一管理在 `config-templates/` 目录

### 📁 结构变更

#### 新增目录
- `docs/` - 所有文档分类存放
  - `getting-started/` - 用户入门文档
  - `guides/` - 使用指南
  - `development/` - 开发者文档
  - `assets/` - 文档资源
- `scripts/` - 所有脚本文件
  - `setup/` - 环境设置
  - `install-mcp/` - MCP 安装
  - `run/` - 运行脚本
- `config-templates/` - 配置文件模板
  - `claude/` - Claude Desktop 配置
  - `cursor/` - Cursor 配置

#### 文档迁移
- `QUICKSTART.md` → `docs/getting-started/quickstart.md`
- `QUICKSTART_MCP.md` → `docs/getting-started/quickstart-mcp.md`
- `MCP_SETUP.md` → `docs/guides/mcp-setup.md`
- `CURSOR_SETUP.md` → `docs/guides/cursor-setup.md`
- `ARCHITECTURE.md` → `docs/guides/architecture.md`

#### 文档整合（删除重复）
- `MCP_README.md` - 内容已合并到 `README.md`
- `CURSOR_README.md` - 内容已合并到 `README.md`

#### 脚本迁移
- `setup.ps1` / `setup.sh` → `scripts/setup/`
- `install_mcp.ps1` → `scripts/install-mcp/claude.ps1`
- `install_mcp_cursor.ps1` → `scripts/install-mcp/cursor.ps1`
- `run.ps1` / `run.sh` → `scripts/run/`

#### 配置文件迁移
- `claude_desktop_config.json` → `config-templates/claude/mcp-server.json`
- `.cursorrules_mcp` → `config-templates/cursor/mcp-rules.txt`

### 📝 新增文档
- `docs/README.md` - 文档索引
- `scripts/README.md` - 脚本使用说明
- `config-templates/README.md` - 配置说明
- `START_HERE.md` - 快速导航指引（重写）
- `REFACTORING_PLAN.md` - 重组规划文档

### 🔧 文档更新
- `README.md` - 简化结构，添加文档导航
- 所有文档中的链接已更新到新路径

### ✅ 改进效果
- 根目录文件数从 20+ 减少到 < 10
- 文档重复率显著降低
- 更清晰的文档层次结构
- 更专业的项目组织

---

## [2026-01-28] - 新增 MCP Server 支持

### 🚀 重大新功能
- **MCP Server 集成**
  - 添加了 Model Context Protocol (MCP) Server 支持
  - 可以在 Claude Desktop 中作为工具直接使用
  - 提供两个工具：`web_search_quick`、`web_search_agentic`
  
### 📝 新增文件
1. **`mcp_server.py`** - MCP Server 主程序
   - 实现了 MCP 协议的 Server 端
   - 将 Web Search 功能封装为 Claude 可调用的工具
   - 支持异步操作和标准输入输出

2. **`scripts/install-mcp/`** - MCP 安装脚本
   - `claude.ps1` / `claude.sh` - Claude Desktop 安装
   - `cursor.ps1` / `cursor.sh` - Cursor 编辑器安装
   - 自动配置 MCP Server
   - 一键安装所有依赖和配置

3. **`test_mcp_server.py`** - MCP Server 测试脚本
   - 5 个全面的配置检查测试
   - 验证依赖、环境配置、客户端、服务器文件和 Claude 配置

4. **`docs/guides/mcp-setup.md`** - 详细配置指南
   - 完整的 MCP Server 设置步骤
   - 故障排查指南
   - 使用示例和最佳实践

5. **`docs/getting-started/quickstart-mcp.md`** - MCP 快速开始指南
   - 5 分钟快速配置指南
   - 简化的安装步骤
   - 常见问题和解决方案

6. **`config-templates/claude/mcp-server.json`** - Claude 配置示例
   - MCP Server 配置模板
   - 适用于不同操作系统

### 📦 依赖更新
- **新增依赖**: `mcp>=1.1.2`
  - 添加到 `pyproject.toml` 的 dependencies 列表
  - 支持 Model Context Protocol 标准

### 📖 文档更新
1. **`README.md`**
   - 在特性列表中添加了 MCP Server 支持
   - 新增"MCP Server 功能"章节
   - 更新了"使用方式"章节，增加"方式 1: 作为 MCP Server 使用"
   - 更新了参考文档链接

2. **`QUICKSTART.md`**
   - 添加了 MCP Server 快速开始的提示
   - 新增"方式 0: 作为 Claude Desktop 工具"
   - 添加了 MCP 相关文档链接

### 🎯 可用的 MCP 工具

#### 1. web_search_quick
- **功能**: 快速网络搜索（无推理）
- **参数**: 
  - `query` (必需): 搜索查询字符串
  - `country` (可选): 国家代码，如 US、CN、JP
- **适用**: 时效性信息、快速查询

#### 2. web_search_agentic
- **功能**: 智能体搜索（带推理）
- **参数**: 
  - `query` (必需): 搜索查询字符串
  - `country` (可选): 国家代码
- **适用**: 复杂查询、需要分析的问题

### 🔧 使用方式

#### 快速安装
```powershell
# Windows - Claude Desktop
.\scripts\install-mcp\claude.ps1

# Windows - Cursor
.\scripts\install-mcp\cursor.ps1

# macOS/Linux - Claude Desktop
bash scripts/install-mcp/claude.sh

# macOS/Linux - Cursor
bash scripts/install-mcp/cursor.sh
```

#### 验证安装
```bash
python test_mcp_server.py
```

#### 在 Claude Desktop 中使用
```
使用 web search 搜索 "2026年人工智能发展趋势"
```

### 💡 技术实现
- 使用 `mcp` Python 包实现协议
- 通过 stdio 与 Claude Desktop 通信
- JSON-RPC 格式的工具调用
- 异步处理搜索请求
- 完整的错误处理和日志记录

### 📊 项目结构更新
```
azure-web-search/
├── mcp_server.py              # MCP Server 主程序（新增）
├── install_mcp.ps1            # Windows 安装脚本（新增）
├── install_mcp.sh             # macOS/Linux 安装脚本（新增）
├── test_mcp_server.py         # MCP 测试脚本（新增）
├── MCP_SETUP.md               # 详细配置指南（新增）
├── QUICKSTART_MCP.md          # 快速开始指南（新增）
├── claude_desktop_config.json # 配置示例（新增）
├── src/                       # 核心代码
├── examples/                  # 使用示例
├── tests/                     # 单元测试
└── ...
```

---

## [2026-01-28] - 移除深度研究功能

### 🗑️ 移除的功能
- **交互式主程序 (`main.py`)**
  - 移除了菜单选项 3（深度研究）
  - 更新了选项编号：原选项 4（更改国家）现在是选项 3
  - 简化了菜单选择逻辑

- **示例文件 (`examples/all_modes.py`)**
  - 移除了深度研究模式的演示代码
  - 更新文件描述为"搜索模式对比示例（快速搜索 vs 智能体搜索）"
  - 保留了快速搜索和智能体搜索的对比示例

### ✅ 当前状态
- 深度研究相关能力已移除，仅保留快速搜索与智能体搜索两种模式

### 📝 更新的文件
1. `main.py` - 主交互式程序
2. `examples/all_modes.py` - 模式对比示例

### 🎯 当前可用的搜索模式

#### 1. 快速搜索 (Quick Search)
- **速度**: ⚡⚡⚡ 非常快（几秒钟）
- **适用场景**: 
  - 简单查询
  - 时效性信息
  - 快速事实查找

#### 2. 智能体搜索 (Agentic Search)
- **速度**: ⚡⚡ 较快（10-30秒）
- **适用场景**: 
  - 复杂查询
  - 需要分析的问题
  - 多步骤推理

### 💡 使用建议
- 大多数情况下使用**快速搜索**即可满足需求
- 需要深入分析时使用**智能体搜索**

### 🔧 技术细节
- 菜单选项从 5 个减少到 4 个（包括退出选项）
- 简化了用户选择流程
- 减少了等待时间较长的操作选项

---

## [2026-01-28] - Bug 修复

### 🐛 修复的问题
1. **字符串拼接错误**
   - 修复了 `main.py` 中 `console.print("\n" + Panel(...))` 的错误
   - 改为分开打印：`console.print("")` 和 `console.print(Panel(...))`

2. **Windows 编码问题**
   - 在测试脚本中添加了 UTF-8 编码设置
   - 移除了可能导致编码错误的 emoji 字符
   - 使用纯文本标签替代（如 `[OK]`, `[FAIL]`, `[TEST 1]` 等）

### 📦 依赖管理
- 修复了 `pyproject.toml` 的打包配置
- 添加了 `[tool.hatch.build.targets.wheel]` 配置
- 指定打包目录为 `["src"]`

---

## 功能清单

### ✅ 已实现的功能
- [x] 快速搜索功能
- [x] 智能体搜索功能
- [x] 地理位置定制搜索
- [x] 配置管理（环境变量）
- [x] 日志系统
- [x] 交互式主程序
- [x] 完整的示例代码
- [x] 单元测试
- [x] 完整的文档

### 🔧 技术栈
- Python 3.10+
- uv (包管理)
- OpenAI SDK
- Pydantic (配置和数据验证)
- Rich (终端 UI)
- pytest (测试)

---

最后更新：2026-01-28
