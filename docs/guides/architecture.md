# 🏗️ 项目架构设计文档

## 📐 设计理念

这个项目遵循以下设计原则：

1. **关注点分离（Separation of Concerns）**
   - 配置管理、日志、模型定义和业务逻辑各司其职
   - 每个模块有明确的职责边界

2. **类型安全（Type Safety）**
   - 使用 Pydantic 进行数据验证和类型检查
   - 所有公共接口都有完整的类型注解

3. **可测试性（Testability）**
   - 依赖注入设计，便于单元测试
   - 核心逻辑与 I/O 操作分离

4. **用户友好（User-Friendly）**
   - 丰富的日志和错误提示
   - 美观的终端输出
   - 简单的配置管理

## 📦 模块架构

```
┌─────────────────────────────────────────────────────────┐
│                      应用层 (Application)                 │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │   main.py   │  │  examples/   │  │    tests/     │  │
│  │  交互式程序   │  │  使用示例     │  │   单元测试     │  │
│  └─────────────┘  └──────────────┘  └───────────────┘  │
└─────────────────────────────────────────────────────────┘
                          ↓ 依赖
┌─────────────────────────────────────────────────────────┐
│                      业务层 (Business)                    │
│  ┌─────────────────────────────────────────────────┐   │
│  │           src/web_search.py                     │   │
│  │       AzureWebSearch 类 - 核心业务逻辑           │   │
│  │  • quick_search()   - 快速搜索                  │   │
│  │  • agentic_search() - 智能体搜索                │   │
│  │  • deep_research()  - 深度研究                  │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                          ↓ 使用
┌─────────────────────────────────────────────────────────┐
│                    数据模型层 (Models)                    │
│  ┌─────────────────────────────────────────────────┐   │
│  │              src/models.py                      │   │
│  │  • SearchMode      - 搜索模式枚举               │   │
│  │  • URLCitation     - URL 引用模型               │   │
│  │  • WebSearchResult - 搜索结果模型               │   │
│  │  • WebSearchTool   - 工具配置模型               │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                          ↓ 支持
┌─────────────────────────────────────────────────────────┐
│                   基础设施层 (Infrastructure)             │
│  ┌──────────────────┐  ┌──────────────────────────┐    │
│  │  src/config.py   │  │    src/logger.py         │    │
│  │  配置管理         │  │    日志系统               │    │
│  │  • Settings      │  │    • setup_logger()      │    │
│  │  • 环境变量验证   │  │    • Rich 格式化输出      │    │
│  └──────────────────┘  └──────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
                          ↓ 依赖
┌─────────────────────────────────────────────────────────┐
│                    外部依赖 (External)                    │
│  ┌──────────┐  ┌─────────┐  ┌──────┐  ┌───────────┐   │
│  │  OpenAI  │  │Pydantic │  │ Rich │  │  dotenv   │   │
│  │   SDK    │  │  验证    │  │ 输出 │  │ 环境变量   │   │
│  └──────────┘  └─────────┘  └──────┘  └───────────┘   │
└─────────────────────────────────────────────────────────┘
```

## 🔄 数据流

### 搜索请求流程

```
用户输入
   ↓
main.py / examples
   ↓
AzureWebSearch.search()
   ↓
构建工具配置 (_build_tools)
   ↓
调用 OpenAI API (client.responses.create)
   ↓
解析响应 (_parse_response)
   ↓
WebSearchResult
   ↓
返回给用户
```

### 配置加载流程

```
启动应用
   ↓
setup_env_file() - 检查 .env 文件
   ↓
get_settings() - 加载配置
   ↓
Pydantic 验证
   ↓
Settings 实例
   ↓
传递给 AzureWebSearch
```

## 📂 目录结构详解

```
azure-web-search/
│
├── src/                          # 核心源代码
│   ├── __init__.py              # 包初始化
│   ├── config.py                # 配置管理模块
│   │   └── Settings (Pydantic)  # 配置类，自动验证
│   ├── logger.py                # 日志配置
│   │   └── Rich Handler         # 美观的日志输出
│   ├── models.py                # 数据模型定义
│   │   ├── SearchMode          # 搜索模式枚举
│   │   ├── URLCitation         # 引用模型
│   │   ├── WebSearchResult     # 结果模型
│   │   └── WebSearchTool       # 工具配置
│   └── web_search.py            # Web Search 核心
│       └── AzureWebSearch      # 主要业务类
│
├── examples/                     # 使用示例
│   ├── basic_search.py          # 基础搜索示例
│   ├── location_search.py       # 地理位置搜索
│   └── all_modes.py             # 所有模式对比
│
├── tests/                        # 单元测试
│   ├── test_config.py           # 配置测试
│   └── test_models.py           # 模型测试
│
├── main.py                       # 交互式主程序
│
├── setup.ps1 / setup.sh         # 安装脚本
├── run.ps1 / run.sh             # 快速启动脚本
│
├── pyproject.toml               # 项目配置（uv）
├── env.example                  # 环境变量模板
│
├── README.md                    # 完整文档
├── QUICKSTART.md               # 快速入门
└── ARCHITECTURE.md             # 架构文档（本文件）
```

