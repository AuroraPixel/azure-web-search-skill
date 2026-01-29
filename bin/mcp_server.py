"""基于 FastMCP 的 Azure OpenAI Web Search MCP Server

这个 MCP 服务器使用 FastMCP 框架构建，提供两种网络搜索模式：
1. 快速搜索 (quick) - 无推理，快速返回结果
2. 智能体搜索 (agentic) - 带推理，适合复杂查询

此外，还支持 Skills Provider，可以将 AI 技能作为 MCP 资源暴露。
"""

import sys
import os
import json
import argparse
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
_skills_resources_registered: bool = False


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
                "reasoning": False
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
                "reasoning": True
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
    global _skills_resources_registered
    skills_dir = project_root / "skills"

    def _register_fallback_resources() -> None:
        """内置 fallback：用资源暴露 skills/*/SKILL.md（UTF-8 读取）。"""
        global _skills_resources_registered

        if _skills_resources_registered:
            return

        skills = [d for d in skills_dir.iterdir() if d.is_dir() and (d / "SKILL.md").exists()]

        @mcp.resource("skills://list")
        def list_skills() -> str:
            """列出可用技能（来自 skills/*/SKILL.md）。"""
            data = {
                "count": len(skills),
                "skills": [d.name for d in skills],
            }
            return json.dumps(data, ensure_ascii=False, indent=2)

        @mcp.resource("skill://{skill_name}")
        def get_skill(skill_name: str) -> str:
            """读取指定技能的 SKILL.md 内容。"""
            skill_path = skills_dir / skill_name / "SKILL.md"
            if not skill_path.exists():
                raise FileNotFoundError(f"未找到技能：{skill_name}")
            return skill_path.read_text(encoding="utf-8")

        _skills_resources_registered = True
        logger.info(
            "ℹ️  已启用内置 skills fallback：使用 `skills://list` 查看技能列表，用 `skill://<name>` 获取 SKILL.md"
        )
        if skills:
            logger.info(f"📁 发现 {len(skills)} 个技能: " + ", ".join(d.name for d in skills))
        else:
            logger.info("📁 未发现任何技能（缺少 skills/*/SKILL.md）")

    if skills_dir.exists():
        try:
            # FastMCP 3.x: https://gofastmcp.com/servers/providers/skills
            from fastmcp.server.providers.skills import SkillsDirectoryProvider  # type: ignore

            mcp.add_provider(SkillsDirectoryProvider(roots=skills_dir))
            logger.info(f"✅ Skills Provider 已启用（SkillsDirectoryProvider），技能目录: {skills_dir}")

        except UnicodeDecodeError as e:
            # Windows 默认编码（gbk）下，skills 里有 emoji 等字符时可能触发
            logger.warning(f"⚠️  Skills Provider 读取技能文件失败（编码问题）：{e}")
            logger.warning("💡 建议使用 UTF-8 模式启动：设置 PYTHONUTF8=1 或运行 `python -X utf8 -m bin.mcp_server`")
            _register_fallback_resources()

        except ImportError:
            # 兼容：旧版 fastmcp 或缺少 skills provider 时，用内置资源模拟 Skills Provider
            _register_fallback_resources()
        except Exception as e:
            logger.error(f"❌ Skills Provider 初始化失败: {e}")


# ============================================================================
# 主函数
# ============================================================================

def main():
    """启动 MCP 服务器（stdio / streamable-http / sse）"""
    settings = get_settings()

    parser = argparse.ArgumentParser(description="Azure Web Search MCP Server (FastMCP)")
    parser.add_argument(
        "--transport",
        default=settings.mcp_transport,
        choices=["stdio", "streamable-http", "sse"],
        help="传输协议：stdio / streamable-http / sse（默认来自 MCP_TRANSPORT）",
    )
    parser.add_argument("--host", default=settings.mcp_host, help="HTTP 绑定地址（仅 HTTP/SSE）")
    parser.add_argument("--port", type=int, default=settings.mcp_port, help="HTTP 端口（仅 HTTP/SSE）")
    parser.add_argument("--path", default="/mcp", help="HTTP 路径（仅 HTTP/SSE，默认：/mcp）")
    parser.add_argument("--no-banner", action="store_true", help="不显示 FastMCP 启动横幅")
    args = parser.parse_args()

    # 预先初始化客户端
    try:
        init_search_client()
    except Exception as e:
        logger.error(f"❌ 初始化失败：{e}")
        logger.error("请确保 .env 文件已正确配置")
        sys.exit(1)

    # 设置 Skills Provider
    setup_skills_provider()

    show_banner = not args.no_banner
    path = args.path if args.path.startswith("/") else f"/{args.path}"

    try:
        if args.transport == "stdio":
            logger.info("🚀 启动 Azure Web Search MCP Server (STDIO)")
            logger.info("🎯 MCP STDIO 服务器正在启动...")
            mcp.run(transport="stdio", show_banner=show_banner)
        else:
            logger.info(f"🚀 启动 Azure Web Search MCP Server ({args.transport})")
            logger.info(f"📡 服务器地址: http://{args.host}:{args.port}{path}")
            logger.info("🎯 MCP HTTP 服务器正在启动...")
            mcp.run(
                transport=args.transport,
                show_banner=show_banner,
                host=args.host,
                port=args.port,
                path=path,
            )
    except OSError as e:
        logger.error(f"❌ 启动失败：{e}")
        logger.error("💡 端口可能被占用，可尝试：--port 8001")
        raise


if __name__ == "__main__":
    main()
