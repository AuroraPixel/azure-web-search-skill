# FastMCP 完整指南

## 📖 目录

- [什么是 FastMCP](#什么是-fastmcp)
- [核心概念](#核心概念)
- [快速开始](#快速开始)
- [MCP 组件详解](#mcp-组件详解)
- [Providers 详解](#providers-详解)
- [Skills Provider 完全指南](#skills-provider-完全指南)
- [高级用法](#高级用法)
- [最佳实践](#最佳实践)

---

## 什么是 FastMCP

### 定义

**FastMCP** 是构建 MCP (Model Context Protocol) 应用程序的 Python 标准框架。它是目前最流行的 MCP 实现框架，为所有语言的 MCP 服务器中的 **70%** 提供支持。

### 主要特点

1. **标准化**: 遵循 MCP 协议规范，确保与其他 MCP 客户端兼容
2. **简单易用**: 提供直观的 API，使用装饰器模式快速创建工具
3. **高性能**: 基于 Python 异步编程，支持高并发操作
4. **灵活扩展**: 支持多种组件来源和转换方式
5. **社区活跃**: 拥有庞大的用户基础和丰富的文档

### 适用场景

- 为 LLM (大语言模型) 添加自定义工具
- 构建知识库搜索服务
- 创建自动化工作流工具
- 集成外部 API 到 AI 助手
- 开发技能管理系统

---

## 核心概念

FastMCP 的架构基于三个核心抽象层：

### 1. Components (组件)

组件是 MCP 中可以向客户端暴露的基本单元。FastMCP 支持三种组件类型：

#### Tools (工具)
- **用途**: 执行操作并返回结果
- **特点**: 可带参数，有明确的输入输出
- **示例**: 搜索函数、计算器、API 调用

#### Resources (资源)
- **用途**: 提供数据访问
- **特点**: 只读，类似文件系统
- **示例`: 文本文件、图片、配置数据

#### Prompts (提示)
- **用途**: 预定义的提示模板
- **特点**: 可参数化，支持动态生成
- **示例**: 代码审查模板、文档生成模板

### 2. Providers (提供者)

提供者是组件的来源。FastMCP 支持多种提供者类型：

#### 装饰器函数提供者
使用 `@mcp.tool()`, `@mcp.resource()` 等装饰器直接定义组件

#### 文件系统提供者
从文件系统自动发现和暴露组件

#### OpenAPI 规范提供者
从 OpenAPI/Swagger 规范自动生成工具

#### 远程服务器提供者
从其他 MCP 服务器代理组件

#### Skills Provider (技能提供者)
从技能目录暴露 AI 技能作为 MCP 资源

### 3. Transforms (转换)

转换用于塑造客户端看到的组件视图：

- **命名转换**: 修改组件名称
- **描述转换**: 修改组件描述
- **验证转换**: 添加或修改输入验证
- **权限转换**: 控制组件访问权限

---

## 快速开始

### 安装

```bash
# 使用 uv (推荐)
uv pip install fastmcp

# 使用 pip
pip install fastmcp
```

### 基础示例

创建第一个 MCP 服务器：

```python
from fastmcp import FastMCP

# 创建 MCP 服务器实例
mcp = FastMCP("Demo Server 🚀")

# 定义一个工具
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together.

    Args:
        a: First number
        b: Second number

    Returns:
        Sum of the two numbers
    """
    return a + b

# 启动服务器
if __name__ == "__main__":
    mcp.run()
```

### 运行服务器

```bash
# 使用 Python 直接运行
python my_server.py

# 或安装后运行
uv pip install -e .
my-mcp-server
```

---

## MCP 组件详解

### 1. Tools (工具)

#### 基础工具定义

```python
from fastmcp import FastMCP
from typing import List

mcp = FastMCP("Weather Service")

@mcp.tool()
def get_weather(city: str) -> str:
    """Get current weather for a city.

    Args:
        city: Name of the city

    Returns:
        Weather description
    """
    # 实际应用中这里会调用天气 API
    return f"Weather in {city}: Sunny, 22°C"
```

#### 带复杂类型的工具

```python
from pydantic import BaseModel

class SearchRequest(BaseModel):
    query: str
    max_results: int = 10
    include_snippets: bool = True

class SearchResult(BaseModel):
    title: str
    url: str
    snippet: str

@mcp.tool()
def web_search(request: SearchRequest) -> List[SearchResult]:
    """Search the web for information.

    Args:
        request: Search parameters

    Returns:
        List of search results
    """
    # 实现搜索逻辑
    return [
        SearchResult(
            title="Example",
            url="https://example.com",
            snippet="Example snippet"
        )
    ]
```

#### 异步工具

```python
import asyncio

@mcp.tool()
async def async_operation(task_id: str) -> str:
    """Perform an async operation.

    Args:
        task_id: Task identifier

    Returns:
        Operation result
    """
    await asyncio.sleep(1)  # 模拟异步操作
    return f"Task {task_id} completed"
```

### 2. Resources (资源)

#### 基础资源定义

```python
@mcp.resource("config://app")
def get_config() -> str:
    """Get application configuration."""
    return """
    {
        "app_name": "My App",
        "version": "1.0.0"
    }
    """
```

#### 动态资源

```python
@mcp.resource("logs://{date}")
def get_logs(date: str) -> str:
    """Get logs for a specific date.

    Args:
        date: Date in YYYY-MM-DD format
    """
    log_file = f"/var/log/app/{date}.log"
    with open(log_file, 'r') as f:
        return f.read()
```

#### 文件系统资源

```python
from pathlib import Path

# 暴露整个目录
@mcp.resource("files://docs")
def serve_docs():
    """Serve documentation files."""
    return Path("./docs")
```

### 3. Prompts (提示)

#### 基础提示定义

```python
@mcp.prompt()
def code_review(code: str) -> str:
    """Generate a code review prompt.

    Args:
        code: Code to review

    Returns:
        Formatted review prompt
    """
    return f"""Please review the following code:

```python
{code}
```

Focus on:
1. Code quality
2. Potential bugs
3. Performance issues
4. Best practices
"""
```

#### 模板化提示

```python
@mcp.prompt()
def document_template(title: str, content: str) -> str:
    """Generate a documentation template.

    Args:
        title: Document title
        content: Main content

    Returns:
        Formatted documentation
    """
    return f"""# {title}

## Overview
{content}

## References
- [Related Documentation](https://example.com)
"""
```

---

## Providers 详解

### 装饰器提供者

这是最常用和最直观的方式：

```python
from fastmcp import FastMCP

mcp = FastMCP("Decorator Example")

@mcp.tool()
def tool1():
    """Tool 1"""
    pass

@mcp.tool()
def tool2():
    """Tool 2"""
    pass
```

### 文件系统提供者

自动从目录中发现 Python 文件并加载工具：

```python
from fastmcp import FastMCP
from pathlib import Path

mcp = FastMCP("File System Provider")

# 从 tools/ 目录加载所有工具
mcp.add_provider(FileSystemProvider(Path("./tools")))
```

目录结构：
```
tools/
├── search.py
│   @mcp.tool()
│   def web_search(): ...
├── database.py
│   @mcp.tool()
│   def query_db(): ...
```

### OpenAPI 提供者

从 OpenAPI 规范自动生成工具：

```python
from fastmcp import FastMCP
from fastmcp.providers.openapi import OpenAPIProvider

mcp = FastMCP("API Integration")

# 加载 OpenAPI 规范
mcp.add_provider(OpenAPIProvider(
    spec_url="https://api.example.com/openapi.json",
    base_url="https://api.example.com"
))
```

### 远程服务器提供者

从其他 MCP 服务器代理工具：

```python
from fastmcp import FastMCP
from fastmcp.providers.remote import RemoteServerProvider

mcp = FastMCP("Proxy Server")

# 连接到远程 MCP 服务器
mcp.add_provider(RemoteServerProvider(
    url="http://localhost:3000/sse"
))
```

---

## Skills Provider 完全指南

### 什么是 Skills Provider

**Skills Provider** 是 FastMCP 3.0.0 引入的功能，用于将 AI 技能目录作为 MCP 资源暴露。技能是包含指令和支持文件的目录。

### 技能目录结构

标准的技能目录结构：

```
~/.claude/skills/
├── pdf-processing/
│   ├── SKILL.md          # 主指令文件
│   ├── reference.md      # 参考文档
│   ├── examples/         # 示例目录
│   │   ├── basic.pdf
│   │   └── advanced.pdf
│   └── config.json       # 技能配置
├── code-review/
│   ├── SKILL.md
│   ├── checklist.md
│   └── templates/
└── documentation/
    ├── SKILL.md
    └── standards.md
```

### SKILL.md 文件格式

```markdown
# PDF Processing Skill

## Overview
This skill helps process and analyze PDF documents using specialized tools.

## Capabilities
- Extract text from PDFs
- Analyze document structure
- Generate summaries
- Convert between formats

## Usage
1. Upload your PDF document
2. Specify the processing type
3. Review the extracted information

## Tools Required
- pdf-extract
- text-analyzer
- summary-generator
```

### 单个技能提供者

```python
from fastmcp import FastMCP
from fastmcp.providers.skills import SkillProvider
from pathlib import Path

mcp = FastMCP("Single Skill Server")

# 添加单个技能目录
skill_path = Path("./skills/pdf-processing")
mcp.add_provider(SkillProvider(skill_path))

# 运行服务器
mcp.run()
```

访问资源：
```
skill://pdf-processing
```

### 技能目录提供者

```python
from fastmcp import FastMCP
from fastmcp.providers.skills import SkillsDirectoryProvider
from pathlib import Path

mcp = FastMCP("Multi Skill Server")

# 添加整个技能目录
skills_dir = Path("~/.claude/skills").expanduser()
mcp.add_provider(SkillsDirectoryProvider(skills_dir))

# 运行服务器
mcp.run()
```

可用资源：
```
skill://pdf-processing
skill://code-review
skill://documentation
```

### 供应商特定提供者

#### Claude Desktop Skills

```python
from fastmcp.providers.skills import ClaudeSkillsProvider

mcp = FastMCP("Claude Skills Integration")

# 自动从 Claude Desktop 技能目录加载
mcp.add_provider(ClaudeSkillsProvider())
```

默认路径：
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

#### Cursor Skills

```python
from fastmcp.providers.skills import CursorSkillsProvider

mcp = FastMCP("Cursor Skills Integration")

# 从 Cursor IDE 加载技能
mcp.add_provider(CursorSkillsProvider())
```

默认路径：
- **Windows**: `%APPDATA%\Cursor\User\globalStorage\mcp.json`
- **macOS**: `~/Library/Application Support/Cursor/User/globalStorage/mcp.json`
- **Linux**: `~/.config/Cursor/User/globalStorage/mcp.json`

#### VSCode Skills

```python
from fastmcp.providers.skills import VSCodeSkillsProvider

mcp = FastMCP("VSCode Skills Integration")

# 从 VSCode 加载技能
mcp.add_provider(VSCodeSkillsProvider())
```

### 技能清单 (Manifest)

每个技能自动提供 `_manifest` 资源：

```python
# 访问技能清单
manifest = mcp.get_resource("skill://pdf-processing/_manifest")

# 返回格式
{
    "name": "pdf-processing",
    "version": "1.0.0",
    "description": "PDF processing capabilities",
    "files": [
        "SKILL.md",
        "reference.md",
        "examples/basic.pdf"
    ],
    "capabilities": [
        "text-extraction",
        "structure-analysis"
    ]
}
```

### 动态技能加载

```python
from fastmcp import FastMCP
from fastmcp.providers.skills import SkillsDirectoryProvider
from pathlib import Path

mcp = FastMCP("Dynamic Skills")

# 创建热重载的技能目录
skills_provider = SkillsDirectoryProvider(
    Path("./skills"),
    watch=True,  # 监控文件变化
    reload_interval=5  # 每 5 秒检查一次
)

mcp.add_provider(skills_provider)
mcp.run()
```

### 技能权限控制

```python
from fastmcp import FastMCP
from fastmcp.providers.skills import SkillsDirectoryProvider
from pathlib import Path

mcp = FastMCP("Secure Skills")

# 创建带权限的技能提供者
skills_provider = SkillsDirectoryProvider(
    Path("./skills"),
    allowed_skills=["pdf-processing", "code-review"],  # 白名单
    denied_skills=["experimental"]  # 黑名单
)

mcp.add_provider(skills_provider)
mcp.run()
```

---

## 高级用法

### 自定义转换

```python
from fastmcp import FastMCP
from fastmcp.transforms import PrefixTransform

mcp = FastMCP("Transformed Server")

# 添加命名前缀
prefix_transform = PrefixTransform(prefix="myapp_")
mcp.add_transform(prefix_transform)

@mcp.tool()
def calculate():
    """计算工具"""
    pass

# 客户端看到的名称：myapp_calculate
```

### 错误处理

```python
from fastmcp import FastMCP

mcp = FastMCP("Error Handling")

@mcp.tool()
def risky_operation():
    """可能失败的操作"""
    try:
        # 尝试执行操作
        result = perform_operation()
        return {"status": "success", "data": result}
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "error_type": type(e).__name__
        }
```

### 中间件

```python
from fastmcp import FastMCP

mcp = FastMCP("Middleware Example")

@mcp.middleware()
async def logging_middleware(request, call_next):
    """日志记录中间件"""
    print(f"Before: {request.method} {request.path}")
    response = await call_next(request)
    print(f"After: {response.status_code}")
    return response

@mcp.tool()
def some_tool():
    """工具函数"""
    return "result"
```

### 上下文管理

```python
from fastmcp import FastMCP

mcp = FastMCP("Context Management")

@mcp.tool()
def context_aware_tool(context):
    """使用上下文的工具"""
    # 访问客户端信息
    client_id = context.client_id
    session_id = context.session_id

    # 访问共享状态
    user_data = context.state.get("user_data")

    return f"Hello from {client_id}"
```

---

## 最佳实践

### 1. 项目结构

推荐的 FastMCP 项目结构：

```
my-mcp-server/
├── src/
│   ├── __init__.py
│   ├── server.py          # MCP 服务器主文件
│   ├── tools/             # 工具模块
│   │   ├── __init__.py
│   │   ├── search.py
│   │   └── database.py
│   └── resources/         # 资源模块
│       ├── __init__.py
│       └── config.py
├── skills/                # 技能目录
│   ├── skill1/
│   └── skill2/
├── tests/                 # 测试
├── pyproject.toml         # 项目配置
└── README.md
```

### 2. 配置管理

```python
# config.py
from pydantic import BaseModel

class MCPServerConfig(BaseModel):
    """MCP 服务器配置"""
    server_name: str = "My MCP Server"
    log_level: str = "INFO"
    max_connections: int = 100

    class Config:
        env_prefix = "MCP_"

# server.py
from fastmcp import FastMCP
from .config import MCPServerConfig

config = MCPServerConfig()
mcp = FastMCP(config.server_name)
```

### 3. 类型注解

始终使用类型注解以提高代码可读性和 IDE 支持：

```python
from typing import List, Optional
from pydantic import BaseModel

class SearchResult(BaseModel):
    title: str
    url: str
    snippet: Optional[str] = None

@mcp.tool()
def search(query: str, max_results: int = 10) -> List[SearchResult]:
    """类型完整的搜索函数"""
    pass
```

### 4. 文档字符串

提供清晰的文档字符串：

```python
@mcp.tool()
def calculate_investment(
    principal: float,
    rate: float,
    years: int
) -> float:
    """Calculate investment return with compound interest.

    This function calculates the future value of an investment
    using compound interest formula.

    Args:
        principal: Initial investment amount (e.g., 1000.00)
        rate: Annual interest rate as percentage (e.g., 5.5 for 5.5%)
        years: Number of years to invest (must be positive integer)

    Returns:
        Future value of the investment

    Raises:
        ValueError: If principal is negative or years is not positive

    Example:
        >>> calculate_investment(1000, 5.5, 10)
        1708.14
    """
    if principal < 0:
        raise ValueError("Principal must be non-negative")
    if years <= 0:
        raise ValueError("Years must be positive")

    return principal * (1 + rate / 100) ** years
```

### 5. 错误处理

```python
from fastmcp import FastMCP
import logging

mcp = FastMCP("Production Server")
logger = logging.getLogger(__name__)

@mcp.tool()
def reliable_operation(input_data: str) -> dict:
    """可靠的操作，带完整错误处理"""
    try:
        # 输入验证
        if not input_data:
            return {
                "success": False,
                "error": "Input cannot be empty"
            }

        # 执行操作
        result = process_data(input_data)

        # 返回结果
        return {
            "success": True,
            "data": result
        }

    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return {
            "success": False,
            "error": f"Invalid input: {str(e)}"
        }
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return {
            "success": False,
            "error": "Internal server error"
        }
```

### 6. 测试

```python
# tests/test_tools.py
import pytest
from my_server import mcp

def test_add_tool():
    """测试加法工具"""
    result = mcp.call_tool("add", {"a": 2, "b": 3})
    assert result == 5

def test_add_with_invalid_input():
    """测试无效输入"""
    with pytest.raises(ValidationError):
        mcp.call_tool("add", {"a": "not a number", "b": 3})

@pytest.mark.asyncio
async def test_async_tool():
    """测试异步工具"""
    result = await mcp.call_tool_async("async_operation", {"task_id": "123"})
    assert "completed" in result
```

### 7. 性能优化

```python
from functools import lru_cache
import asyncio

@mcp.tool()
@lru_cache(maxsize=128)
def cached_lookup(identifier: str) -> dict:
    """带缓存的结果查找"""
    return expensive_lookup_operation(identifier)

@mcp.tool()
async def batch_operations(items: list) -> list:
    """批量并行操作"""
    tasks = [process_item(item) for item in items]
    return await asyncio.gather(*tasks)
```

### 8. 安全性

```python
from fastmcp import FastMCP
import secrets

mcp = FastMCP("Secure Server")

@mcp.tool()
def secure_api_call(endpoint: str, token: str) -> dict:
    """安全的 API 调用"""
    # 验证 token
    if not validate_token(token):
        raise PermissionError("Invalid token")

    # 清理输入
    clean_endpoint = sanitize_input(endpoint)

    # 调用 API
    return call_api(clean_endpoint)

def validate_token(token: str) -> bool:
    """验证令牌"""
    # 实现验证逻辑
    return True

def sanitize_input(input_str: str) -> str:
    """清理输入"""
    # 移除危险字符
    return input_str.replace(";", "").replace("--", "")
```

---

## 完整示例

### Azure Web Search MCP 服务器

这是项目中的实际实现示例：

```python
# bin/mcp_server.py
import sys
import os
from pathlib import Path
from fastmcp import FastMCP

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from azure_web_search.config import settings
from azure_web_search.web_search import AzureWebSearch
from azure_web_search.logger import setup_logger

# 创建 MCP 服务器
mcp = FastMCP("Azure Web Search")
logger = setup_logger(__name__)

# 初始化搜索服务
search_service = AzureWebSearch(
    api_key=settings.azure_openai_api_key,
    endpoint=settings.azure_openai_endpoint,
    model=settings.azure_openai_model
)

@mcp.tool()
def web_search(
    query: str,
    mode: str = "quick",
    num_results: int = 10,
    query_depth: int = 3
) -> str:
    """在网络上搜索信息并返回结果。

    这个工具使用 Azure OpenAI 的网络搜索功能来查找相关信息，
    支持两种搜索模式：快速和智能体。

    Args:
        query: 搜索查询字符串
        mode: 搜索模式 (quick/agentic)
        num_results: 返回结果数量 (1-50)
        query_depth: 查询深度 (1-5)

    Returns:
        JSON 格式的搜索结果字符串

    Raises:
        ValueError: 如果参数无效
        APIError: 如果 API 调用失败
    """
    try:
        results = search_service.search(
            query=query,
            mode=mode,
            num_results=num_results,
            query_depth=query_depth
        )
        return results.model_dump_json()
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise

@mcp.tool()
def web_search_structured(
    query: str,
    mode: str = "quick"
) -> dict:
    """执行结构化网络搜索。

    Args:
        query: 搜索查询
        mode: 搜索模式

    Returns:
        包含查询、响应和时间戳的字典
    """
    results = search_service.search(
        query=query,
        mode=mode,
        num_results=5
    )
    return {
        "query": query,
        "response": results.model_dump(),
        "timestamp": search_service.get_current_time()
    }

@mcp.tool()
def web_search_live_crawl(
    url: str,
    query: str = "summarize this page"
) -> str:
    """实时抓取并分析网页内容。

    Args:
        url: 要抓取的网页 URL
        query: 分析查询

    Returns:
        分析结果
    """
    results = search_service.search(
        query=query,
        mode="quick",
        num_results=1,
        url=url
    )
    return results.model_dump_json()

def main():
    """启动 MCP 服务器"""
    logger.info("Starting Azure Web Search MCP Server")
    mcp.run()

if __name__ == "__main__":
    main()
```

---

## 常见问题 (FAQ)

### Q1: FastMCP 和标准 MCP 有什么区别？

**A**: FastMCP 是 MCP 协议的 Python 实现。它提供了更简单的 API 和更好的开发体验，但完全兼容 MCP 协议规范。

### Q2: 如何调试 MCP 服务器？

**A**:
1. 使用日志记录：`mcp = FastMCP("Server", log_level="DEBUG")`
2. 使用测试客户端：`python test_mcp_server.py`
3. 启用详细输出：`mcp.run(verbose=True)`

### Q3: Skills Provider 支持哪些文件格式？

**A**:
- 必需：`SKILL.md` (主指令文件)
- 支持：Markdown, PDF, 文本文件, 图片, JSON
- 任何可以被 MCP 作为资源暴露的文件

### Q4: 如何在 Claude Desktop 中使用自定义 MCP 服务器？

**A**: 编辑 Claude Desktop 配置文件：

```json
{
  "mcpServers": {
    "my-server": {
      "command": "uv",
      "args": ["--directory", "/path/to/project", "run", "python", "bin/mcp_server.py"],
      "env": {
        "PYTHONPATH": "/path/to/project"
      }
    }
  }
}
```

### Q5: 如何处理大文件上传？

**A**: 使用流式处理：

```python
@mcp.tool()
async def process_large_file(file_path: str) -> str:
    """处理大文件"""
    chunk_size = 1024 * 1024  # 1MB
    results = []

    with open(file_path, 'r') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            result = await process_chunk(chunk)
            results.append(result)

    return merge_results(results)
```

---

## 资源链接

- **官方文档**: https://gofastmcp.com
- **GitHub 仓库**: https://github.com/jlowin/fastmcp
- **MCP 协议规范**: https://modelcontextprotocol.io
- **社区论坛**: https://discord.gg/fastmcp

---

**文档版本**: 1.0.0
**最后更新**: 2026-01-29
**维护者**: Azure Web Search Team
