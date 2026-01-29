"""基于 FastMCP 的 Azure OpenAI Web Search MCP Server

这个 MCP 服务器使用 FastMCP 框架构建，提供三种网络搜索模式：
1. 快速搜索 (quick) - 无推理，快速返回结果
2. 智能体搜索 (agentic) - 带推理，适合复杂查询
3. 深度研究 (deep_research) - 深度分析，适合学术研究

此外，还支持 Skills Provider，可以将 AI 技能作为 MCP 资源暴露。
"""

import sys
import os
import json
from pathlib import Path
from typing import Optional

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from fastmcp import FastMCP
except ImportError:
    print("错误：请先安装 fastmcp 包", file=sys.stderr)
    print("运行: uv pip install fastmcp", file=sys.stderr)
    sys.exit(1)

from src.config import get_settings
from src.web_search import AzureWebSearch
from src.logger import get_logger

logger = get_logger(__name__)

# 创建 FastMCP 服务器实例
mcp = FastMCP("Azure Web Search")

# 全局搜索客户端
search_client: Optional[AzureWebSearch] = None


def init_search_client():
    """初始化搜索客户端"""
    global search_client
    if search_client is None:
        try:
            settings = get_settings()
            search_client = AzureWebSearch(settings)
            logger.info("✅ Web Search 客户端初始化成功")
        except Exception as e:
            logger.error(f"❌ 初始化失败：{e}")
            raise


# ============================================================================
# 工具定义 (Tools)
# ============================================================================

@mcp.tool()
def web_search_quick(
    query: str,
    country: Optional[str] = None
) -> str:
    """执行快速网络搜索（无推理）。

    这是最高效的搜索模式，适用于需要快速获取最新信息的场景。

    适用场景：
    - 快速查询时效性信息（如新闻、最新数据）
    - 简单的事实查询（如定义、公式）
    - 获取单一来源的明确答案
    - 不需要复杂推理的查询

    Args:
        query: 搜索查询字符串（必需）
        country: 国家代码（可选），如 US、CN、JP 等，使用 ISO 3166-1 alpha-2 标准

    Returns:
        JSON 格式的搜索结果，包含：
        - text: 搜索结果文本
        - statistics: 统计信息（引用数、搜索调用数、唯一来源数）
        - sources: 前 10 个唯一来源列表

    Raises:
        ValueError: 如果 query 参数为空
        APIError: 如果 API 调用失败

    Example:
        >>> result = web_search_quick("Python 3.12 新特性")
        >>> data = json.loads(result)
        >>> print(data["text"])
    """
    init_search_client()

    if not query:
        raise ValueError("query 参数是必需的")

    logger.info(f"🔍 执行快速搜索：{query}")

    try:
        result = search_client.quick_search(query, country=country)

        # 提取唯一来源
        sources = result.get_unique_sources()

        # 格式化输出
        output = {
            "text": result.text,
            "statistics": {
                "citations": len(result.citations),
                "search_calls": len(result.search_calls),
                "unique_sources": len(sources)
            },
            "sources": sources[:10]  # 只返回前 10 个来源
        }

        logger.info(f"✅ 快速搜索完成，找到 {len(result.citations)} 个引用")

        return json.dumps(output, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"❌ 快速搜索失败：{e}")
        raise


@mcp.tool()
def web_search_agentic(
    query: str,
    country: Optional[str] = None
) -> str:
    """执行智能体搜索（带推理）。

    此模式使用 AI 推理来分析和综合搜索结果，适合复杂查询。

    适用场景：
    - 需要多步推理的复杂问题
    - 需要综合分析多个来源的信息
    - 需要理解上下文的模糊查询
    - 需要比较和对比不同观点

    Args:
        query: 搜索查询字符串（必需）
        country: 国家代码（可选），如 US、CN、JP 等，使用 ISO 3166-1 alpha-2 标准

    Returns:
        JSON 格式的搜索结果，包含：
        - text: 经过推理分析的搜索结果
        - statistics: 统计信息
        - sources: 来源列表

    Raises:
        ValueError: 如果 query 参数为空
        APIError: 如果 API 调用失败

    Note:
        此模式比快速搜索慢，但提供更深入的分析和综合。

    Example:
        >>> result = web_search_agentic("比较不同编程语言的性能")
        >>> data = json.loads(result)
        >>> print(data["text"])  # 包含推理和对比分析
    """
    init_search_client()

    if not query:
        raise ValueError("query 参数是必需的")

    logger.info(f"🧠 执行智能体搜索：{query}")

    try:
        result = search_client.agentic_search(query, country=country)

        # 提取唯一来源
        sources = result.get_unique_sources()

        # 格式化输出
        output = {
            "text": result.text,
            "statistics": {
                "citations": len(result.citations),
                "search_calls": len(result.search_calls),
                "unique_sources": len(sources)
            },
            "sources": sources[:10]
        }

        logger.info(f"✅ 智能体搜索完成，找到 {len(result.citations)} 个引用")

        return json.dumps(output, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"❌ 智能体搜索失败：{e}")
        raise


# ============================================================================
# 资源定义 (Resources)
# ============================================================================

