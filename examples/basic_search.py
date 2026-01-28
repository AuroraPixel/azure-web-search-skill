"""基础搜索示例"""

import sys
from pathlib import Path

# 添加 src 目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from src.config import get_settings, setup_env_file
from src.logger import setup_logger
from src.web_search import AzureWebSearch

console = Console()


def main():
    """基础搜索示例"""
    # 检查环境文件
    if not setup_env_file():
        return

    # 加载配置
    try:
        settings = get_settings()
    except Exception as e:
        console.print(f"[red]❌ 配置加载失败：{e}[/red]")
        return

    # 设置日志
    setup_logger(level=settings.log_level)

    # 创建搜索客户端
    search_client = AzureWebSearch(settings)

    # 执行快速搜索
    query = "2026年人工智能最新发展趋势"
    console.print(Panel(f"[cyan]🔍 搜索查询：{query}[/cyan]"))

    try:
        result = search_client.quick_search(query)

        # 显示结果
        console.print("\n[green]✅ 搜索结果：[/green]\n")
        console.print(Panel(result.text, title="回答内容", border_style="green"))

        # 显示引用源
        if result.citations:
            console.print(f"\n[yellow]📚 引用来源（{len(result.citations)} 个）：[/yellow]\n")
            for i, citation in enumerate(result.citations, 1):
                console.print(f"{i}. [{citation.title or '未知标题'}]({citation.url})")

        # 显示唯一源
        sources = result.get_unique_sources()
        if sources:
            console.print(f"\n[blue]🌐 唯一数据源（{len(sources)} 个）：[/blue]\n")
            for i, source in enumerate(sources, 1):
                console.print(f"{i}. {source['title']}")
                console.print(f"   {source['url']}\n")

    except Exception as e:
        console.print(f"[red]❌ 搜索失败：{e}[/red]")


if __name__ == "__main__":
    main()
