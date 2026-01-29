"""MCP Server for Azure OpenAI Web Search"""

import os
import sys
import json
import asyncio
from typing import Any, Optional

# 添加 src 目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
except ImportError:
    print("错误：请先安装 mcp 包", file=sys.stderr)
    print("运行: uv pip install mcp", file=sys.stderr)
    sys.exit(1)

from src.config import get_settings
from src.web_search import AzureWebSearch
from src.models import SearchMode
from src.logger import get_logger

logger = get_logger(__name__)

# 初始化服务器
app = Server("azure-web-search")

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


@app.list_tools()
async def list_tools() -> list[Tool]:
    """列出所有可用的工具"""
    return [
        Tool(
            name="web_search_quick",
            description="""执行快速网络搜索（无推理）。
            
适用场景：
- 快速查询时效性信息
- 获取最新新闻或数据
- 简单的事实查询
            
参数：
- query: 搜索查询字符串（必需）
- country: 国家代码（可选），如 US、CN、JP 等，使用 ISO 3166-1 alpha-2 标准
            
返回：搜索结果文本、引用来源列表和统计信息""",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "要搜索的查询内容"
                    },
                    "country": {
                        "type": "string",
                        "description": "国家代码（可选），如 US、CN、JP 等",
                        "pattern": "^[A-Z]{2}$"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="web_search_agentic",
            description="""执行智能体搜索（带推理）。
            
适用场景：
- 复杂查询需要多步推理
- 需要综合分析多个来源
- 需要理解上下文的搜索
            
参数：
- query: 搜索查询字符串（必需）
- country: 国家代码（可选），如 US、CN、JP 等，使用 ISO 3166-1 alpha-2 标准
            
返回：经过推理分析的搜索结果、引用来源列表和统计信息
            
注意：此模式比快速搜索慢，但结果更深入""",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "要搜索的查询内容"
                    },
                    "country": {
                        "type": "string",
                        "description": "国家代码（可选），如 US、CN、JP 等",
                        "pattern": "^[A-Z]{2}$"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="web_search_deep",
            description="""执行深度研究搜索。
            
适用场景：
- 学术研究和深度调查
- 需要全面分析的主题
- 多角度综合研究
            
参数：
- query: 研究主题（必需）
- country: 国家代码（可选），如 US、CN、JP 等，使用 ISO 3166-1 alpha-2 标准
- include_code_interpreter: 是否包含代码解释器工具（可选，默认 false）
            
返回：深度研究报告、多个来源的引用和详细分析
            
注意：此模式最慢但最深入，可能需要数分钟，需要 o3-deep-research 模型""",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "要研究的主题"
                    },
                    "country": {
                        "type": "string",
                        "description": "国家代码（可选），如 US、CN、JP 等",
                        "pattern": "^[A-Z]{2}$"
                    },
                    "include_code_interpreter": {
                        "type": "boolean",
                        "description": "是否包含代码解释器工具",
                        "default": False
                    }
                },
                "required": ["query"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """调用工具"""
    try:
        # 确保客户端已初始化
        init_search_client()
        
        if search_client is None:
            raise ValueError("搜索客户端未初始化")
        
        # 获取参数
        query = arguments.get("query")
        country = arguments.get("country")
        
        if not query:
            raise ValueError("query 参数是必需的")
        
        # 执行搜索
        result = None
        
        if name == "web_search_quick":
            logger.info(f"🔍 执行快速搜索：{query}")
            result = search_client.quick_search(query, country=country)
            
        elif name == "web_search_agentic":
            logger.info(f"🧠 执行智能体搜索：{query}")
            result = search_client.agentic_search(query, country=country)
            
        elif name == "web_search_deep":
            logger.info(f"📚 执行深度研究：{query}")
            include_code = arguments.get("include_code_interpreter", False)
            result = search_client.deep_research(
                query, 
                country=country,
                include_code_interpreter=include_code
            )
        else:
            raise ValueError(f"未知的工具：{name}")
        
        # 格式化结果
        sources = result.get_unique_sources()
        
        output = {
            "text": result.text,
            "statistics": {
                "citations": len(result.citations),
                "search_calls": len(result.search_calls),
                "unique_sources": len(sources)
            },
            "sources": sources[:10]  # 只返回前 10 个来源
        }
        
        logger.info(f"✅ 搜索完成，找到 {len(result.citations)} 个引用")
        
        return [
            TextContent(
                type="text",
                text=json.dumps(output, ensure_ascii=False, indent=2)
            )
        ]
        
    except Exception as e:
        logger.error(f"❌ 工具调用失败：{e}")
        error_output = {
            "error": str(e),
            "tool": name,
            "arguments": arguments
        }
        return [
            TextContent(
                type="text",
                text=json.dumps(error_output, ensure_ascii=False, indent=2)
            )
        ]


async def main():
    """主函数"""
    logger.info("🚀 启动 Azure Web Search MCP Server")
    
    # 预先初始化客户端
    try:
        init_search_client()
    except Exception as e:
        logger.error(f"❌ 初始化失败：{e}")
        logger.error("请确保 .env 文件已正确配置")
        sys.exit(1)
    
    # 运行服务器
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
