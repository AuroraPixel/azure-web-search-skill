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
import time
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
from src.logger import get_logger, setup_logger

logger = get_logger()

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
            logger.info("[INIT] Web Search client initialized")
        except Exception as e:
            logger.error(f"[INIT] Failed to initialize Web Search client: {e}")
            raise


def _summarize_text(text: str, max_chars: int = 200) -> str:
    """返回单行摘要，避免日志刷屏。"""
    if not text:
        return ""
    one_line = " ".join(text.split())
    if len(one_line) <= max_chars:
        return one_line
    return one_line[: max_chars - 1] + "…"


def _extract_usage(raw_response: object) -> Optional[dict]:
    """尽量从 OpenAI Responses 返回里提取 token 用量。"""
    if not isinstance(raw_response, dict):
        return None

    def _normalize(u: dict) -> dict:
        # 兼容多种字段命名（不同 SDK/代理层）
        input_tokens = (
            u.get("input_tokens")
            or u.get("prompt_tokens")
            or u.get("inputTokens")
            or u.get("promptTokens")
        )
        output_tokens = (
            u.get("output_tokens")
            or u.get("completion_tokens")
            or u.get("outputTokens")
            or u.get("completionTokens")
        )
        total_tokens = (
            u.get("total_tokens")
            or u.get("totalTokens")
            or (input_tokens + output_tokens if isinstance(input_tokens, int) and isinstance(output_tokens, int) else None)
        )

        normalized = dict(u)
        if input_tokens is not None:
            normalized["input_tokens"] = input_tokens
        if output_tokens is not None:
            normalized["output_tokens"] = output_tokens
        if total_tokens is not None:
            normalized["total_tokens"] = total_tokens
        return normalized

    usage = raw_response.get("usage")
    if isinstance(usage, dict) and usage:
        return _normalize(usage)

    # 兼容某些 SDK/代理层包装
    resp = raw_response.get("response")
    if isinstance(resp, dict):
        usage = resp.get("usage")
        if isinstance(usage, dict) and usage:
            return _normalize(usage)

    # 再尝试一些常见包装字段
    usage = raw_response.get("token_usage") or raw_response.get("tokenUsage") or raw_response.get("usage_stats")
    if isinstance(usage, dict) and usage:
        return _normalize(usage)

    return None


# ============================================================================
# 工具定义 (Tools)
# ============================================================================

@mcp.tool(
    name="azure_web_search",
    description=(
        "Search the web via Azure OpenAI Web Search.\n"
        "Args: query (required), mode: quick|agentic (default: quick), country: ISO 3166-1 alpha-2.\n"
        "Returns: JSON string with text, sources, statistics, and optional token usage."
    ),
)
def azure_web_search(
    query: str,
    mode: str = "quick",
    country: Optional[str] = None,
) -> str:
    """Azure OpenAI Web Search (single entrypoint).

    Parameters:
        query: Search query (required).
        mode: "quick" (fast, no reasoning) or "agentic" (slower, with analysis). Default: "quick".
        country: Optional ISO 3166-1 alpha-2 country code (e.g. "US", "CN", "JP").

    Returns:
        A JSON string:
        - meta: { tool, mode, query, country, elapsed_ms }
        - text: result text
        - statistics: { citations, search_calls, unique_sources }
        - sources: top 10 unique sources
        - usage: best-effort token usage (if available)
    """
    init_search_client()

    if not query:
        raise ValueError("query is required")

    mode = (mode or "").strip().lower()
    if mode not in {"quick", "agentic"}:
        raise ValueError("mode must be 'quick' or 'agentic'")

    t0 = time.perf_counter()
    logger.info(f"[CALL] tool=azure_web_search mode={mode} country={country or '-'} query={query!r}")

    try:
        if mode == "quick":
            result = search_client.quick_search(query, country=country)
        else:
            result = search_client.agentic_search(query, country=country)

        sources = result.get_unique_sources()
        usage = _extract_usage(result.raw_response)
        elapsed_ms = int((time.perf_counter() - t0) * 1000)

        output = {
            "meta": {
                "tool": "azure_web_search",
                "mode": mode,
                "query": query,
                "country": country,
                "elapsed_ms": elapsed_ms,
            },
            "text": result.text,
            "statistics": {
                "citations": len(result.citations),
                "search_calls": len(result.search_calls),
                "unique_sources": len(sources),
            },
            "usage": usage,
            "sources": sources[:10],
        }

        preview = _summarize_text(result.text)
        logger.info(
            "[OK] tool=azure_web_search mode=%s elapsed_ms=%s citations=%s unique_sources=%s preview=%r",
            mode,
            elapsed_ms,
            len(result.citations),
            len(sources),
            preview,
        )
        if usage:
            logger.info("[TOKENS] %s", usage)

        return json.dumps(output, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"[ERR] azure_web_search failed: {e}")
        raise


