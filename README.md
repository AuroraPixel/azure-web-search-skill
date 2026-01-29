# Azure OpenAI Web Search

一个功能完整、架构清晰的 Azure OpenAI Web Search 集成项目，使用 Python 实现，支持多种搜索模式和配置选项。

## ✨ 特性

- 🔍 **三种搜索模式**
  - 快速搜索（Quick Search）：无推理，快速获取结果
  - 智能体搜索（Agentic Search）：带推理的多步骤搜索
  - 深度研究（Deep Research）：深入的多源研究分析

- 🤖 **MCP Server 支持**：可作为 Claude Desktop 的 MCP Server 使用
- 🌍 **地理位置支持**：根据不同国家/地区定制搜索结果
- 📚 **自动引用管理**：自动提取和管理 URL 引用
- 🎨 **美观的输出**：使用 Rich 库提供漂亮的终端输出
- ⚙️ **完善的配置**：基于 Pydantic 的类型安全配置管理
- 🛠️ **开发工具集成**：包含 Black、Ruff 等开发工具

## 📁 项目结构

```
azure-web-search/
├── src/
│   ├── __init__.py          # 包初始化
│   ├── config.py            # 配置管理（Pydantic Settings）
│   ├── logger.py            # 日志配置（Rich Logger）
│   ├── models.py            # 数据模型定义
│   └── web_search.py        # Web Search 核心功能
├── examples/
│   ├── __init__.py
│   ├── basic_search.py      # 基础搜索示例
│   ├── location_search.py   # 地理位置搜索示例
│   └── all_modes.py         # 所有模式对比示例
├── pyproject.toml           # uv 项目配置
├── env.example              # 环境变量模板
├── .gitignore              # Git 忽略文件
└── README.md               # 项目文档
```

## 🚀 快速开始

> 💡 **想在 Claude Desktop 中使用？** 查看 [MCP_SETUP.md](MCP_SETUP.md) 了解如何配置为 MCP Server！

### 1. 环境准备

