"""按地理位置搜索示例"""

import sys
from pathlib import Path

# 添加 src 目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from rich.console import Console
from rich.panel import Panel

from src.config import get_settings, setup_env_file
from src.logger import setup_logger
from src.web_search import AzureWebSearch

console = Console()


def main():
    """地理位置搜索示例"""
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

    # 不同地区的搜索对比
    query = "今天有什么好消息"
    countries = [
        ("US", "美国"),
        ("CN", "中国"),
        ("JP", "日本"),
    ]

    for country_code, country_name in countries:
        console.print(Panel(f"[cyan]🌍 地区：{country_name} ({country_code})[/cyan]"))
        console.print(f"[cyan]🔍 搜索：{query}[/cyan]\n")

        try:
            result = search_client.quick_search(query, country=country_code)

            # 显示结果
            console.print(Panel(
                result.text[:500] + "..." if len(result.text) > 500 else result.text,
                title=f"{country_name}的搜索结果",
                border_style="green"
            ))

            # 显示来源数量
            console.print(f"[yellow]📚 引用来源：{len(result.citations)} 个[/yellow]\n")
            console.print("-" * 80 + "\n")

        except Exception as e:
            console.print(f"[red]❌ 搜索失败：{e}[/red]\n")


if __name__ == "__main__":
    main()
