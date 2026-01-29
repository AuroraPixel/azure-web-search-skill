# 🚀 快速入门指南

这是一个 5 分钟快速入门指南，帮助你快速开始使用 Azure Web Search。

> 🤖 **想在 Claude Desktop 中使用？** 查看 [MCP Server 快速开始](QUICKSTART_MCP.md)！

## 📋 前置要求

1. **Python 3.10+** 已安装
2. **Azure OpenAI 账户** 和 API 密钥
3. **uv 包管理器**（脚本会自动安装）

## ⚡ 一键安装（推荐）

### Windows 用户

```powershell
# 在 PowerShell 中运行
.\setup.ps1
```

### macOS/Linux 用户

```bash
# 在终端中运行
chmod +x setup.sh
./setup.sh
```

脚本会自动完成：
- ✅ 安装 uv（如果未安装）
- ✅ 创建虚拟环境
- ✅ 安装所有依赖
- ✅ 创建 .env 配置文件

## 🔧 手动安装

如果你更喜欢手动安装：

```bash
# 1. 安装 uv
# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. 创建虚拟环境
uv venv

# 3. 激活虚拟环境
# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate

# 4. 安装依赖
uv pip install -e .

# 5. 复制环境变量文件
# Windows
copy env.example .env

# macOS/Linux
cp env.example .env
```

## ⚙️ 配置 Azure OpenAI

编辑 `.env` 文件，填写你的 Azure OpenAI 信息：

```env
AZURE_OPENAI_API_KEY=你的-API-密钥
AZURE_OPENAI_ENDPOINT=https://你的资源名.openai.azure.com
AZURE_OPENAI_MODEL=gpt-4o
```

### 🔑 如何获取配置信息？

1. 登录 [Azure Portal](https://portal.azure.com/)
2. 找到你的 **Azure OpenAI** 资源
3. 点击左侧菜单的 **"Keys and Endpoint"**
4. 复制：
   - **Key 1** → `AZURE_OPENAI_API_KEY`
   - **Endpoint** → `AZURE_OPENAI_ENDPOINT`
5. 在 [Azure OpenAI Studio](https://oai.azure.com/) 中创建模型部署，记下部署名称 → `AZURE_OPENAI_MODEL`

## 🎯 开始使用

### 方式 0：作为 Claude Desktop 工具（最强大）

将此项目配置为 MCP Server，在 Claude Desktop 中直接使用：

```powershell
# 运行安装脚本
.\install_mcp.ps1  # Windows
# 或
./install_mcp.sh   # macOS/Linux
```

详见：[QUICKSTART_MCP.md](QUICKSTART_MCP.md)

### 方式 1：交互式程序（最简单）

```bash
# 确保虚拟环境已激活
python main.py
```

这会启动一个交互式菜单，你可以：
- 选择搜索模式（快速/智能/深度）
- 输入查询
- 更改地区设置
- 查看漂亮的结果展示

### 方式 2：运行示例脚本

```bash
# 基础搜索示例
python examples/basic_search.py

# 地理位置搜索对比
python examples/location_search.py

# 所有模式对比
python examples/all_modes.py
```

### 方式 3：在代码中使用

```python
from src.config import get_settings
from src.web_search import AzureWebSearch

# 初始化
settings = get_settings()
search = AzureWebSearch(settings)

# 快速搜索
result = search.quick_search("2026年AI发展趋势")

# 打印结果
print(result.text)
print(f"引用数量：{len(result.citations)}")

# 获取引用源
for source in result.get_unique_sources():
    print(f"- {source['title']}: {source['url']}")
```

## 📚 三种搜索模式

### 1. 快速搜索 (Quick Search)

```python
result = search.quick_search("查询内容")
```

- ⚡ **最快**：几秒钟完成
- 📝 **适合**：简单查询、新闻资讯、快速事实查找
- 🔧 **特点**：无推理，直接返回搜索结果

### 2. 智能体搜索 (Agentic Search)

```python
result = search.agentic_search("查询内容")
```

- ⚡ **中速**：10-30秒
- 📝 **适合**：需要分析和理解的复杂查询
- 🔧 **特点**：带推理能力，可以多步骤搜索

### 3. 深度研究 (Deep Research)

```python
result = search.deep_research("研究主题")
```

- ⚡ **较慢**：数分钟
- 📝 **适合**：学术研究、深度分析、综合报告
- 🔧 **特点**：多源引用，全面深入，适合复杂主题

## 🌍 按地区搜索

```python
# 搜索美国地区的结果
result = search.quick_search("今日新闻", country="US")

# 搜索中国地区的结果
result = search.quick_search("今日新闻", country="CN")
```

支持的国家代码（ISO 3166-1 alpha-2）：
- `US` - 美国
- `CN` - 中国
- `GB` - 英国
- `JP` - 日本
- `IN` - 印度
- 等等...

## 💡 常见问题

### Q: 提示 "API key not found"

**A:** 检查 `.env` 文件是否存在，并确保 `AZURE_OPENAI_API_KEY` 已正确填写。

### Q: 提示 "Model deployment not found"

**A:** 确认：
1. 模型部署已在 Azure OpenAI Studio 中创建
2. `.env` 中的 `AZURE_OPENAI_MODEL` 与部署名称完全一致

### Q: 搜索速度很慢

**A:** 
- 快速搜索模式应该很快（几秒钟）
- 如果使用深度研究模式，数分钟是正常的
- 检查网络连接

### Q: 出现费用问题

**A:** 
- Web Search 功能会产生额外费用
- 每次搜索调用都会计费
- 建议在测试时使用快速搜索模式

## 📊 项目结构

```
azure-web-search/
├── src/                    # 核心代码
│   ├── config.py          # 配置管理
│   ├── logger.py          # 日志系统
│   ├── models.py          # 数据模型
│   └── web_search.py      # 搜索核心
├── examples/              # 使用示例
├── tests/                 # 单元测试
├── main.py               # 交互式主程序
├── .env                  # 环境变量（需创建）
└── README.md             # 完整文档
```

## 🎓 下一步

1. ✅ 运行示例脚本熟悉功能
2. 📖 阅读 [README.md](README.md) 了解完整功能
3. 🔧 查看 [examples/](examples/) 目录学习更多用法
4. 🧪 运行测试：`pytest tests/`
5. 🚀 在你的项目中集成

## 📞 需要帮助？

- 📖 查看完整文档：[README.md](README.md)
- 🌐 Azure 官方文档：https://learn.microsoft.com/azure/ai-foundry/openai/how-to/web-search
- 💬 提交 Issue 获取支持

---

**开始你的 Azure Web Search 之旅！** 🎉
