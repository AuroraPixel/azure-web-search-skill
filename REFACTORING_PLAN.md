# 项目结构重组规划文档

## 📋 目录

1. [现状分析](#现状分析)
2. [重组目标](#重组目标)
3. [新目录结构](#新目录结构)
4. [详细迁移计划](#详细迁移计划)
5. [文档整合策略](#文档整合策略)
6. [执行步骤](#执行步骤)
7. [验证清单](#验证清单)
8. [风险评估](#风险评估)

---

## 🔍 现状分析

### 当前问题

#### 1. 根目录文件过多（10+ 个 Markdown 文档）
```
├── README.md
├── QUICKSTART.md
├── QUICKSTART_MCP.md
├── MCP_README.md
├── MCP_SETUP.md
├── CURSOR_README.md
├── CURSOR_SETUP.md
├── ARCHITECTURE.md
├── CHANGELOG.md
└── START_HERE.md
```

**问题：**
- 新用户不知道从哪里开始
- 文档间关系不清晰
- 维护困难，容易产生内容不一致

#### 2. 文档内容重复
- `README.md`、`MCP_README.md`、`CURSOR_README.md` 有大量重叠内容
- `QUICKSTART.md` 和 `QUICKSTART_MCP.md` 分离导致重复说明
- 多个 SETUP 文档导致配置说明分散

#### 3. 脚本文件分散（7+ 个脚本）
```
├── setup.ps1 / setup.sh
├── run.ps1 / run.sh
├── install_mcp.ps1 / install_mcp.sh
└── install_mcp_cursor.ps1
```

**问题：**
- 缺乏分类和组织
- 难以找到所需脚本
- 没有清晰的命名规范

#### 4. 配置文件混杂
```
├── env.example
├── claude_desktop_config.json
└── .cursorrules_mcp
```

**问题：**
- 配置模板与代码混在一起
- 没有统一的配置管理

---

## 🎯 重组目标

### 主要目标

1. **清晰的文档层次结构**
   - 按用户类型分类（最终用户、开发者）
   - 按功能分类（快速开始、配置指南、API 文档）
   - 减少重复内容

2. **简化的根目录**
   - 只保留 5-7 个核心文件
   - 提供清晰的入口指引

3. **组织化的脚本和配置**
   - 按用途分类脚本
   - 统一管理配置模板

4. **提升可维护性**
   - 单一信息源原则
   - 清晰的文件命名
   - 易于扩展的结构

---

## 📁 新目录结构

### 完整结构树

```
web-search/
│
├── README.md                          # 🎯 精简主文档（300-500 行）
├── START_HERE.md                      # 🚀 快速开始指引（< 100 行）
├── CHANGELOG.md                       # 📝 更新日志
├── pyproject.toml                     # 📦 项目配置
├── .env.example                       # 🔧 环境变量模板
├── uv.lock                            # 🔒 依赖锁定
│
├── docs/                              # 📚 所有文档
│   │
│   ├── README.md                      # 文档索引（指向各子目录）
│   │
│   ├── getting-started/               # 🏁 用户入门
│   │   ├── overview.md                #   项目概述和功能介绍
│   │   ├── quickstart.md              #   基础功能快速开始
│   │   ├── quickstart-mcp.md          #   MCP 功能快速开始
│   │   ├── first-search.md            #   第一次搜索指南
│   │   └── configuration.md           #   详解所有配置选项
│   │
│   ├── guides/                        # 📘 详细指南
│   │   ├── search-modes.md            #   搜索模式对比和使用
│   │   ├── mcp-setup.md               #   MCP 详细配置指南
│   │   ├── cursor-setup.md            #   Cursor 集成指南
│   │   ├── architecture.md            #   架构设计说明
│   │   └── api-reference.md           #   API 参考文档
│   │
│   ├── development/                   # 👨‍💻 开发者文档
│   │   ├── setup.md                   #   开发环境搭建
│   │   ├── testing.md                 #   测试指南
│   │   ├── contributing.md            #   贡献指南
│   │   └── deployment.md              #   部署指南
│   │
│   └── assets/                        # 🖼️ 文档资源
│       ├── images/
│       └── diagrams/
│
├── scripts/                           # 🛠️ 所有脚本
│   │
│   ├── README.md                      # 脚本使用说明
│   │
│   ├── setup/                         # ⚙️ 环境设置
│   │   ├── setup.ps1                  #   Windows 安装
│   │   └── setup.sh                   #   Unix 安装
│   │
│   ├── install-mcp/                   # 🔌 MCP 安装
│   │   ├── claude.ps1                 #   Claude Desktop (Windows)
│   │   ├── claude.sh                  #   Claude Desktop (Unix)
│   │   ├── cursor.ps1                 #   Cursor (Windows)
│   │   └── cursor.sh                  #   Cursor (Unix)
│   │
│   └── run/                           # ▶️ 运行脚本
│       ├── run.ps1                    #   Windows 运行
│       └── run.sh                     #   Unix 运行
│
├── config-templates/                  # 📋 配置模板
│   │
│   ├── README.md                      # 配置说明
│   │
│   ├── claude/                        # 🤖 Claude 相关
│   │   ├── mcp-server.json           #   Claude Desktop 配置模板
│   │   └── usage-examples.md         #   使用示例
│   │
│   └── cursor/                        # 🖊️ Cursor 相关
│       ├── mcp-rules.txt             #   Cursor MCP 规则模板
│       └── usage-examples.md         #   使用示例
│
├── src/                               # ✅ 源代码（保持不变）
│   ├── __init__.py
│   ├── config.py
│   ├── logger.py
│   ├── models.py
│   └── web_search.py
│
├── tests/                             # ✅ 测试代码（保持不变）
│   ├── test_config.py
│   └── test_models.py
│
├── examples/                          # ✅ 示例代码（保持不变）
│   ├── basic_search.py
│   ├── location_search.py
│   └── all_modes.py
│
├── main.py                            # ✅ 主程序（保持不变）
├── mcp_server.py                      # ✅ MCP 服务器（保持不变）
├── quick_test.py                      # ✅ 快速测试（保持不变）
└── test_menu.py                       # ✅ 测试菜单（保持不变）
```

---

## 🔄 详细迁移计划

### 第一阶段：目录创建

#### 1.1 创建新目录结构

```powershell
# PowerShell 命令
New-Item -ItemType Directory -Path "docs\getting-started"
New-Item -ItemType Directory -Path "docs\guides"
New-Item -ItemType Directory -Path "docs\development"
New-Item -ItemType Directory -Path "docs\assets\images"
New-Item -ItemType Directory -Path "docs\assets\diagrams"
New-Item -ItemType Directory -Path "scripts\setup"
New-Item -ItemType Directory -Path "scripts\install-mcp"
New-Item -ItemType Directory -Path "scripts\run"
New-Item -ItemType Directory -Path "config-templates\claude"
New-Item -ItemType Directory -Path "config-templates\cursor"
```

### 第二阶段：文档迁移和整合

#### 2.1 根目录文档重组

| 原文件 | 操作 | 新位置 | 说明 |
|--------|------|--------|------|
| `README.md` | 重写 | `README.md` | 保留基础介绍，添加指向 docs/ 的链接 |
| `START_HERE.md` | 重写 | `START_HERE.md` | 简化为快速导航（< 100 行） |
| `CHANGELOG.md` | 保持 | `CHANGELOG.md` | 保持不变 |
| `QUICKSTART.md` | 整合 | `docs/getting-started/quickstart.md` | 保留基础快速开始 |
| `QUICKSTART_MCP.md` | 整合 | `docs/getting-started/quickstart-mcp.md` | 保留 MCP 快速开始 |
| `ARCHITECTURE.md` | 迁移 | `docs/guides/architecture.md` | 保持不变 |
| `MCP_SETUP.md` | 整合 | `docs/guides/mcp-setup.md` | 保留详细配置 |
| `CURSOR_SETUP.md` | 整合 | `docs/guides/cursor-setup.md` | 保留 Cursor 配置 |
| `MCP_README.md` | **删除** | - | 内容合并到 README |
| `CURSOR_README.md` | **删除** | - | 内容合并到 README |

#### 2.2 新文档创建

需要创建的新文档：

1. **`docs/README.md`** - 文档导航索引
2. **`docs/getting-started/overview.md`** - 项目概述
3. **`docs/getting-started/first-search.md`** - 第一次搜索教程
4. **`docs/getting-started/configuration.md`** - 详细配置说明
5. **`docs/guides/search-modes.md`** - 搜索模式对比
6. **`docs/guides/api-reference.md`** - API 参考文档
7. **`docs/development/setup.md`** - 开发环境搭建
8. **`docs/development/testing.md`** - 测试指南
9. **`docs/development/contributing.md`** - 贡献指南
10. **`docs/development/deployment.md`** - 部署指南

#### 2.3 文档内容整合策略

**整合 MCP_README 和 CURSOR_README：**
- 将 MCP 相关内容合并到 `README.md` 的 "MCP Server 集成" 章节
- 将 Cursor 相关内容合并到 `README.md` 的 "Cursor 集成" 章节
- 详细配置指南保留在 `docs/guides/mcp-setup.md` 和 `docs/guides/cursor-setup.md`

**整合 QUICKSTART 文档：**
- `QUICKSTART.md` → `docs/getting-started/quickstart.md`（基础功能）
- `QUICKSTART_MCP.md` → `docs/getting-started/quickstart-mcp.md`（MCP 功能）
- 在 `docs/README.md` 中提供清晰的导航

### 第三阶段：脚本迁移

#### 3.1 脚本迁移映射表

| 原路径 | 新路径 | 重命名 |
|--------|--------|--------|
| `setup.ps1` | `scripts/setup/setup.ps1` | 保持 |
| `setup.sh` | `scripts/setup/setup.sh` | 保持 |
| `install_mcp.ps1` | `scripts/install-mcp/claude.ps1` | 重命名 |
| `install_mcp.sh` | `scripts/install-mcp/claude.sh` | 重命名 |
| `install_mcp_cursor.ps1` | `scripts/install-mcp/cursor.ps1` | 重命名 |
| `run.ps1` | `scripts/run/run.ps1` | 保持 |
| `run.sh` | `scripts/run/run.sh` | 保持 |

#### 3.2 脚本内容更新

需要更新所有脚本中的路径引用：
- 相对导入路径调整
- 文档链接更新
- 配置文件路径更新

### 第四阶段：配置模板迁移

#### 4.1 配置文件迁移

| 原路径 | 新路径 | 说明 |
|--------|--------|------|
| `claude_desktop_config.json` | `config-templates/claude/mcp-server.json` | 重命名并移动 |
| `.cursorrules_mcp` | `config-templates/cursor/mcp-rules.txt` | 重命名并移动 |

#### 4.2 配置说明文档

创建配置说明：
- `config-templates/README.md` - 配置总览
- `config-templates/claude/usage-examples.md` - Claude 使用示例
- `config-templates/cursor/usage-examples.md` - Cursor 使用示例

### 第五阶段：文档重写

#### 5.1 根目录文档

**新的 `README.md` 结构（约 400 行）：**

```markdown
# Azure OpenAI Web Search

## 简介
- 项目概述（50 行）
- 核心功能（50 行）
- 技术栈（30 行）

## 快速开始
- 指向 START_HERE.md（10 行）
- 30 秒快速示例（20 行）

## 功能特性
- 三种搜索模式（50 行）
- MCP Server 集成（50 行）
- Cursor 集成（30 行）

## 文档导航
- 用户文档链接（20 行）
- 开发者文档链接（20 行）

## 许可证
（10 行）
```

**新的 `START_HERE.md` 结构（< 100 行）：**

```markdown
# 从这里开始

## 新用户导航
- [ ] 我想快速体验 → quickstart.md
- [ ] 我想使用 MCP → quickstart-mcp.md
- [ ] 我想了解架构 → overview.md

## 开发者导航
- [ ] 开发环境搭建 → docs/development/setup.md
- [ ] 贡献代码 → docs/development/contributing.md

## 快速参考
- 配置指南 → configuration.md
- API 文档 → api-reference.md
```

#### 5.2 文档目录索引

**`docs/README.md` 结构：**

```markdown
# 文档目录

## 📚 用户文档
- [入门指南](getting-started/)
- [使用指南](guides/)

## 👨‍💻 开发者文档
- [开发指南](development/)

## 🔍 快速查找
- 按主题索引
- 按场景索引
```

---

## 📝 执行步骤

### 步骤 1：备份当前项目
```powershell
# 创建备份
git add -A
git commit -m "备份：重组前的完整状态"
git tag before-refactoring
```

### 步骤 2：创建新目录结构
```powershell
# 执行 2.1 中的 PowerShell 命令
```

### 步骤 3：迁移脚本文件
```powershell
# 按照迁移映射表移动脚本
# 更新脚本中的路径引用
```

### 步骤 4：迁移配置模板
```powershell
# 移动配置文件到 config-templates/
```

### 步骤 5：迁移和整合文档
```powershell
# 按照文档迁移映射表操作
# 创建新的文档索引
```

### 步骤 6：重写核心文档
```powershell
# 重写 README.md
# 重写 START_HERE.md
# 创建 docs/README.md
```

### 步骤 7：更新所有引用
```powershell
# 更新文档中的相互引用
# 更新脚本中的文档链接
# 更新代码中的配置路径
```

### 步骤 8：创建 README 文件
```powershell
# 为每个子目录创建 README.md
# scripts/README.md
# config-templates/README.md
```

### 步骤 9：删除旧文件
```powershell
# 确认所有内容已迁移
# 删除根目录的旧文档
# 删除重复文件
```

### 步骤 10：测试和验证
```powershell
# 验证所有链接有效
# 测试所有脚本正常运行
# 确认文档完整性
```

### 步骤 11：Git 提交
```powershell
git add -A
git commit -m "重构：重组项目结构和文档"
```

---

## ✅ 验证清单

### 结构验证

- [ ] 根目录只保留必要文件（< 10 个）
- [ ] 所有文档都在 `docs/` 目录中
- [ ] 所有脚本都在 `scripts/` 目录中
- [ ] 所有配置模板都在 `config-templates/` 中

### 文档验证

- [ ] README.md 简洁明了（< 500 行）
- [ ] START_HERE.md 清晰指引（< 100 行）
- [ ] 没有重复内容的文档
- [ ] 所有文档链接有效
- [ ] 文档目录索引完整

### 脚本验证

- [ ] 所有脚本已迁移
- [ ] 脚本命名清晰规范
- [ ] 脚本中的路径引用已更新
- [ ] 所有脚本可正常运行

### 配置验证

- [ ] 所有配置模板已迁移
- [ ] 配置文件命名清晰
- [ ] 配置说明文档完整

### 功能验证

- [ ] 项目可正常安装
- [ ] 所有示例代码可运行
- [ ] 测试全部通过
- [ ] MCP Server 可正常启动

### Git 验证

- [ ] 所有更改已提交
- [ ] 提交信息清晰
- [ ] 没有遗留的临时文件

---

## ⚠️ 风险评估

### 高风险项

1. **脚本路径引用失效**
   - **风险**：移动脚本后，路径引用可能失效
   - **缓解**：
     - 使用相对路径
     - 更新所有路径引用
     - 添加路径验证逻辑

2. **配置文件路径变更**
   - **风险**：代码中硬编码的配置路径可能失效
   - **缓解**：
     - 使用环境变量
     - 更新所有配置加载逻辑
     - 添加配置查找逻辑

### 中风险项

3. **文档链接失效**
   - **风险**：文档间的相互引用可能失效
   - **缓解**：
     - 使用相对路径
     - 创建链接映射表
     - 使用自动化工具检查

4. **用户习惯改变**
   - **风险**：现有用户可能找不到熟悉的文档
   - **缓解**：
     - 在 README 中添加迁移说明
     - 保留旧文档的重定向
     - 发布迁移公告

### 低风险项

5. **Git 历史混乱**
   - **风险**：大量文件移动可能导致历史混乱
   - **缓解**：
     - 使用 `git mv` 而非复制删除
     - 创建清晰的提交信息
     - 添加 refactoring 标签

---

## 📊 影响评估

### 正面影响

1. **提升用户体验**
   - 新用户更容易找到所需文档
   - 清晰的导航减少困惑
   - 专业的项目结构

2. **提升可维护性**
   - 文档结构清晰，易于更新
   - 减少重复内容
   - 单一信息源原则

3. **提升扩展性**
   - 新功能有明确的文档位置
   - 脚本和配置分类清晰
   - 易于添加新内容

### 负面影响

1. **短期学习成本**
   - 现有用户需要适应新结构
   - 文档链接可能需要更新

2. **迁移工作量**
   - 需要大量文件移动和重命名
   - 需要仔细检查所有引用
   - 需要重写核心文档

---

## 🎯 成功标准

### 量化指标

1. **根目录文件数**：从 20+ 个减少到 < 10 个
2. **文档重复率**：从 ~30% 降低到 < 5%
3. **文档层级深度**：不超过 3 层
4. **用户查找时间**：减少 50%（通过用户测试验证）

### 质化指标

1. **新用户反馈**：能够快速找到所需文档
2. **开发者反馈**：易于维护和扩展
3. **整体评价**：项目结构更专业

---

## 📅 预计时间

- **步骤 1-2**（备份和创建目录）：15 分钟
- **步骤 3-4**（迁移脚本和配置）：30 分钟
- **步骤 5-6**（迁移和重写文档）：2-3 小时
- **步骤 7-8**（更新引用和创建索引）：1 小时
- **步骤 9-10**（清理和验证）：30 分钟
- **步骤 11**（提交）：15 分钟

**总计**：约 4-5 小时

---

## 🤝 需要确认的事项

在执行重组前，请确认：

1. [ ] 是否同意新的目录结构？
2. [ ] 是否需要调整某些文档的组织方式？
3. [ ] 是否有其他需要考虑的因素？
4. [ ] 是否需要逐步迁移而非一次性重组？
5. [ ] 是否需要在迁移前通知现有用户？

---

## 📞 后续支持

重组完成后，建议：

1. **创建迁移指南**：帮助现有用户适应新结构
2. **更新 README 图标**：添加 shields.io 徽章
3. **添加贡献指南**：明确文档贡献流程
4. **设置文档检查**：在 CI 中添加链接检查
5. **定期审查**：每季度审查文档结构

---

**文档版本**：v1.0
**创建日期**：2026-01-29
**作者**：Claude Code
**状态**：待审核