确保已安装 [uv](https://github.com/astral-sh/uv)：

```bash
# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. 安装依赖

```bash
# 使用 uv 创建虚拟环境并安装依赖
uv venv
uv pip install -e .
```

### 3. 配置环境变量

复制环境变量模板并填写配置：

```bash
# Windows
copy env.example .env

# macOS/Linux
cp env.example .env
```

编辑 `.env` 文件，填写你的 Azure OpenAI 配置：

```env
# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=你的API密钥
AZURE_OPENAI_ENDPOINT=https://你的资源名.openai.azure.com
AZURE_OPENAI_MODEL=gpt-4o
AZURE_OPENAI_API_VERSION=2024-12-01-preview

# Web Search 配置
WEB_SEARCH_COUNTRY=CN

# 日志级别
LOG_LEVEL=INFO
```

#### 🔑 获取 Azure OpenAI 配置

1. 登录 [Azure Portal](https://portal.azure.com/)
2. 导航到你的 Azure OpenAI 资源
3. 在左侧菜单找到 **"Keys and Endpoint"**
4. 复制以下信息：
   - **Key 1** 或 **Key 2** → `AZURE_OPENAI_API_KEY`
   - **Endpoint** → `AZURE_OPENAI_ENDPOINT`
5. 在 **Azure OpenAI Studio** 中创建模型部署，记下部署名称 → `AZURE_OPENAI_MODEL`

### 4. 激活虚拟环境

```bash
# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

# Windows (CMD)
.\.venv\Scripts\activate.bat

# macOS/Linux
source .venv/bin/activate
```

## 📖 使用方式

### 方式 1：作为 MCP Server 使用（推荐）

将此项目配置为 Claude Desktop 的 MCP Server，直接在 Claude 对话中使用 Web Search 功能。

详细配置步骤请查看：**[MCP_SETUP.md](MCP_SETUP.md)**

配置完成后，在 Claude Desktop 中可以这样使用：
```
请使用 web search 搜索"2026年人工智能发展趋势"
```

### 方式 2：作为 Python 库使用

#### 基础搜索

```bash
python examples/basic_search.py
```

```python
from src.config import get_settings
from src.web_search import AzureWebSearch

# 加载配置
settings = get_settings()

# 创建搜索客户端
search = AzureWebSearch(settings)

# 执行快速搜索
result = search.quick_search("2026年人工智能发展趋势")

print(result.text)
print(f"引用数量：{len(result.citations)}")
```

### 按地理位置搜索

```bash
python examples/location_search.py
```

```python
# 搜索美国地区的结果
result = search.quick_search("今天的新闻", country="US")

# 搜索中国地区的结果
result = search.quick_search("今天的新闻", country="CN")
```

### 所有搜索模式对比

```bash
python examples/all_modes.py
```

## 🔧 API 使用说明

### AzureWebSearch 类

```python
class AzureWebSearch:
    def __init__(self, settings: Settings):
        """初始化客户端"""
        
    def quick_search(
        self, 
        query: str, 
        country: Optional[str] = None
    ) -> WebSearchResult:
        """快速搜索（无推理）"""
        
    def agentic_search(
        self, 
        query: str, 
        country: Optional[str] = None
    ) -> WebSearchResult:
        """智能体搜索（带推理）"""
        
    def deep_research(
        self,
        query: str,
        country: Optional[str] = None,
        include_code_interpreter: bool = False
    ) -> WebSearchResult:
        """深度研究（需要 o3-deep-research 模型）"""
```

### WebSearchResult 模型

```python
class WebSearchResult:
    text: str                           # 搜索结果文本
    citations: List[URLCitation]        # 引用列表
    search_calls: List[WebSearchCall]   # 搜索调用列表
    raw_response: Optional[Dict]        # 原始响应数据
    
    def get_unique_sources(self) -> List[Dict[str, str]]:
        """获取唯一的引用源列表"""
```

## 🌍 支持的国家代码

使用 ISO 3166-1 alpha-2 标准的两字母国家代码：

- `US` - 美国
- `CN` - 中国
- `GB` - 英国
- `JP` - 日本
- `DE` - 德国
- `FR` - 法国
- `IN` - 印度
- 更多...

## 🔄 搜索模式对比

| 模式 | 速度 | 深度 | 推理能力 | 适用场景 |
|-----|------|------|---------|---------|
| Quick Search | ⚡⚡⚡ | ⭐ | ❌ | 快速查询、时效性信息 |
| Agentic Search | ⚡⚡ | ⭐⭐ | ✅ | 复杂查询、需要分析 |
| Deep Research | ⚡ | ⭐⭐⭐ | ✅✅ | 深度研究、学术调查 |

## 🛠️ 开发工具

### 安装开发依赖

```bash
uv pip install -e ".[dev]"
```

### 代码格式化

```bash
# 使用 Black 格式化代码
black src/ examples/

# 使用 Ruff 检查代码
ruff check src/ examples/
```

### 运行测试

```bash
pytest
```

## 📋 依赖说明

- **openai** (>=1.57.0) - Azure OpenAI SDK
- **python-dotenv** (>=1.0.0) - 环境变量管理
- **pydantic** (>=2.10.0) - 数据验证和设置管理
- **pydantic-settings** (>=2.6.0) - Pydantic 设置扩展
- **rich** (>=13.9.0) - 美观的终端输出

## ⚠️ 注意事项

1. **费用提醒**
   - Web Search 功能会产生额外费用
   - 每次搜索调用都会计费
   - Deep Research 模式可能产生多次搜索调用

2. **数据隐私**
   - 使用 Grounding with Bing Search 服务
   - 数据可能流向客户合规边界之外
   - Microsoft 隐私声明和使用条款适用

3. **模型要求**
   - 基础搜索：支持 GPT-4 及更高版本
   - Deep Research：需要 `o3-deep-research` 模型
   - 推理搜索：需要支持推理能力的模型

4. **运行时间**
   - Quick Search：通常几秒钟
   - Agentic Search：可能需要 10-30 秒
   - Deep Research：可能需要数分钟

## 🤖 MCP Server 功能

本项目支持作为 Model Context Protocol (MCP) Server 运行，可以集成到 Claude Desktop 中。

**支持的工具：**
- `web_search_quick` - 快速搜索
- `web_search_agentic` - 智能体搜索  
- `web_search_deep` - 深度研究

**配置指南：** 查看 [MCP_SETUP.md](MCP_SETUP.md) 了解详细配置步骤

## 📚 参考文档

- [MCP Server 配置指南](MCP_SETUP.md) - 如何配置为 Claude Desktop 工具
- [Azure OpenAI Web Search 官方文档](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/web-search)
- [Model Context Protocol](https://modelcontextprotocol.io/) - MCP 协议文档
- [Grounding with Bing 使用条款](https://www.microsoft.com/licensing/terms)
- [Azure OpenAI 定价](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/)

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📞 支持

如有问题，请：
1. 查看官方文档
2. 提交 GitHub Issue
3. 联系 Azure 技术支持

---

**Made with ❤️ using Python & Azure OpenAI**
