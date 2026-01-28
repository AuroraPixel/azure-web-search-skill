"""主程序入口 - 交互式 Web Search 工具"""

import sys
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from src.config import get_settings, setup_env_file
from src.logger import setup_logger
from src.models import SearchMode
from src.web_search import AzureWebSearch

console = Console()


def print_banner():
    """打印欢迎横幅"""
    banner = """
    ╔═══════════════════════════════════════════════════════╗
    ║                                                       ║
    ║         🔍 Azure OpenAI Web Search 工具 🔍            ║
    ║                                                       ║
    ║              基于 Python + uv 构建                     ║
    ║                                                       ║
    ╚═══════════════════════════════════════════════════════╝
    """
    console.print(banner, style="bold cyan")


def show_menu() -> str:
    """显示菜单并获取用户选择"""
    console.print("\n" + "=" * 60, style="cyan")
    console.print("请选择搜索模式：", style="bold yellow")
    console.print("  [1] 快速搜索 (Quick Search) - 快速获取结果", style="green")
    console.print("  [2] 智能体搜索 (Agentic Search) - 带推理的搜索", style="blue")
    console.print("  [3] 深度研究 (Deep Research) - 深入分析", style="magenta")
    console.print("  [4] 更改国家/地区", style="yellow")
    console.print("  [0] 退出", style="red")
    console.print("=" * 60 + "\n", style="cyan")

    choice = Prompt.ask("请输入选项", choices=["0", "1", "2", "3", "4"], default="1")
    return choice


def display_result(result, mode: str):
    """显示搜索结果"""
    console.print("\n" + "=" * 60, style="green")
    console.print(f"✅ 搜索完成 ({mode})", style="bold green")
    console.print("=" * 60, style="green")

    # 显示结果文本
    console.print(Panel(result.text, title="📝 搜索结果", border_style="green"))

    # 显示统计信息
    stats_table = Table(show_header=False, box=None)
    stats_table.add_column("指标", style="cyan")
    stats_table.add_column("数值", style="yellow")

    stats_table.add_row("📚 引用数量", str(len(result.citations)))
    stats_table.add_row("🔄 搜索调用", str(len(result.search_calls)))
    stats_table.add_row("🌐 唯一来源", str(len(result.get_unique_sources())))

    console.print("\n")
    console.print(stats_table)

    # 显示引用源
    if result.citations:
        console.print("\n[yellow]📚 引用来源：[/yellow]\n")
        sources = result.get_unique_sources()
        for i, source in enumerate(sources[:5], 1):  # 只显示前 5 个
            console.print(f"  {i}. {source['title']}", style="bright_white")
            console.print(f"     {source['url']}", style="dim")

        if len(sources) > 5:
            console.print(f"\n  ... 还有 {len(sources) - 5} 个来源", style="dim")


def main():
    """主程序"""
    print_banner()

    # 检查环境文件
    if not setup_env_file():
        console.print("\n[red]❌ 请先配置环境变量文件[/red]")
        return

    # 加载配置
    try:
        settings = get_settings()
        console.print("[green]✅ 配置加载成功[/green]")
    except Exception as e:
        console.print(f"[red]❌ 配置加载失败：{e}[/red]")
        console.print("\n[yellow]💡 请检查 .env 文件中的配置是否正确[/yellow]")
        return

    # 设置日志
    setup_logger(level=settings.log_level)

    # 创建搜索客户端
    try:
        search_client = AzureWebSearch(settings)
        console.print("[green]✅ 连接成功[/green]\n")
    except Exception as e:
        console.print(f"[red]❌ 连接失败：{e}[/red]")
        return

    # 当前国家设置
    current_country: Optional[str] = settings.web_search_country

    # 主循环
    while True:
        try:
            # 显示菜单
            choice = show_menu()

            if choice == "0":
                console.print("\n[cyan]👋 感谢使用，再见！[/cyan]\n")
                break

            elif choice == "4":
                # 更改国家
                console.print("\n[yellow]💡 请输入国家代码（ISO 3166-1 alpha-2），例如：US, CN, JP[/yellow]")
                console.print("[yellow]   输入 'none' 清除国家设置[/yellow]")
                country = Prompt.ask("国家代码", default=current_country or "none")

                if country.lower() == "none":
                    current_country = None
                    console.print("[green]✅ 已清除国家设置[/green]")
                else:
                    current_country = country.upper()
                    console.print(f"[green]✅ 国家设置为：{current_country}[/green]")
                continue

            # 获取搜索查询
            query = Prompt.ask("\n[cyan]🔍 请输入搜索查询[/cyan]")

            if not query.strip():
                console.print("[yellow]⚠️  查询不能为空[/yellow]")
                continue

            # 显示当前设置
            info_lines = [f"查询：{query}"]
            if current_country:
                info_lines.append(f"地区：{current_country}")

            console.print("")
            console.print(Panel("\n".join(info_lines), title="🔍 搜索信息", border_style="cyan"))

            # 执行搜索
            console.print("\n[yellow]⏳ 正在搜索...[/yellow]\n")

            if choice == "1":
                result = search_client.quick_search(query, country=current_country)
                display_result(result, "快速搜索")

            elif choice == "2":
                result = search_client.agentic_search(query, country=current_country)
                display_result(result, "智能体搜索")

            elif choice == "3":
                console.print("[yellow]⚠️  深度研究可能需要数分钟时间...[/yellow]")
                confirm = Prompt.ask("确认继续", choices=["y", "n"], default="n")
                if confirm.lower() == "y":
                    result = search_client.deep_research(query, country=current_country)
                    display_result(result, "深度研究")
                else:
                    console.print("[yellow]已取消[/yellow]")

        except KeyboardInterrupt:
            console.print("\n\n[yellow]⚠️  操作已取消[/yellow]")
            continue

        except Exception as e:
            console.print(f"\n[red]❌ 搜索失败：{e}[/red]")
            console.print("[yellow]💡 请检查您的配置和网络连接[/yellow]")

        # 询问是否继续
        console.print("\n")
        continue_choice = Prompt.ask("继续搜索", choices=["y", "n"], default="y")
        if continue_choice.lower() != "y":
            console.print("\n[cyan]👋 感谢使用，再见！[/cyan]\n")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\n[cyan]👋 程序已退出[/cyan]\n")
        sys.exit(0)