# ============================================================================
# Resources
# ============================================================================

@mcp.resource(
    "config://server",
    description="Server metadata and capabilities as JSON.",
)
def get_server_config() -> str:
    """Return MCP server metadata as JSON."""
    settings = get_settings()

    config = {
        "server_name": "Azure Web Search MCP Server",
        "version": "2.0.0",
        "framework": "FastMCP",
        "azure_endpoint": settings.azure_openai_endpoint,
        "azure_model": settings.azure_openai_model,
        "capabilities": {
            "tools": [
                "azure_web_search"
            ],
            "resources": [
                "config://server",
                "search://modes"
            ]
        }
    }

    return json.dumps(config, ensure_ascii=False, indent=2)


@mcp.resource(
    "search://modes",
    description="Supported search modes and when to use them.",
)
def get_search_modes() -> str:
    """Return supported search modes as JSON."""
    modes = {
        "modes": [
            {
                "name": "quick",
                "tool": "azure_web_search",
                "description": "Fast search (no reasoning).",
                "use_cases": [
                    "time-sensitive lookups (news, latest data)",
                    "simple factual questions",
                    "quick source gathering"
                ],
                "speed": "fast",
                "reasoning": False
            },
            {
                "name": "agentic",
                "tool": "azure_web_search",
                "description": "Search with analysis (slower).",
                "use_cases": [
                    "complex questions requiring synthesis",
                    "compare multiple sources/viewpoints",
                    "context-dependent queries"
                ],
                "speed": "medium",
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
    """Generate a research prompt template.

    Args:
        topic: Research topic.

    Returns:
        A formatted prompt string.
    """
    return f"""You are a professional research assistant. Research the topic below using web search.

Topic: {topic}

Steps:
1. Use `azure_web_search` (mode=quick) to gather an overview and key facts.
2. Use `azure_web_search` (mode=agentic) to synthesize, compare sources, and draw conclusions.

Output requirements:
- A concise, structured report
- Cite reputable sources with links
- Highlight differing viewpoints and evidence
- Note freshness/recency of key information
"""

@mcp.prompt()
def news_analyzer(topic: str) -> str:
    """Generate a news analysis prompt template.

    Args:
        topic: News topic.

    Returns:
        A formatted prompt string.
    """
    return f"""You are a news analyst. Find and analyze the latest coverage about: {topic}

Steps:
1. Use `azure_web_search` (mode=quick) to collect the latest reports.
2. Identify key events, timeline, and emerging trends.
3. Compare angles and claims across sources.
4. Summarize key takeaways and likely impact.

Output format:
- Title
- Published time (if available)
- Key facts (separate facts vs opinions)
- Source links
- Your analysis (brief and evidence-based)
"""


# ============================================================================
# Skills Provider 支持
# ============================================================================

def setup_skills_provider():
    """Set up Skills Provider (optional).

    If `skills/` exists, expose skills as MCP resources.
    """
    global _skills_resources_registered
    skills_dir = project_root / "skills"

    def _register_fallback_resources() -> None:
        """Fallback resources for skills (explicit UTF-8 reads)."""
        global _skills_resources_registered

        if _skills_resources_registered:
            return

        skills = [d for d in skills_dir.iterdir() if d.is_dir() and (d / "SKILL.md").exists()]

        @mcp.resource(
            "skills://list",
            description="List available skills discovered under skills/*/SKILL.md.",
        )
        def list_skills() -> str:
            """List available skills (JSON)."""
            data = {
                "count": len(skills),
                "skills": [d.name for d in skills],
            }
            return json.dumps(data, ensure_ascii=False, indent=2)

        @mcp.resource(
            "skill://{skill_name}/SKILL.md",
            description="Return SKILL.md content for the given skill (UTF-8).",
        )
        def get_skill_md(skill_name: str) -> str:
            """Return a skill's SKILL.md (UTF-8)."""
            skill_path = skills_dir / skill_name / "SKILL.md"
            if not skill_path.exists():
                raise FileNotFoundError(f"Skill not found: {skill_name}")
            return skill_path.read_text(encoding="utf-8")

        @mcp.resource(
            "skill://{skill_name}/_manifest",
            description="Return a minimal skill manifest for the given skill (JSON).",
        )
        def get_skill_manifest(skill_name: str) -> str:
            """Return a minimal skill manifest (JSON)."""
            skill_path = skills_dir / skill_name / "SKILL.md"
            if not skill_path.exists():
                raise FileNotFoundError(f"Skill not found: {skill_name}")
            data = {
                "name": skill_name,
                "files": ["SKILL.md"],
                "entry": "SKILL.md",
            }
            return json.dumps(data, ensure_ascii=False, indent=2)

        _skills_resources_registered = True
        logger.info(
            "[INFO] Skills fallback enabled. Use `skills://list` and `skill://<name>/SKILL.md`."
        )
        if skills:
            logger.info(f"[INFO] Found {len(skills)} skills: " + ", ".join(d.name for d in skills))
        else:
            logger.info("[INFO] No skills found under skills/*/SKILL.md")

    if skills_dir.exists():
        # If Python is not running in UTF-8 mode (common on Windows: cp936/gbk),
        # SkillsDirectoryProvider may read SKILL.md using the system default encoding.
        # In that case, use the UTF-8 fallback to avoid decode errors.
        try:
            import locale

            preferred = (locale.getpreferredencoding(False) or "").lower().replace("_", "-")
            if getattr(sys.flags, "utf8_mode", 0) != 1 and preferred not in {"utf-8", "utf8"}:
                logger.info(
                    "[INFO] Default encoding=%s and UTF-8 mode is off; using the UTF-8 skills fallback. "
                    "To force SkillsDirectoryProvider, set PYTHONUTF8=1 or start with `python -X utf8 ...`.",
                    preferred,
                )
                _register_fallback_resources()
                return
        except Exception:
            # If detection fails, fall back to the normal path.
            pass

        try:
            # FastMCP 3.x: https://gofastmcp.com/servers/providers/skills
            from fastmcp.server.providers.skills import SkillsDirectoryProvider  # type: ignore

            mcp.add_provider(SkillsDirectoryProvider(roots=skills_dir))
            logger.info(f"[OK] Skills Provider 已启用（SkillsDirectoryProvider），技能目录: {skills_dir}")

        except UnicodeDecodeError as e:
            # Windows 默认编码（gbk）下，skills 里有 emoji 等字符时可能触发
            logger.warning(f"[WARN] Skills Provider 读取技能文件失败（编码问题）：{e}")
            logger.warning("[HINT] 建议使用 UTF-8 模式启动：设置 PYTHONUTF8=1 或运行 `python -X utf8 -m bin.mcp_server`")
            _register_fallback_resources()

        except ImportError:
            # 兼容：旧版 fastmcp 或缺少 skills provider 时，用内置资源模拟 Skills Provider
            _register_fallback_resources()
        except Exception as e:
            logger.error(f"[ERR] Skills Provider 初始化失败: {e}")


# ============================================================================
# 主函数
# ============================================================================

def main():
    """启动 MCP 服务器（stdio / streamable-http / sse）"""
    settings = get_settings()
    # 确保业务日志有 handler（否则只有 uvicorn/fastmcp 的日志）
    global logger
    setup_logger(level=settings.log_level)
    logger = get_logger()

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