@mcp.resource("config://server")
def get_server_config() -> str:
    """获取 MCP 服务器配置信息。

    Returns:
        JSON 格式的服务器配置

    Example:
        >>> config = get_server_config()
        >>> data = json.loads(config)
        >>> print(data["server_name"])
    """
    settings = get_settings()

    config = {
        "server_name": "Azure Web Search MCP Server",
        "version": "2.0.0",
        "framework": "FastMCP",
        "azure_endpoint": settings.azure_openai_endpoint,
        "azure_model": settings.azure_openai_model,
        "capabilities": {
            "tools": [
                "web_search_quick",
                "web_search_agentic"
            ],
            "resources": [
                "config://server",
                "search://modes"
            ]
        }
    }

    return json.dumps(config, ensure_ascii=False, indent=2)


@mcp.resource("search://modes")
def get_search_modes() -> str:
    """获取支持的搜索模式说明。

    Returns:
        JSON 格式的搜索模式文档

    Example:
        >>> modes = get_search_modes()
        >>> data = json.loads(modes)
        >>> for mode in data["modes"]:
        ...     print(f"{mode['name']}: {mode['description']}")
    """
    modes = {
        "modes": [
            {
                "name": "quick",
                "tool": "web_search_quick",
                "description": "快速搜索，无推理",
                "use_cases": [
                    "快速查询时效性信息",
                    "简单的事实查询",
                    "获取最新新闻或数据"
                ],
                "speed": "快速",
                "reasoning": false
            },
            {
                "name": "agentic",
                "tool": "web_search_agentic",
                "description": "智能体搜索，带推理",
                "use_cases": [
                    "复杂查询需要多步推理",
                    "需要综合分析多个来源",
                    "需要理解上下文的搜索"
                ],
                "speed": "中等",
                "reasoning": true
            }
        ]
    }

    return json.dumps(modes, ensure_ascii=False, indent=2)


# ============================================================================
# 提示定义 (Prompts)
# ============================================================================

@mcp.prompt()
def research_assistant(topic: str) -> str:
    """生成研究助手提示模板。

    Args:
        topic: 研究主题

    Returns:
        格式化的研究提示

    Example:
        >>> prompt = research_assistant("人工智能在医疗领域的应用")
        >>> print(prompt)
    """
    return f"""你是一个专业的研究助手。请使用网络搜索工具深入研究以下主题：

**研究主题**: {topic}

**研究步骤**:
1. 使用 `web_search_quick` 快速了解主题概况
2. 使用 `web_search_agentic` 深入分析关键方面

**输出要求**:
- 提供全面的研究报告
- 包含权威来源引用
- 分析不同观点和证据
- 标注信息时效性

请开始研究。"""

@mcp.prompt()
def news_analyzer(topic: str) -> str:
    """生成新闻分析提示模板。

    Args:
        topic: 新闻主题

    Returns:
        格式化的新闻分析提示

    Example:
        >>> prompt = news_analyzer("2026年人工智能发展趋势")
        >>> print(prompt)
    """
    return f"""你是一个新闻分析专家。请搜索并分析关于"{topic}"的最新报道。

**分析步骤**:
1. 使用 `web_search_quick` 获取最新新闻
2. 识别主要事件和趋势
3. 分析不同来源的报道角度
4. 总结关键发现和影响

**输出格式**:
- 📰 标题
- 📅 发布时间
- 📝 核心内容
- 🔗 来源链接
- 💭 分析评论

请开始分析。"""


# ============================================================================
# Skills Provider 支持
# ============================================================================

def setup_skills_provider():
    """设置 Skills Provider（可选）。

    如果项目包含 skills/ 目录，自动将其作为 MCP 资源暴露。
    """
    skills_dir = project_root / "skills"

    if skills_dir.exists():
        try:
            from fastmcp.providers.skills import SkillsDirectoryProvider

            # 添加技能目录提供者
            mcp.add_provider(SkillsDirectoryProvider(skills_dir))

            logger.info(f"✅ Skills Provider 已启用，技能目录: {skills_dir}")

            # 列出发现的技能
            skills = [d for d in skills_dir.iterdir() if d.is_dir() and (d / "SKILL.md").exists()]
            if skills:
                logger.info(f"📁 发现 {len(skills)} 个技能:")
                for skill in skills:
                    logger.info(f"   - {skill.name}")

        except ImportError:
            logger.warning("⚠️  FastMCP Skills Provider 不可用，请升级到最新版本")
        except Exception as e:
            logger.error(f"❌ Skills Provider 初始化失败: {e}")


# ============================================================================
# 主函数
# ============================================================================

def main():
    """启动 MCP 服务器"""
    logger.info("🚀 启动 Azure Web Search MCP Server (基于 FastMCP)")

    # 预先初始化客户端
    try:
        init_search_client()
    except Exception as e:
        logger.error(f"❌ 初始化失败：{e}")
        logger.error("请确保 .env 文件已正确配置")
        sys.exit(1)

    # 设置 Skills Provider
    setup_skills_provider()

    # 运行服务器
    logger.info("🎯 MCP 服务器已启动，等待连接...")
    mcp.run()


if __name__ == "__main__":
    main()