## 🔧 核心类设计

### 1. Settings (config.py)

```python
class Settings(BaseSettings):
    """应用程序设置 - 使用 Pydantic Settings"""
    
    # 职责：
    # - 从环境变量加载配置
    # - 验证配置的合法性
    # - 提供类型安全的配置访问
    
    # 特点：
    # - 自动从 .env 文件加载
    # - 字段验证（@field_validator）
    # - 类型提示完整
```

### 2. AzureWebSearch (web_search.py)

```python
class AzureWebSearch:
    """Azure OpenAI Web Search 客户端"""
    
    # 职责：
    # - 管理 OpenAI 客户端连接
    # - 提供不同模式的搜索方法
    # - 构建工具配置
    # - 解析和转换响应数据
    
    # 设计模式：
    # - Facade 模式：简化 API 调用
    # - Builder 模式：构建复杂的工具配置
```

### 3. WebSearchResult (models.py)

```python
class WebSearchResult(BaseModel):
    """搜索结果模型"""
    
    # 职责：
    # - 封装搜索结果数据
    # - 提供便捷的数据访问方法
    # - 确保数据结构的一致性
    
    # 特点：
    # - 不可变（Pydantic frozen=False 但不建议修改）
    # - 类型安全
    # - 提供辅助方法（如 get_unique_sources）
```

## 🎯 设计模式应用

### 1. 依赖注入 (Dependency Injection)

```python
# AzureWebSearch 接受 Settings 作为依赖
search = AzureWebSearch(settings)

# 优点：
# - 便于测试（可注入 mock settings）
# - 配置与实现分离
```

### 2. 工厂方法 (Factory Method)

```python
# get_settings() 作为工厂方法
settings = get_settings()

# 优点：
# - 集中创建逻辑
# - 便于缓存和单例实现
```

### 3. 外观模式 (Facade Pattern)

```python
# AzureWebSearch 作为 OpenAI API 的外观
search.quick_search(query)  # 简化的接口

# 而不是直接操作：
client.responses.create(
    model=...,
    tools=[...],
    input=...
)

# 优点：
# - 简化复杂的 API 调用
# - 提供领域特定的接口
```

## 🔒 错误处理策略

### 1. 配置阶段

```python
try:
    settings = get_settings()
except ValidationError as e:
    # Pydantic 验证错误
    # 提供清晰的错误信息
```

### 2. 运行阶段

```python
try:
    result = search.quick_search(query)
except OpenAIError as e:
    # API 调用错误
    # 记录日志并向用户提供友好提示
except Exception as e:
    # 其他未预期错误
    # 记录完整堆栈信息
```

## 📊 性能考虑

### 1. 连接复用

```python
# OpenAI 客户端在 AzureWebSearch 初始化时创建
# 多次搜索复用同一个客户端实例
self.client = OpenAI(...)
```

### 2. 懒加载

```python
# 配置只在需要时加载
settings = get_settings()
```

### 3. 响应解析优化

```python
# 只解析必要的字段
# 原始数据保存在 raw_response 中供调试使用
```

## 🧪 测试策略

### 1. 单元测试

- 配置验证测试 (`test_config.py`)
- 数据模型测试 (`test_models.py`)
- 使用 pytest 框架

### 2. 集成测试

- 示例程序作为集成测试
- 真实 API 调用验证

### 3. 类型检查

- 完整的类型注解
- 可使用 mypy 进行静态类型检查

## 🚀 扩展点

### 1. 添加新的搜索模式

```python
# 在 SearchMode 枚举中添加
class SearchMode(str, Enum):
    NEW_MODE = "new_mode"

# 在 AzureWebSearch 中添加方法
def new_mode_search(self, query: str) -> WebSearchResult:
    return self.search(query, mode=SearchMode.NEW_MODE)
```

### 2. 自定义响应解析

```python
# 在 _parse_response 方法中扩展解析逻辑
def _parse_response(self, response: Any) -> WebSearchResult:
    # 添加新的解析逻辑
    pass
```

### 3. 添加新的配置项

```python
# 在 Settings 类中添加字段
class Settings(BaseSettings):
    new_config: str = Field(default="value", description="...")
```

## 📈 未来改进方向

1. **异步支持**
   - 使用 `asyncio` 和 `aiohttp`
   - 并发处理多个搜索请求

2. **缓存机制**
   - 缓存搜索结果
   - 减少 API 调用次数和费用

3. **流式响应**
   - 支持流式输出搜索结果
   - 改善用户体验

4. **重试机制**
   - API 调用失败自动重试
   - 指数退避策略

5. **监控和指标**
   - 搜索性能监控
   - 费用追踪

## 🤝 贡献指南

如果你想改进这个项目：

1. 遵循现有的代码风格
2. 添加适当的类型注解
3. 编写单元测试
4. 更新相关文档
5. 使用 Black 和 Ruff 格式化代码

---

**设计哲学：简单、清晰、可维护** ✨
