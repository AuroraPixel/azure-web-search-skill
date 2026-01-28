"""所有搜索模式对比示例"""

import sys
from pathlib import Path

# 添加 src 目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from rich.console import Console
from rich.panel import Panel

from src.config import get_settings, setup_env_file
from src.logger import setup_logger
from src.models import SearchMode
from src.web_search import AzureWebSearch

console = Console()


def main():
    """演示所有搜索模式"""
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

    query = "什么是量子计算？它有什么实际应用？"

    # 1. 快速搜索模式
    console.print("\n" + "=" * 80)
    console.print(Panel(
        "[cyan]模式 1：快速搜索（Quick Search）[/cyan]\n"
        "特点：快速、直接，适合简单查询",
        border_style="cyan"
    ))
    console.print(f"🔍 查询：{query}\n")

    try:
        result = search_client.quick_search(query)
        console.print(Panel(result.text[:300] + "...", title="结果摘要", border_style="green"))
        console.print(f"[yellow]📚 引用：{len(result.citations)} 个[/yellow]")
    except Exception as e:
        console.print(f"[red]❌ 失败：{e}[/red]")

    # 2. 智能体搜索模式（需要支持推理的模型）
    console.print("\n" + "=" * 80)
    console.print(Panel(
        "[cyan]模式 2：智能体搜索（Agentic Search）[/cyan]\n"
        "特点：带推理能力，可以多步搜索和分析",
        border_style="cyan"
    ))
    console.print(f"🔍 查询：{query}\n")

    try:
        # 注意：这需要推理模型支持
        result = search_client.agentic_search(query)
        console.print(Panel(result.text[:300] + "...", title="结果摘要", border_style="green"))
        console.print(f"[yellow]📚 引用：{len(result.citations)} 个[/yellow]")
        console.print(f"[blue]🔄 搜索调用：{len(result.search_calls)} 次[/blue]")
    except Exception as e:
        console.print(f"[red]❌ 失败：{e}[/red]")
        console.print("[yellow]提示：智能体模式需要支持推理的模型[/yellow]")

    # 3. 深度研究模式
    console.print("\n" + "=" * 80)
    console.print(Panel(
        "[cyan]模式 3：深度研究（Deep Research）[/cyan]\n"
        "特点：多步骤深入研究，适合复杂主题\n"
        "⚠️  注意：此模式可能运行较长时间（数分钟）",
        border_style="cyan"
    ))

    console.print("[yellow]💡 深度研究模式演示已跳过（需要较长时间）[/yellow]")
    console.print("[yellow]   如需测试，请取消下方代码的注释[/yellow]\n")

    # 取消注释以测试深度研究模式
    # try:
    #     console.print(f"🔍 研究主题：{query}\n")
    #     console.print("[yellow]⏳ 正在进行深度研究，可能需要几分钟...[/yellow]\n")
    #     
    #     result = search_client.deep_research(query)
    #     console.print(Panel(result.text[:500] + "...", title="研究报告摘要", border_style="green"))
    #     console.print(f"[yellow]📚 引用：{len(result.citations)} 个[/yellow]")
    #     console.print(f"[blue]🔄 搜索调用：{len(result.search_calls)} 次[/blue]")
    # except Exception as e:
    #     console.print(f"[red]❌ 失败：{e}[/red]")

    console.print("\n" + "=" * 80)
    console.print("[green]✅ 演示完成！[/green]\n")


if __name__ == "__main__":
    main()
